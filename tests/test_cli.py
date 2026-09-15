# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import json
import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.__main__ import main

FIXTURES = Path(__file__).resolve().parent / "fixtures"


class Cli(unittest.TestCase):
    def test_lint_clear_zero(self) -> None:
        buf = StringIO()
        with patch("sys.stdout", buf):
            rc = main(["lint", str(FIXTURES / "clear.md")])
        self.assertEqual(rc, 0)

    def test_lint_slop_nonzero(self) -> None:
        buf = StringIO()
        with patch("sys.stdout", buf):
            rc = main(["lint", str(FIXTURES / "slop.md")])
        self.assertEqual(rc, 1)

    def test_lint_json(self) -> None:
        buf = StringIO()
        with patch("sys.stdout", buf):
            rc = main(["lint", str(FIXTURES / "slop.md"), "--json"])
        self.assertEqual(rc, 1)
        payload = json.loads(buf.getvalue())
        self.assertTrue(payload["findings"])

    def test_echo_hits(self) -> None:
        buf = StringIO()
        with patch("sys.stdout", buf):
            rc = main(
                [
                    "echo",
                    str(FIXTURES / "echo_a.md"),
                    "--corpus",
                    str(FIXTURES),
                ]
            )
        self.assertEqual(rc, 1)

    def test_prompt_genome(self) -> None:
        buf = StringIO()
        with patch("sys.stdout", buf):
            rc = main(["prompt", "genome"])
        self.assertEqual(rc, 0)
        self.assertIn("intuition first", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
