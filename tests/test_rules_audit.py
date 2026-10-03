# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text


class RulesAudit(unittest.TestCase):
    def test_empty_string_returns_empty_list(self) -> None:
        self.assertEqual(lint_text("", mode="prose"), [])

    def test_clean_simple_sentences_pass_in_prose_mode(self) -> None:
        text = (
            "The cat sat on the mat. "
            "The dog ran in the park. "
            "The sun rose in the east."
        )
        self.assertEqual(lint_text(text, mode="prose"), [])


if __name__ == "__main__":
    unittest.main()
