#!/usr/bin/env python3
"""Tests for skill and application freshness checks."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from check_skill_freshness import (
    application_state_status,
    build_manifest,
    compare_manifest,
    skill_root,
    write_application_state,
    write_manifest,
)


class SkillFreshnessTests(unittest.TestCase):
    def test_repository_manifest_matches_current_skill(self) -> None:
        current, errors = compare_manifest(skill_root())
        self.assertEqual(errors, [])
        self.assertRegex(current["skill_version"], r"^\d+\.\d+\.\d+")
        self.assertEqual(len(current["content_sha256"]), 64)

    def test_recorded_application_state_is_current(self) -> None:
        current = build_manifest(skill_root())
        with tempfile.TemporaryDirectory() as temporary_directory:
            state_file = Path(temporary_directory) / "skill-state.json"
            write_application_state(state_file, current)
            status, _, errors = application_state_status(state_file, current)
            self.assertEqual(status, "current")
            self.assertEqual(errors, [])

    def test_old_application_state_is_stale(self) -> None:
        current = build_manifest(skill_root())
        with tempfile.TemporaryDirectory() as temporary_directory:
            state_file = Path(temporary_directory) / "skill-state.json"
            state_file.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "skill_name": "tailor-tech-job-application",
                        "skill_version": "0.9.0",
                        "content_sha256": "0" * 64,
                    }
                ),
                encoding="utf-8",
            )
            status, _, errors = application_state_status(state_file, current)
            self.assertEqual(status, "stale")
            self.assertTrue(any("recorded skill version" in error for error in errors))
            self.assertTrue(any("instruction digest" in error for error in errors))

    def test_manifest_update_requires_version_bump_for_changed_content(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "references").mkdir()
            (root / "SKILL.md").write_text("name: test\n", encoding="utf-8")
            (root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
            (root / "references" / "version-history.md").write_text(
                "# Version history\n\n## 1.0.0\n",
                encoding="utf-8",
            )
            current = build_manifest(root)
            (root / "skill-manifest.json").write_text(
                json.dumps(current), encoding="utf-8"
            )
            (root / "SKILL.md").write_text(
                "name: test\ndescription: changed\n", encoding="utf-8"
            )
            with self.assertRaisesRegex(ValueError, "without a VERSION bump"):
                write_manifest(root)


if __name__ == "__main__":
    unittest.main()
