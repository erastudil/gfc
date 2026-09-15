# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.strip import strip_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class Strip(unittest.TestCase):
    def test_drops_mush_and_disclaimer(self) -> None:
        raw = (FIXTURES / "slop.md").read_text(encoding="utf-8")
        out = strip_text(raw).lower()
        self.assertNotIn("happy to help", out)
        self.assertNotIn("legal advice", out)
        self.assertNotIn("let me know", out)
        self.assertNotIn("in conclusion", out)

    def test_keeps_code_fence(self) -> None:
        raw = "intro\n\n```\nI'd be happy to help!\n```\n"
        out = strip_text(raw)
        self.assertIn("I'd be happy to help!", out)

    def test_collapses_reversal(self) -> None:
        out = strip_text("It's not a tool. It's a teammate.\n")
        self.assertIn("teammate", out.lower())
        self.assertNotIn("not a tool", out.lower())


if __name__ == "__main__":
    unittest.main()
