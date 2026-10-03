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


class RulesAudit(unittest.TestCase):
    """Verify that lint rules G001‑G003 behave as expected on basic inputs."""

    def test_empty_string_returns_no_infractions(self) -> None:
        """An empty string should yield an empty list of infractions."""
        self.assertEqual(lint_text(""), [])

    def test_clean_simple_sentences_prose_mode_passes(self) -> None:
        """Simple, well‑formed sentences should produce zero violations in prose mode."""
        samples = [
            "The quick brown fox jumps over the lazy dog.",
            "She sells seashells by the seashore.",
            "Python is a versatile programming language.",
            "Today is a good day to learn something new.",
        ]
        for sentence in samples:
            with self.subTest(sentence=sentence):
                self.assertEqual(
                    lint_text(sentence, mode="prose"),
                    [],
                    msg=f"Unexpected infractions for: {sentence!r}",
                )


if __name__ == "__main__":
    unittest.main()
