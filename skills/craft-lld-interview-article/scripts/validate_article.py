#!/usr/bin/env python3
"""Run structural, bundle, and editorial release checks for an LLD article."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path


REQUIRED_SECTION_GROUPS = {
    "problem framing": ("understanding the problem", "problem understanding"),
    "clarifying questions": ("clarifying questions", "requirements discovery"),
    "final requirements": ("final requirements",),
    "out of scope": ("out of scope",),
    "entity pruning": ("finding the core entities", "core entities", "entities and responsibilities"),
    "class design": ("class design",),
    "final class design": ("final class design",),
    "core implementation": ("core implementation", "key implementation"),
    "runnable implementation": ("complete runnable implementation", "runnable reference implementation"),
    "verification": ("verification", "walkthrough"),
    "extensibility": ("extensibility", "extensions"),
    "level expectations": ("expected at each level", "level expectations"),
}

PLACEHOLDER_PATTERNS = (
    r"\bTODO\b", r"\bTBD\b", r"\bFIXME\b", r"placeholder",
    r"replace this", r"replace me", r"left as (?:an )?exercise",
    r"exercise for the reader", r"CandidateName", r"CentralType", r"CentralClass",
)

SOURCE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".h", ".hpp", ".java", ".js",
    ".kt", ".py", ".rb", ".rs", ".swift", ".ts",
}

FORMULAIC_PATTERNS = {
    "generic opening": r"\b(?:in today'?s fast-paced world|let'?s dive in)\b",
    "empty signposting": r"\b(?:it is worth noting|with that in mind|the key is|the important thing is)\b",
    "inflated adjective": r"\b(?:robust|seamless|comprehensive|powerful|elegant)\b",
    "mechanical contrast": r"\bnot\s+[^.!?;]{1,80}\s+but\s+[^.!?;]{1,80}",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument("--solution-dir", type=Path)
    parser.add_argument("--pdf", type=Path)
    parser.add_argument("--candidate-level", choices=("junior", "mid-level", "senior"))
    return parser.parse_args()


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def headings(markdown: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", re.sub(r"[*_`]", "", match.group(1)).strip().lower())
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", markdown, re.MULTILINE)
    ]


def contains_heading(all_headings: list[str], alternatives: tuple[str, ...]) -> bool:
    return any(alternative in heading for heading in all_headings for alternative in alternatives)


def class_design_sections(markdown: str) -> list[tuple[str, str]]:
    match = re.search(
        r"^##\s+Class Design\s*$\n(?P<body>.*?)(?=^##\s+Final Class Design\s*$)",
        markdown,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if not match:
        return []
    body = match.group("body")
    starts = list(re.finditer(r"^###\s+(.+?)\s*$", body, re.MULTILINE))
    sections = []
    for index, start in enumerate(starts):
        end = starts[index + 1].start() if index + 1 < len(starts) else len(body)
        sections.append((re.sub(r"[*_`]", "", start.group(1)).strip(), body[start.end():end]))
    return sections


def validate_filename(path: Path, markdown: str, candidate_level: str | None) -> list[str]:
    errors = []
    if path.name.lower() == "article.md":
        errors.append("Final Markdown filename must use the question name, not article.md.")
    title_match = re.search(r"^#\s+(?:Design\s+)?(.+?)\s*$", markdown, re.MULTILINE | re.IGNORECASE)
    if title_match:
        expected = slugify(re.sub(r"[*_`]", "", title_match.group(1)))
        if candidate_level:
            expected = f"{expected}-{candidate_level}"
        if path.stem != expected:
            errors.append(f"Markdown stem should be '{expected}' for this title and level; found '{path.stem}'.")
    return errors


def validate_article(path: Path, candidate_level: str | None) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_file():
        return [f"Article does not exist: {path}"], warnings

    markdown = path.read_text(encoding="utf-8")
    all_headings = headings(markdown)
    errors.extend(validate_filename(path, markdown, candidate_level))

    for label, alternatives in REQUIRED_SECTION_GROUPS.items():
        if not contains_heading(all_headings, alternatives):
            errors.append(f"Missing required section: {label}")

    if not re.search(r"\b(?:Implement in interview|Mention if asked|Production extension)\b", markdown, re.IGNORECASE):
        errors.append("Mark a design recommendation by interview scope.")

    if not re.search(r"```mermaid\s+classDiagram\b", markdown, re.IGNORECASE):
        errors.append("Include a synchronized Mermaid UML-lite class diagram.")

    if markdown.count("```") % 2:
        errors.append("Code fences are unbalanced.")
    if re.search(r"```[^\n]*\n\s*```", markdown):
        errors.append("An empty fenced code block remains.")
    for pattern in PLACEHOLDER_PATTERNS:
        if re.search(pattern, markdown, re.IGNORECASE):
            errors.append(f"Unresolved placeholder-like text matches: {pattern}")

    derived_classes = class_design_sections(markdown)
    if not derived_classes:
        errors.append("Class Design must contain per-class level-three subsections.")
    elif len(derived_classes) < 2:
        warnings.append("Only one per-class derivation was found; confirm the design truly has one central class.")
    for name, body in derived_classes:
        if not re.search(r"\b(?:state|field|remember|invariant)\b", body, re.IGNORECASE):
            errors.append(f"Class Design for {name} does not derive state or an invariant.")
        if not re.search(r"\b(?:method|operation|caller|transition|query|command)\b", body, re.IGNORECASE):
            errors.append(f"Class Design for {name} does not derive methods from behavior.")
        if "```" not in body:
            warnings.append(f"Class Design for {name} has no compact interface sketch.")

    numbered_requirements = re.findall(r"^\s*\d+[.)]\s+\S", markdown, re.MULTILINE)
    if len(numbered_requirements) < 4:
        warnings.append("Fewer than four numbered requirements were found.")
    if len(markdown.split()) < 1000:
        warnings.append("The article is unusually short; confirm every central class and core operation is covered.")

    word_count = max(1, len(markdown.split()))
    em_dash_count = markdown.count("—")
    if em_dash_count > max(3, word_count // 500):
        warnings.append(f"Em dash appears {em_dash_count} times; check for habitual punctuation.")
    for label, pattern in FORMULAIC_PATTERNS.items():
        count = len(re.findall(pattern, markdown, re.IGNORECASE))
        threshold = 0 if label == "generic opening" else 2
        if count > threshold:
            warnings.append(f"{label.capitalize()} pattern appears {count} time(s); revise low-information repetition.")

    if not re.search(r"\b(?:alternative|option|trade-?off|counterexample|decision)\b", markdown, re.IGNORECASE):
        warnings.append("No consequential alternative analysis was detected; confirm the problem genuinely has no useful pressure point.")
    return errors, warnings


def validate_solution(path: Path) -> tuple[list[str], list[str], list[Path]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not path.is_dir():
        return [f"Solution directory does not exist: {path}"], warnings, []

    files = [item for item in path.rglob("*") if item.is_file() and "__pycache__" not in item.parts]
    source_files = [item for item in files if item.suffix.lower() in SOURCE_SUFFIXES]
    if not source_files:
        errors.append("Solution directory contains no recognized source files.")
        return errors, warnings, files
    def is_test_source(item: Path) -> bool:
        relative_parts = item.relative_to(path).parts
        return (
            "test" in item.name.lower()
            or "spec" in item.name.lower()
            or "test" in relative_parts
            or "tests" in relative_parts
        )

    if not all("src" in item.relative_to(path).parts or is_test_source(item) for item in source_files):
        errors.append("Production source files must live under solution/src and tests under a test root.")

    test_files = [item for item in source_files if is_test_source(item)]
    if not test_files:
        errors.append("Solution directory contains no recognizable test source file.")

    production = [item for item in source_files if item not in test_files]
    if len(production) >= 4:
        relative_parents = {
            item.relative_to(path).parent.as_posix() for item in production
        }
        if len(relative_parents) < 2:
            errors.append("Four or more production source files are flat; add meaningful responsibility-based directories.")

    java_files = [item for item in source_files if item.suffix.lower() == ".java"]
    if java_files:
        for item in java_files:
            relative = item.relative_to(path).as_posix()
            if item in test_files and not relative.startswith("src/test/java/"):
                errors.append(f"Java test must use src/test/java: {relative}")
            if item in production and not relative.startswith("src/main/java/"):
                errors.append(f"Java source must use src/main/java: {relative}")

    for source_file in source_files:
        text = source_file.read_text(encoding="utf-8", errors="replace")
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"{source_file}: placeholder-like text matches: {pattern}")
    return errors, warnings, files


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def appendix_files(solution_dir: Path) -> list[Path]:
    ignored = {".git", ".idea", ".pytest_cache", ".venv", "__pycache__", "build", "dist", "node_modules", "out", "target", "venv"}
    build_names = {"CMakeLists.txt", "Makefile", "README.md", "build.gradle", "gradlew", "gradlew.bat", "package-lock.json", "package.json", "pom.xml", "pyproject.toml", "requirements.txt", "settings.gradle", "tsconfig.json"}
    extras = {".json", ".kts", ".toml", ".xml", ".yaml", ".yml"}
    return sorted(
        (
            path for path in solution_dir.rglob("*")
            if path.is_file()
            and not any(part in ignored for part in path.parts)
            and (path.suffix.lower() in SOURCE_SUFFIXES | extras or path.name in build_names)
        ),
        key=lambda item: item.relative_to(solution_dir).as_posix(),
    )


def validate_pdf(pdf_path: Path, article_path: Path, markdown: str, solution_dir: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not pdf_path.is_file():
        return [f"PDF does not exist: {pdf_path}"], warnings
    if pdf_path.name.lower() == "article.pdf":
        errors.append("Final PDF filename must use the question name, not article.pdf.")
    if pdf_path.stem != article_path.stem:
        errors.append("Markdown and PDF stems do not match.")

    try:
        from pypdf import PdfReader
    except ImportError:
        return errors, ["pypdf is unavailable; PDF text and appendix parity were not checked."]

    reader = PdfReader(str(pdf_path))
    if not reader.pages:
        return errors + ["PDF contains no pages."], warnings
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    collapsed = re.sub(r"\s+", " ", text)
    compact = re.sub(r"\s+", "", text)
    if "Appendix: Complete Runnable Code" not in collapsed:
        errors.append("PDF is missing Appendix: Complete Runnable Code.")
    if "[Diagram source fallback]" in collapsed:
        errors.append("PDF contains an unsupported diagram fallback; render the required diagram visually.")

    article_headings = [
        re.sub(r"[*_`]", "", value).strip()
        for value in re.findall(r"^#{1,3}\s+(.+?)\s*$", markdown, re.MULTILINE)
    ]
    for heading in article_headings:
        if heading not in collapsed:
            errors.append(f"PDF body is missing Markdown heading: {heading}")

    for path in appendix_files(solution_dir):
        relative = (Path("solution") / path.relative_to(solution_dir)).as_posix()
        if relative not in collapsed:
            errors.append(f"PDF appendix is missing file path: {relative}")
        digest = sha256(path)
        if digest not in compact:
            errors.append(f"PDF appendix checksum does not match or is missing: {relative}")
    if "APPENDIX_MANIFEST_BEGIN" not in collapsed or "APPENDIX_MANIFEST_END" not in collapsed:
        errors.append("PDF appendix manifest markers are missing.")
    warnings.append(f"PDF has {len(reader.pages)} page(s); visual page inspection is still required.")
    return errors, warnings


def main() -> int:
    args = parse_args()
    errors, warnings = validate_article(args.article, args.candidate_level)
    markdown = args.article.read_text(encoding="utf-8") if args.article.is_file() else ""

    if args.solution_dir is not None:
        solution_errors, solution_warnings, _ = validate_solution(args.solution_dir)
        errors.extend(solution_errors)
        warnings.extend(solution_warnings)
    if args.pdf is not None:
        if args.solution_dir is None:
            errors.append("--pdf requires --solution-dir for appendix parity checks.")
        else:
            pdf_errors, pdf_warnings = validate_pdf(args.pdf, args.article, markdown, args.solution_dir)
            errors.extend(pdf_errors)
            warnings.extend(pdf_warnings)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(f"Validation passed with {len(warnings)} warning(s).")
    print("Compilation, test execution, diagram semantics, and visual PDF review remain explicit release checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
