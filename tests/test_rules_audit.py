# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

# Ensure the src directory is on the import path, mirroring tests/test_lint.py
_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text


class RulesAuditTest(unittest.TestCase):
    """Verify lint rules G001 through G003 on basic inputs."""

    def test_empty_string_returns_empty(self) -> None:
        """An empty string should yield no infractions."""
        self.assertEqual(lint_text(""), [])

    def test_clean_simple_sentences_prose_mode(self) -> None:
        """Clean, simple prose should produce zero violations in prose mode."""
        clean_text = (
            "The sky is blue.\n"
            "Birds fly.\n"
            "Water is wet.\n"
        )
        # lint_text returns a list of Infractions; we expect an empty list.
        self.assertEqual(lint_text(clean_text, mode="prose"), [])


if __name__ == "__main__":
    unittest.main()
