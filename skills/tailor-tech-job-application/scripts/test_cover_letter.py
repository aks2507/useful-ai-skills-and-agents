#!/usr/bin/env python3
"""Synthetic regressions for cover-letter advisories, not prose-quality scoring."""

import tempfile
import unittest
from pathlib import Path

from validate_application import check_cover_letter, check_style, validate


REPORT_CARD = """Dear Hiring Team,
I built 12 services for 40 teams, reduced latency by 35%, saved $80,000,
increased coverage from 62% to 91%, and resolved 150 production incidents.
I also led 3 migrations and supported 18 developers.
Sincerely,
Example Candidate
"""


class CoverLetterChecksTests(unittest.TestCase):
    def test_achievement_dump_warns_without_claiming_quality_failure(self):
        errors, warnings = check_cover_letter(REPORT_CARD)
        self.assertEqual(errors, [])
        self.assertTrue(any("dense numerical detail" in item for item in warnings))

    def test_single_before_after_example_is_not_dense(self):
        _, warnings = check_cover_letter(
            "Helping engineers release changes confidently interests me. "
            "I helped reduce validation time from 90 minutes to 15 minutes. "
            "That work is relevant to your release-tooling responsibilities."
        )
        self.assertFalse(any("dense numerical detail" in item for item in warnings))

    def test_references_do_not_inflate_number_count(self):
        _, warnings = check_cover_letter(
            "# Cover letter for role 12345\nDate: 2026-09-16\nJob ID: 12345\n"
            "My experience with Java 17 would be useful here. "
            "[Engineering article](https://example.test/2026/09/16/12345) "
            "https://example.test/2026/09/16/12345"
        )
        self.assertFalse(any("dense numerical detail" in item for item in warnings))

    def test_letter_paragraphs_do_not_trigger_list_warning(self):
        _, warnings = check_cover_letter(
            "Dear Hiring Team,\n\nMaking shared services dependable interests me "
            "because other engineers need to trust them when shipping their own work. "
            "My API experience gives me a useful starting point for contributing."
        )
        self.assertFalse(any("list formatting" in item for item in warnings))

    def test_list_without_numbers_still_warns(self):
        for marker in ("-", "*", "+", "1.", "1)"):
            with self.subTest(marker=marker):
                _, warnings = check_cover_letter(
                    f"Dear Hiring Team,\n\n{marker} Built backend services.\n"
                    f"{marker} Led platform migrations."
                )
                self.assertTrue(any("list formatting" in item for item in warnings))

    def test_no_warning_does_not_prove_narrative_quality(self):
        # A heuristic cannot distinguish this unsupported catalogue from prose.
        # This deliberate limitation is why the skill requires editorial review.
        errors, warnings = check_cover_letter(
            "I built services. I led migrations. I improved reliability. "
            "I managed releases. I saved money."
        )
        self.assertEqual(errors, [])
        self.assertFalse(any("dense numerical detail" in item for item in warnings))
        self.assertFalse(any("list formatting" in item for item in warnings))

    def test_existing_hard_length_limit_remains(self):
        errors, _ = check_cover_letter("word " * 601)
        self.assertTrue(any("unlikely to fit one page" in item for item in errors))

    def test_style_constraints_remain_separate(self):
        errors, _ = check_style("cover-letter.md", "Not features but outcomes—I care.")
        self.assertEqual(len(errors), 2)

    def test_advisory_is_used_in_both_application_modes(self):
        with tempfile.TemporaryDirectory() as directory:
            application_dir = Path(directory)
            (application_dir / "cover-letter.md").write_text(REPORT_CARD, encoding="utf-8")
            for anonymous in (False, True):
                with self.subTest(anonymous=anonymous):
                    _, warnings = validate(application_dir, 200, anonymous_company=anonymous)
                    self.assertTrue(any("dense numerical detail" in item for item in warnings))


if __name__ == "__main__":
    unittest.main()
