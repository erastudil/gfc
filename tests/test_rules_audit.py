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
    def test_empty_string_returns_empty_list(self) -> None:
        self.assertEqual(lint_text(""), [])

    def test_clean_simple_sentences_in_prose_mode_pass(self) -> None:
        text = "Hello world. This is a test."
        self.assertEqual(lint_text(text, mode="prose"), [])

if __name__ == "__main__":
    unittest.main()
