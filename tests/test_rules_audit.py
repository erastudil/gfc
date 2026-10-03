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


class TestRulesAudit(unittest.TestCase):
    def test_empty_string_returns_no_infractions(self):
        """An empty string should yield an empty list of infractions."""
        self.assertEqual(lint_text(""), [])

    def test_clean_simple_sentences_prose_mode_zero_violations(self):
        """Clean simple sentences in prose mode should produce zero violations."""
        text = "Hello world. This is a test."
        self.assertEqual(lint_text(text, mode="prose"), [])
