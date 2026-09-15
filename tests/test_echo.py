# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.echo import echo_hits

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class Echo(unittest.TestCase):
    def test_shared_span(self) -> None:
        a = (FIXTURES / "echo_a.md").read_text(encoding="utf-8")
        b = (FIXTURES / "echo_b.md").read_text(encoding="utf-8")
        hits = echo_hits(a, [("b", b)], n=8)
        self.assertTrue(hits)
        joined = " ".join(" ".join(h.ngram) for h in hits)
        self.assertIn("exponential backoff", joined)

    def test_clean_when_different(self) -> None:
        a = (FIXTURES / "echo_a.md").read_text(encoding="utf-8")
        hits = echo_hits(a, [("c", "the oven timer rang twice")], n=8)
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
