#!/usr/bin/env python3
"""Create a problem workspace from the article template."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create article.md and solution/ for an LLD interview article."
    )
    parser.add_argument("--title", required=True, help="Human-readable problem title")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--language", default="Java")
    parser.add_argument("--candidate-level", default="mid-level")
    parser.add_argument("--timebox", default="60")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite an existing article.md"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    skill_root = Path(__file__).resolve().parent.parent
    template_path = skill_root / "assets" / "article-template.md"
    article_path = args.output_dir / "article.md"
    solution_dir = args.output_dir / "solution"

    if article_path.exists() and not args.force:
        raise SystemExit(f"Refusing to overwrite {article_path}; pass --force to replace it.")

    text = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{TITLE}}": args.title,
        "{{LANGUAGE}}": args.language,
        "{{CANDIDATE_LEVEL}}": args.candidate_level,
        "{{TIMEBOX}}": str(args.timebox),
    }
    for placeholder, value in replacements.items():
        text = text.replace(placeholder, value)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    solution_dir.mkdir(exist_ok=True)
    article_path.write_text(text, encoding="utf-8")

    print(f"Created {article_path}")
    print(f"Created {solution_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
