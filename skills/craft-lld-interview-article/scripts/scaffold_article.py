#!/usr/bin/env python3
"""Create a named LLD article workspace and language-appropriate source roots."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


LEVELS = ("junior", "mid-level", "senior")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise argparse.ArgumentTypeError("title must contain a letter or number")
    return slug


def question_title(value: str) -> str:
    normalized = re.sub(r"^\s*design\s+(?:an?\s+|the\s+)?", "", value, flags=re.IGNORECASE).strip()
    return normalized or value.strip()


def package_name(slug: str) -> str:
    name = re.sub(r"[^a-z0-9]", "", slug)
    return name if name and not name[0].isdigit() else f"lld{name}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create question[-level].md and organized solution roots."
    )
    parser.add_argument("--title", required=True, help="Human-readable question title")
    parser.add_argument(
        "--output-dir", type=Path,
        help="Override the default <skill>/generated-content/<problem-slug> directory",
    )
    parser.add_argument("--language", default="Java")
    parser.add_argument(
        "--candidate-level",
        choices=LEVELS,
        help="Explicit level; included in the filename when supplied",
    )
    parser.add_argument("--timebox", default="60")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite the named Markdown file"
    )
    return parser.parse_args()


def source_roots(solution_dir: Path, language: str, root_package: str) -> list[Path]:
    normalized = language.strip().lower()
    if normalized == "java":
        main = solution_dir / "src" / "main" / "java" / root_package
        return [
            main / "model",
            main / "service",
            main / "demo",
            solution_dir / "src" / "test" / "java" / root_package,
        ]
    if normalized in {"python", "python 3", "python3"}:
        return [solution_dir / "src" / root_package, solution_dir / "tests"]
    if normalized in {"typescript", "ts"}:
        return [
            solution_dir / "src" / "model",
            solution_dir / "src" / "service",
            solution_dir / "tests",
        ]
    if normalized in {"c++", "cpp"}:
        return [
            solution_dir / "src" / "model",
            solution_dir / "src" / "service",
            solution_dir / "tests",
        ]
    return [solution_dir / "src", solution_dir / "tests"]


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    template_path = skill_root / "assets" / "article-template.md"
    title = question_title(args.title)
    slug = slugify(title)
    output_dir = args.output_dir or skill_root / "generated-content" / slug
    stem = slug if args.candidate_level is None else f"{slug}-{args.candidate_level}"
    article_path = output_dir / f"{stem}.md"
    pdf_path = output_dir / f"{stem}.pdf"
    solution_dir = output_dir / "solution"
    display_level = args.candidate_level or "mid-level"
    root_package = package_name(slug)

    if article_path.exists() and not args.force:
        raise SystemExit(
            f"Refusing to overwrite {article_path}; pass --force to replace it."
        )

    text = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{TITLE}}": title,
        "{{LANGUAGE}}": args.language,
        "{{CANDIDATE_LEVEL}}": display_level,
        "{{TIMEBOX}}": str(args.timebox),
    }
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    output_dir.mkdir(parents=True, exist_ok=True)
    for directory in source_roots(solution_dir, args.language, root_package):
        directory.mkdir(parents=True, exist_ok=True)
    article_path.write_text(text, encoding="utf-8")

    print(f"Created Markdown: {article_path}")
    print(f"Reserved PDF name: {pdf_path}")
    print(f"Created organized solution roots under: {solution_dir}")
    print(f"Suggested root package: {root_package}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
