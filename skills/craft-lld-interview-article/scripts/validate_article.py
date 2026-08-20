#!/usr/bin/env python3
"""Run structural release checks for an LLD interview article.

This helper does not execute implementation tests or render Mermaid diagrams.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED_SECTION_GROUPS = {
    "problem framing": ("understanding the problem", "problem understanding"),
    "clarifying questions": ("clarifying questions", "requirements discovery"),
    "final requirements": ("final requirements",),
    "out of scope": ("out of scope",),
    "core entities": ("core entities", "entities and responsibilities"),
    "class design": ("class design",),
    "final class design": ("final class design",),
    "core implementation": ("core implementation", "key implementation"),
    "runnable implementation": (
        "complete runnable implementation",
        "runnable reference implementation",
    ),
    "verification": ("verification", "walkthrough"),
    "extensibility": ("extensibility", "extensions"),
    "level expectations": ("expected at each level", "level expectations"),
}

PLACEHOLDER_PATTERNS = (
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"placeholder",
    r"replace this",
    r"replace me",
    r"left as (?:an )?exercise",
    r"exercise for the reader",
)

SOURCE_SUFFIXES = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".go",
    ".java",
    ".js",
    ".kt",
    ".py",
    ".rb",
    ".rs",
    ".swift",
    ".ts",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument("--solution-dir", type=Path)
    return parser.parse_args()


def headings(markdown: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", match.group(1).strip().lower())
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", markdown, re.MULTILINE)
    ]


def contains_heading(all_headings: list[str], alternatives: tuple[str, ...]) -> bool:
    return any(
        alternative in heading
        for heading in all_headings
        for alternative in alternatives
    )


def validate_article(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_file():
        return [f"Article does not exist: {path}"], warnings

    markdown = path.read_text(encoding="utf-8")
    all_headings = headings(markdown)

    for label, alternatives in REQUIRED_SECTION_GROUPS.items():
        if not contains_heading(all_headings, alternatives):
            errors.append(f"Missing required section: {label}")

    has_bad = any(re.search(r"\bbad\b", heading) for heading in all_headings)
    has_better = any(
        re.search(r"\b(?:good|great)\b", heading) for heading in all_headings
    )
    if not (has_bad and has_better):
        errors.append("Add at least one contextual Bad -> Good/Great comparison.")

    if not re.search(
        r"\b(?:Implement in interview|Mention if asked|Production extension)\b",
        markdown,
        re.IGNORECASE,
    ):
        errors.append("Mark a design recommendation by interview scope.")

    if "```mermaid" not in markdown.lower():
        errors.append("Include at least one useful Mermaid diagram.")

    if markdown.count("```") % 2:
        errors.append("Code fences are unbalanced.")

    if re.search(r"```[^\n]*\n\s*```", markdown):
        errors.append("An empty fenced code block remains.")

    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, markdown, re.IGNORECASE):
            errors.append(f"Unresolved placeholder-like text matches: {pattern}")

    numbered_requirements = re.findall(r"^\s*\d+[.)]\s+\S", markdown, re.MULTILINE)
    if len(numbered_requirements) < 2:
        warnings.append("Fewer than two numbered requirements were found.")

    if len(markdown.split()) < 800:
        warnings.append("The article is unusually short; confirm the reasoning is complete.")

    return errors, warnings


def validate_solution(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not path.is_dir():
        return [f"Solution directory does not exist: {path}"], warnings

    files = [item for item in path.rglob("*") if item.is_file()]
    source_files = [item for item in files if item.suffix.lower() in SOURCE_SUFFIXES]
    if not source_files:
        errors.append("Solution directory contains no recognized source files.")
        return errors, warnings

    test_files = [
        item
        for item in source_files
        if "test" in item.name.lower() or "spec" in item.name.lower()
    ]
    if not test_files:
        errors.append("Solution directory contains no recognizable test source file.")

    for source_file in source_files:
        text = source_file.read_text(encoding="utf-8", errors="replace")
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(
                    f"{source_file}: placeholder-like text matches: {pattern}"
                )

    return errors, warnings


def main() -> int:
    args = parse_args()
    errors, warnings = validate_article(args.article)

    if args.solution_dir is not None:
        solution_errors, solution_warnings = validate_solution(args.solution_dir)
        errors.extend(solution_errors)
        warnings.extend(solution_warnings)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(
            f"Structural validation failed with {len(errors)} error(s).",
            file=sys.stderr,
        )
        return 1

    print(f"Structural validation passed with {len(warnings)} warning(s).")
    print("Implementation execution and Mermaid rendering remain separate checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
