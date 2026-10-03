# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text


class TestRulesAudit(unittest.TestCase):
    def test_empty_string_returns_no_infractions(self):
        """An empty string should return an empty list of infractions."""
        self.assertEqual(lint_text("", mode="prose"), [])

    def test_clean_simple_sentences_pass(self):
        """Clean simple sentences in prose mode should pass with zero violations."""
        text = "This is a clean sentence. Another clear statement here."
        self.assertEqual(lint_text(text, mode="prose"), [])


if __name__ == "__main__":
    unittest.main()
