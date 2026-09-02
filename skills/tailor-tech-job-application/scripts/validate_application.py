#!/usr/bin/env python3
"""Validate a tailored tech job application package.

The checks are structural and heuristic. Human review still decides whether the
research is sufficient and whether the writing sounds natural.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_FILES = (
    "company-context.md",
    "job-analysis.md",
    "candidate-evidence.md",
    "recruiter-email.md",
    "linkedin-connection.md",
    "cover-letter.md",
    "resume-change-log.md",
    "tailored-resume.pdf",
)

REQUIRED_HEADINGS = {
    "company-context.md": (
        "executive summary",
        "business and customers",
        "products and technical surface",
        "current priorities",
        "problems the company is addressing",
        "role and team implications",
        "candidate contribution opportunities",
        "unknowns and cautions",
        "sources",
    ),
    "job-analysis.md": (
        "role mission and outcomes",
        "prioritized responsibilities",
        "required and preferred qualifications",
        "keywords and terminology",
        "team problem signals",
        "unknowns",
    ),
    "candidate-evidence.md": (
        "supported",
        "safe rephrasing",
        "unsupported",
        "priority fit map",
    ),
    "resume-change-log.md": (
        "material changes",
        "keywords used",
        "unsupported keywords omitted",
        "content removed for space",
        "formatting and reconstruction notes",
    ),
}

PUBLIC_TEXT_FILES = (
    "recruiter-email.md",
    "linkedin-connection.md",
    "cover-letter.md",
)

PLACEHOLDER_PATTERNS = (
    r"\bTODO\b",
    r"\bTBD\b",
    r"\bFIXME\b",
    r"complete this section",
    r"replace (?:this|me)",
)

GENERIC_PHRASES = (
    "i hope this message finds you well",
    "i am writing to express my interest",
    "i am excited to apply",
    "deeply resonates",
    "unique blend",
    "fast-paced landscape",
    "at the intersection of",
    "delve",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("application_dir", type=Path)
    parser.add_argument("--linkedin-limit", type=int, default=200)
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def markdown_body(text: str) -> str:
    lines = []
    for line in text.splitlines():
        if re.match(r"^#{1,6}\s+", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w][\w'’-]*\b", text, re.UNICODE))


def visible_character_count(text: str) -> int:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return len(text)


def headings(text: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", match.group(1).strip().lower())
        for match in re.finditer(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    ]


def check_style(label: str, text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    lowered = text.lower()

    if "—" in text:
        errors.append(f"{label}: contains an em dash")

    contrast = re.search(r"\bnot\b[^.!?\n]{0,100}\bbut\b", text, re.IGNORECASE)
    if contrast:
        excerpt = re.sub(r"\s+", " ", contrast.group(0)).strip()
        errors.append(f"{label}: contains a staged 'not X but Y' contrast: {excerpt!r}")

    for phrase in GENERIC_PHRASES:
        if phrase in lowered:
            warnings.append(f"{label}: review generic phrase: {phrase!r}")

    return errors, warnings


def pdf_page_count(path: Path) -> tuple[int | None, str]:
    failures: list[str] = []
    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = __import__(module_name)
            reader = module.PdfReader(str(path))
            return len(reader.pages), module_name
        except (ImportError, AttributeError):
            continue
        except Exception as exc:  # pragma: no cover - depends on PDF parser
            failures.append(f"{module_name} failed: {exc}")

    if shutil.which("pdfinfo"):
        result = subprocess.run(
            ["pdfinfo", str(path)],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            match = re.search(r"^Pages:\s+(\d+)\s*$", result.stdout, re.MULTILINE)
            if match:
                return int(match.group(1)), "pdfinfo"
        failures.append("pdfinfo could not read page count")

    data = path.read_bytes()
    approximate = len(re.findall(rb"/Type\s*/Page\b", data))
    if approximate:
        return approximate, "PDF marker fallback"
    failures.append("no PDF page-count method succeeded")
    return None, "; ".join(failures)


def extract_pdf_text(path: Path) -> tuple[str | None, str]:
    failures: list[str] = []
    try:
        import pdfplumber

        with pdfplumber.open(path) as document:
            text = "\n".join(page.extract_text() or "" for page in document.pages)
        return text, "pdfplumber"
    except ImportError:
        pass
    except Exception as exc:  # pragma: no cover - depends on PDF parser
        failures.append(f"pdfplumber failed: {exc}")

    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = __import__(module_name)
            reader = module.PdfReader(str(path))
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text, module_name
        except (ImportError, AttributeError):
            continue
        except Exception as exc:  # pragma: no cover - depends on PDF parser
            failures.append(f"{module_name} failed: {exc}")

    if shutil.which("pdftotext"):
        result = subprocess.run(
            ["pdftotext", "-layout", str(path), "-"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return result.stdout, "pdftotext"
        failures.append(result.stderr.strip() or "pdftotext failed")

    failures.append("no PDF text-extraction method succeeded")
    return None, "; ".join(failures)


def validate(application_dir: Path, linkedin_limit: int) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not application_dir.is_dir():
        return [f"Application directory does not exist: {application_dir}"], warnings

    paths = {name: application_dir / name for name in REQUIRED_FILES}
    for name, path in paths.items():
        if not path.is_file():
            errors.append(f"Missing required file: {name}")

    text_files: dict[str, str] = {}
    for name, path in paths.items():
        if path.is_file() and path.suffix.lower() in {".md", ".txt"}:
            text = read_text(path)
            text_files[name] = text
            for pattern in PLACEHOLDER_PATTERNS:
                if re.search(pattern, text, re.IGNORECASE):
                    errors.append(f"{name}: unfinished placeholder matches {pattern!r}")

    for name, expected in REQUIRED_HEADINGS.items():
        text = text_files.get(name)
        if text is None:
            continue
        found = headings(text)
        for required in expected:
            if not any(required in heading for heading in found):
                errors.append(f"{name}: missing section {required!r}")

    context = text_files.get("company-context.md", "")
    urls = set(re.findall(r"https?://[^\s)>]+", context))
    if context and len(urls) < 3:
        errors.append("company-context.md: include at least three distinct direct source URLs")
    if context and "first-party" not in context.lower():
        errors.append("company-context.md: identify at least one First-party source")
    if context and not re.search(r"^Researched:\s*\d{4}-\d{2}-\d{2}", context, re.MULTILINE):
        errors.append("company-context.md: add a YYYY-MM-DD research date")

    email = markdown_body(text_files.get("recruiter-email.md", ""))
    if email:
        count = word_count(email)
        if count > 200:
            errors.append(f"recruiter-email.md: {count} words exceeds the 200-word limit")
        elif count < 60:
            warnings.append(f"recruiter-email.md: only {count} words; confirm the narrative is complete")

    note = markdown_body(text_files.get("linkedin-connection.md", ""))
    if note:
        count = visible_character_count(note)
        if count > linkedin_limit:
            errors.append(
                f"linkedin-connection.md: {count} characters exceeds the {linkedin_limit}-character limit"
            )

    cover = markdown_body(text_files.get("cover-letter.md", ""))
    if cover:
        count = word_count(cover)
        if count > 600:
            errors.append(f"cover-letter.md: {count} words is unlikely to fit one page")
        elif count < 250 or count > 500:
            warnings.append(f"cover-letter.md: {count} words; the usual target is 250 to 500")

    for name in PUBLIC_TEXT_FILES:
        text = text_files.get(name)
        if text:
            style_errors, style_warnings = check_style(name, text)
            errors.extend(style_errors)
            warnings.extend(style_warnings)

    pdf = paths["tailored-resume.pdf"]
    if pdf.is_file():
        if pdf.stat().st_size == 0:
            errors.append("tailored-resume.pdf: file is empty")
        else:
            pages, method = pdf_page_count(pdf)
            if pages is None:
                warnings.append(f"tailored-resume.pdf: page count not verified ({method})")
            elif pages != 1:
                errors.append(f"tailored-resume.pdf: expected 1 page, found {pages} via {method}")

            extracted, extraction_method = extract_pdf_text(pdf)
            if extracted is None:
                warnings.append(f"tailored-resume.pdf: text extraction not verified ({extraction_method})")
            else:
                if word_count(extracted) < 100:
                    errors.append("tailored-resume.pdf: extracted text is unexpectedly sparse")
                style_errors, style_warnings = check_style("tailored-resume.pdf", extracted)
                errors.extend(style_errors)
                warnings.extend(style_warnings)

    source_dir = application_dir / "resume-source"
    if not source_dir.is_dir() or not any(item.is_file() for item in source_dir.rglob("*")):
        errors.append("resume-source/: include the editable resume source")

    return errors, warnings


def main() -> int:
    args = parse_args()
    errors, warnings = validate(args.application_dir, args.linkedin_limit)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"Validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"Validation passed with {len(warnings)} warning(s).")
    print("Manual fact-checking, visual PDF review, and prose review remain required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
