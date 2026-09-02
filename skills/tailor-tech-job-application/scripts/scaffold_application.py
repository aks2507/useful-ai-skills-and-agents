#!/usr/bin/env python3
"""Create a safe workspace for one tailored tech job application."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


TEMPLATES = {
    "company-context.md": """# Company Context: {company}

Researched: <!-- Complete this section -->
Target role: {role}
Job description: <!-- Complete this section -->

## Executive summary

<!-- Complete this section -->

## Business and customers

<!-- Complete this section -->

## Products and technical surface

<!-- Complete this section -->

## Current priorities

<!-- Complete this section -->

## Problems the company is addressing

<!-- Complete this section -->

## Role and team implications

<!-- Complete this section -->

## Candidate contribution opportunities

<!-- Complete this section -->

## Unknowns and cautions

<!-- Complete this section -->

## Sources

| Source | Tier | Published or updated | Accessed | Supports |
| --- | --- | --- | --- | --- |
""",
    "job-analysis.md": """# Job Analysis: {role}

## Role mission and outcomes

<!-- Complete this section -->

## Prioritized responsibilities

<!-- Complete this section -->

## Required and preferred qualifications

<!-- Complete this section -->

## Keywords and terminology

<!-- Complete this section -->

## Team problem signals

<!-- Complete this section -->

## Unknowns

<!-- Complete this section -->
""",
    "candidate-evidence.md": """# Candidate Evidence Ledger

## Supported

<!-- Complete this section -->

## Safe rephrasing

<!-- Complete this section -->

## Unsupported

<!-- Complete this section -->

## Priority fit map

<!-- Complete this section -->
""",
    "recruiter-email.md": """# Recruiter Email

<!-- Complete this section -->
""",
    "linkedin-connection.md": """# LinkedIn Connection Note

<!-- Complete this section -->
""",
    "cover-letter.md": """# Cover Letter

<!-- Complete this section -->
""",
    "resume-change-log.md": """# Resume Change Log

## Material changes

| Location | Original | Tailored | Change type | Evidence | Reason |
| --- | --- | --- | --- | --- | --- |

## Keywords used

<!-- Complete this section -->

## Unsupported keywords omitted

<!-- Complete this section -->

## Content removed for space

<!-- Complete this section -->

## Formatting and reconstruction notes

<!-- Complete this section -->
""",
}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "application"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--company", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument(
        "--output",
        type=Path,
        help="Application directory. Defaults to <company>-<role> in the current directory.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = args.output or Path(f"{slugify(args.company)}-{slugify(args.role)}")
    output.mkdir(parents=True, exist_ok=True)
    (output / "resume-source").mkdir(exist_ok=True)

    created = 0
    skipped = 0
    for relative_path, template in TEMPLATES.items():
        target = output / relative_path
        if target.exists():
            print(f"SKIP existing file: {target}")
            skipped += 1
            continue
        target.write_text(
            template.format(company=args.company, role=args.role),
            encoding="utf-8",
        )
        print(f"CREATE: {target}")
        created += 1

    print(f"Workspace ready: {output} ({created} created, {skipped} preserved)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
