# tests/test_rules_audit.py
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
    """Verify that lint rules G001‑G003 behave as expected on basic inputs."""

    def test_empty_string_returns_empty(self):
        """An empty string should produce no infractions in any mode."""
        self.assertEqual(lint_text("", mode="prose"), [])
        self.assertEqual(lint_text("", mode="educate"), [])

    def test_clean_simple_sentences_prose_pass(self):
        """Simple, clean sentences should yield zero violations in prose mode."""
        clean_sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Hello world.",
            "This is a fine sentence.",
            "Python is a versatile programming language.",
            "She sells seashells by the seashore.",
        ]
        for sentence in clean_sentences:
            with self.subTest(sentence=sentence):
                self.assertEqual(
                    lint_text(sentence, mode="prose"),
                    [],
                    msg=f"Expected no infractions for: {sentence!r}",
                )


if __name__ == "__main__":
    unittest.main()
