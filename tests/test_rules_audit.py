# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Ensure the src directory is on the import path (mirrors tests/test_lint.py)
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text


class RulesAuditTest(unittest.TestCase):
    """Verification tests for lint rules G001 through G003."""

    def test_empty_string_returns_no_infractions(self) -> None:
        """An empty input should yield an empty list of infractions."""
        self.assertEqual(lint_text(""), [])

    def test_clean_simple_sentences_prose_mode_zero_violations(self) -> None:
        """
        Simple, well‑formed sentences in prose mode should not trigger any
        lint violations (including G001, G002, G003).
        """
        clean_text = (
            "The quick brown fox jumps over the lazy dog.\n"
            "She sells seashells by the seashore.\n"
            "Python is a versatile programming language.\n"
        )
        infractions = lint_text(clean_text, mode="prose")
        self.assertEqual(infractions, [], msg=f"Unexpected infractions: {infractions}")

        # Additionally assert that none of the specific rules we are verifying
        # appear in the result (defensive check).
        rule_ids = {inf.rule for inf in infractions}
        for rule in ("G001", "G002", "G003"):
            self.assertNotIn(rule, rule_ids, f"{rule} should not be triggered")


if __name__ == "__main__":
    unittest.main()
