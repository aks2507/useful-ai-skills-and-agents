#!/usr/bin/env python3
"""Verify skill integrity and detect stale application instructions."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SKILL_NAME = "tailor-tech-job-application"
MANIFEST_NAME = "skill-manifest.json"
STATE_SCHEMA_VERSION = 1
MANIFEST_SCHEMA_VERSION = 1
INCLUDED_TOP_LEVEL_FILES = {"SKILL.md", "VERSION"}
INCLUDED_DIRECTORIES = {"agents", "references", "scripts"}
IGNORED_NAMES = {"__pycache__", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def read_version(root: Path) -> str:
    version_path = root / "VERSION"
    if not version_path.is_file():
        raise ValueError(f"Missing {version_path}")
    version = version_path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        raise ValueError(f"Invalid semantic version in {version_path}: {version!r}")
    return version


def instruction_files(root: Path) -> dict[str, Path]:
    files: dict[str, Path] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in IGNORED_NAMES for part in relative.parts):
            continue
        if path.suffix.lower() in IGNORED_SUFFIXES or path.name == MANIFEST_NAME:
            continue
        if (
            relative.as_posix() in INCLUDED_TOP_LEVEL_FILES
            or relative.parts[0] in INCLUDED_DIRECTORIES
        ):
            files[relative.as_posix()] = path
    return dict(sorted(files.items()))


def build_manifest(root: Path) -> dict[str, Any]:
    version = read_version(root)
    file_hashes: dict[str, str] = {}
    combined = hashlib.sha256()
    for relative, path in instruction_files(root).items():
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        file_hashes[relative] = digest
        combined.update(relative.encode("utf-8"))
        combined.update(b"\0")
        combined.update(data)
        combined.update(b"\0")
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "skill_name": SKILL_NAME,
        "skill_version": version,
        "content_sha256": combined.hexdigest(),
        "files": file_hashes,
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Missing {path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object in {path}")
    return data


def compare_manifest(root: Path) -> tuple[dict[str, Any], list[str]]:
    current = build_manifest(root)
    manifest_path = root / MANIFEST_NAME
    try:
        recorded = load_json(manifest_path)
    except ValueError as exc:
        return current, [str(exc)]

    errors: list[str] = []
    for key in ("schema_version", "skill_name", "skill_version", "content_sha256"):
        if recorded.get(key) != current.get(key):
            errors.append(
                f"{MANIFEST_NAME}: {key} is {recorded.get(key)!r}; "
                f"current content requires {current.get(key)!r}"
            )

    recorded_files = recorded.get("files")
    if recorded_files != current["files"]:
        recorded_files = recorded_files if isinstance(recorded_files, dict) else {}
        current_paths = set(current["files"])
        recorded_paths = set(recorded_files)
        added = sorted(current_paths - recorded_paths)
        removed = sorted(recorded_paths - current_paths)
        changed = sorted(
            path
            for path in current_paths & recorded_paths
            if current["files"][path] != recorded_files[path]
        )
        if added:
            errors.append(f"{MANIFEST_NAME}: unrecorded files: {', '.join(added)}")
        if removed:
            errors.append(f"{MANIFEST_NAME}: missing recorded files: {', '.join(removed)}")
        if changed:
            errors.append(f"{MANIFEST_NAME}: changed files: {', '.join(changed)}")
    return current, errors


def _skill_name(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:4096]
    except OSError:
        return None
    match = re.search(r"^name:\s*['\"]?([^'\"\s]+)", text, re.MULTILINE)
    return match.group(1) if match else None


def candidate_skill_directories(cwd: Path | None = None) -> list[Path]:
    working = (cwd or Path.cwd()).resolve()
    roots: list[Path] = []
    for directory in (working, *working.parents):
        roots.append(directory / ".agents" / "skills")
    roots.append(Path.home() / ".agents" / "skills")
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    roots.append(codex_home / "skills")
    roots.append(Path("/etc/codex/skills"))
    return roots


def duplicate_skill_paths(root: Path, cwd: Path | None = None) -> list[Path]:
    canonical = root.resolve()
    duplicates: dict[Path, Path] = {}
    for skills_directory in candidate_skill_directories(cwd):
        candidate = skills_directory / SKILL_NAME / "SKILL.md"
        if not candidate.is_file() or _skill_name(candidate) != SKILL_NAME:
            continue
        resolved = candidate.parent.resolve()
        if resolved != canonical:
            duplicates[resolved] = candidate.parent
    return sorted(duplicates.values(), key=lambda path: str(path))


def verify_installation(
    root: Path, cwd: Path | None = None
) -> tuple[dict[str, Any], list[str]]:
    current, errors = compare_manifest(root)
    duplicates = duplicate_skill_paths(root, cwd)
    if duplicates:
        errors.append(
            "Duplicate skill copies can expose stale instructions: "
            + ", ".join(str(path) for path in duplicates)
        )
    return current, errors


def application_state_status(
    state_file: Path, current: dict[str, Any]
) -> tuple[str, dict[str, Any] | None, list[str]]:
    if not state_file.is_file():
        return "missing", None, [f"Missing application skill state: {state_file}"]
    try:
        state = load_json(state_file)
    except ValueError as exc:
        return "invalid", None, [str(exc)]

    errors: list[str] = []
    if state.get("schema_version") != STATE_SCHEMA_VERSION:
        errors.append(f"{state_file}: unsupported state schema")
    if state.get("skill_name") != SKILL_NAME:
        errors.append(f"{state_file}: belongs to a different skill")
    if state.get("skill_version") != current["skill_version"]:
        errors.append(
            f"{state_file}: recorded skill version {state.get('skill_version')!r} "
            f"is stale; current version is {current['skill_version']!r}"
        )
    if state.get("content_sha256") != current["content_sha256"]:
        errors.append(f"{state_file}: recorded instruction digest is stale")
    return ("stale" if errors else "current"), state, errors


def write_application_state(state_file: Path, current: dict[str, Any]) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "schema_version": STATE_SCHEMA_VERSION,
        "skill_name": SKILL_NAME,
        "skill_version": current["skill_version"],
        "content_sha256": current["content_sha256"],
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    state_file.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def write_manifest(root: Path) -> dict[str, Any]:
    current = build_manifest(root)
    manifest_path = root / MANIFEST_NAME
    previous: dict[str, Any] | None = None
    if manifest_path.is_file():
        previous = load_json(manifest_path)
    if (
        previous
        and previous.get("skill_version") == current["skill_version"]
        and previous.get("content_sha256") != current["content_sha256"]
    ):
        raise ValueError(
            "Skill content changed without a VERSION bump. Update VERSION and "
            "references/version-history.md before regenerating the manifest."
        )

    history = root / "references" / "version-history.md"
    history_text = history.read_text(encoding="utf-8") if history.is_file() else ""
    heading = rf"^##\s+{re.escape(current['skill_version'])}\s*$"
    if not re.search(heading, history_text, re.MULTILINE):
        raise ValueError(
            f"{history}: add a '## {current['skill_version']}' release entry first"
        )

    manifest_path.write_text(
        json.dumps(current, indent=2) + "\n", encoding="utf-8"
    )
    return current


def application_freshness_errors(application_dir: Path) -> list[str]:
    root = skill_root()
    current, errors = verify_installation(root)
    if errors:
        return errors
    _, _, state_errors = application_state_status(
        application_dir / "skill-state.json", current
    )
    return state_errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--state-file",
        type=Path,
        help="Application skill-state.json to compare with the current skill.",
    )
    parser.add_argument(
        "--record-state",
        action="store_true",
        help="Write the current version and digest after current instructions are reconciled.",
    )
    parser.add_argument(
        "--print-manifest",
        action="store_true",
        help="Print the manifest required by the current skill files.",
    )
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help=(
            "Regenerate skill-manifest.json after VERSION and version history are updated."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = skill_root()

    if args.write_manifest:
        try:
            current = write_manifest(root)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        print(
            f"Wrote {root / MANIFEST_NAME} for v{current['skill_version']} "
            f"({current['content_sha256'][:12]})"
        )
        return 0

    current, errors = verify_installation(root)

    if args.print_manifest:
        print(json.dumps(current, indent=2))
        return 0

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            "Skill installation is partial, unversioned, or ambiguous. "
            "Finish the update and regenerate the manifest before using the skill.",
            file=sys.stderr,
        )
        return 2

    print(
        f"Using {SKILL_NAME} v{current['skill_version']} "
        f"({current['content_sha256'][:12]})"
    )

    if args.record_state and args.state_file is None:
        print("ERROR: --record-state requires --state-file", file=sys.stderr)
        return 2

    if args.state_file is not None:
        status, previous, state_errors = application_state_status(
            args.state_file, current
        )
        if args.record_state:
            write_application_state(args.state_file, current)
            previous_version = previous.get("skill_version") if previous else None
            previous_digest = previous.get("content_sha256") if previous else None
            if previous and (
                previous_version != current["skill_version"]
                or previous_digest != current["content_sha256"]
            ):
                print(
                    "Recorded reconciled state: "
                    f"v{previous_version or 'unknown'} "
                    f"({str(previous_digest or 'unknown')[:12]}) -> "
                    f"v{current['skill_version']} ({current['content_sha256'][:12]})"
                )
            else:
                print(f"Recorded current state: {args.state_file}")
            return 0
        if state_errors:
            for error in state_errors:
                print(f"STALE: {error}", file=sys.stderr)
            print(
                "Reread the current skill and relevant references, reconcile existing "
                "artifacts, rerun current validation, then record the new state.",
                file=sys.stderr,
            )
            return 3
        print(f"Application skill state is {status}: {args.state_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
