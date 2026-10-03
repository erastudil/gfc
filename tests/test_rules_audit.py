# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text


class AuditRulesTest(unittest.TestCase):
    def test_empty_string_returns_no_infractions(self) -> None:
        """An empty string returns an empty list of infractions."""
        result = lint_text("", mode="prose")
        self.assertEqual(result, [])

    def test_clean_simple_sentences_pass_prose_mode(self) -> None:
        """Clean simple sentences in prose mode pass with zero violations."""
        text = "This is a simple sentence. It has no violations.\nAnother sentence follows."
        result = lint_text(text, mode="prose")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
