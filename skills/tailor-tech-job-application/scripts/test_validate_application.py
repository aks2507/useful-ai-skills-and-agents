#!/usr/bin/env python3
"""Focused tests for the resume layout lock."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_application import (
    latex_layout_signature,
    latex_preamble_signature,
    latex_section_signature,
    latex_structure_signature,
    validate,
    validate_format_change_approval,
)


ORIGINAL = r"""% !TEX program = xelatex
\documentclass[10pt]{article}
\usepackage[margin=0.5in]{geometry}
\newcommand{\resumeItem}[1]{\item #1}
\begin{document}
\section{Experience}
\begin{itemize}[leftmargin=*]
  \resumeItem{Built reliable APIs for internal services.}
\end{itemize}
\vspace{-4pt}
\section{Skills}
Python, Go
\end{document}
"""


class ResumeLayoutLockTests(unittest.TestCase):
    def assert_layout_equal(self, first: str, second: str) -> None:
        self.assertEqual(latex_preamble_signature(first), latex_preamble_signature(second))
        self.assertEqual(latex_structure_signature(first), latex_structure_signature(second))
        self.assertEqual(latex_section_signature(first), latex_section_signature(second))
        self.assertEqual(latex_layout_signature(first), latex_layout_signature(second))

    def test_content_only_edit_preserves_layout_signatures(self) -> None:
        tailored = ORIGINAL.replace(
            "Built reliable APIs for internal services.",
            "Improved API reliability for internal services.",
        ).replace("Python, Go", "Go, Python")
        self.assert_layout_equal(ORIGINAL, tailored)

    def test_preamble_change_is_detected(self) -> None:
        tailored = ORIGINAL.replace("margin=0.5in", "margin=0.35in")
        self.assertNotEqual(
            latex_preamble_signature(ORIGINAL), latex_preamble_signature(tailored)
        )

    def test_body_spacing_change_is_detected(self) -> None:
        tailored = ORIGINAL.replace(r"\vspace{-4pt}", r"\vspace{-8pt}")
        self.assertNotEqual(
            latex_layout_signature(ORIGINAL), latex_layout_signature(tailored)
        )

    def test_section_reorder_is_detected(self) -> None:
        tailored = ORIGINAL.replace(r"\section{Experience}", r"\section{Projects}")
        self.assertNotEqual(
            latex_section_signature(ORIGINAL), latex_section_signature(tailored)
        )

    def test_override_requires_valid_application_local_approval(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            application_dir = Path(temporary_directory)
            self.assertTrue(validate_format_change_approval(application_dir, None))

            approval = application_dir / "format-change-approval.md"
            approval.write_text(
                "# User-authorized resume format change\n\n"
                "User request: Please switch this resume to a two-column layout.\n\n"
                "## Approved changes\n\n"
                "- Change the body from one column to two columns.\n",
                encoding="utf-8",
            )
            self.assertEqual(
                validate_format_change_approval(application_dir, approval), []
            )

    def test_unapproved_override_keeps_layout_lock_active(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            application_dir = Path(temporary_directory)
            original_dir = application_dir / "resume-source" / "original"
            tailored_dir = application_dir / "resume-source" / "tailored"
            original_dir.mkdir(parents=True)
            tailored_dir.mkdir(parents=True)
            (original_dir / "main.tex").write_text(ORIGINAL, encoding="utf-8")
            (tailored_dir / "main.tex").write_text(
                ORIGINAL.replace("margin=0.5in", "margin=0.35in"),
                encoding="utf-8",
            )

            errors, _ = validate(
                application_dir,
                linkedin_limit=200,
                allow_format_change=True,
                format_change_approval=None,
                anonymous_company=True,
            )
            self.assertTrue(any("requires --format-change-approval" in error for error in errors))
            self.assertTrue(any("LaTeX preamble changed" in error for error in errors))

    def test_ancillary_project_change_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            application_dir = Path(temporary_directory)
            original_dir = application_dir / "resume-source" / "original"
            tailored_dir = application_dir / "resume-source" / "tailored"
            original_dir.mkdir(parents=True)
            tailored_dir.mkdir(parents=True)
            (original_dir / "main.tex").write_text(ORIGINAL, encoding="utf-8")
            (tailored_dir / "main.tex").write_text(ORIGINAL, encoding="utf-8")
            (original_dir / "resume.sty").write_text(
                "\\ProvidesPackage{resume}\n", encoding="utf-8"
            )
            (tailored_dir / "resume.sty").write_text(
                "\\ProvidesPackage{resume}\n\\setlength{\\parskip}{1pt}\n",
                encoding="utf-8",
            )

            errors, _ = validate(
                application_dir,
                linkedin_limit=200,
                anonymous_company=True,
            )
            self.assertTrue(any("LaTeX support file changed" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
