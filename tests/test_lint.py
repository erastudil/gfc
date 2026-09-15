# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def ids(source: str, **kwargs) -> set[str]:
    return {f.rule for f in lint_text(source, **kwargs)}


class LintFixtures(unittest.TestCase):
    def test_clear_is_clean(self) -> None:
        text = (FIXTURES / "clear.md").read_text(encoding="utf-8")
        self.assertEqual(lint_text(text, mode="prose"), [])
        self.assertEqual(lint_text(text, mode="educate"), [])

    def test_slop_hits_core(self) -> None:
        text = (FIXTURES / "slop.md").read_text(encoding="utf-8")
        got = ids(text)
        for needed in ("G001", "G002", "G003", "G007", "G008", "G009", "G010"):
            self.assertIn(needed, got, msg=f"missing {needed} in {got}")

    def test_educate_wrong(self) -> None:
        text = (FIXTURES / "educate_wrong.md").read_text(encoding="utf-8")
        self.assertIn("G011", ids(text, mode="educate"))
        self.assertNotIn("G011", ids(text, mode="prose"))

    def test_educate_right(self) -> None:
        text = (FIXTURES / "educate_right.md").read_text(encoding="utf-8")
        self.assertNotIn("G011", ids(text, mode="educate"))

    def test_latch(self) -> None:
        text = (FIXTURES / "latch.md").read_text(encoding="utf-8")
        self.assertIn("G006", ids(text))

    def test_echo(self) -> None:
        a = (FIXTURES / "echo_a.md").read_text(encoding="utf-8")
        b = (FIXTURES / "echo_b.md").read_text(encoding="utf-8")
        self.assertIn("G005", ids(a, corpus=[("echo_b.md", b)]))
        self.assertEqual(lint_text(a, corpus=[("other.md", "unrelated short note.")]), [])

    def test_regurgitate_and_heading(self) -> None:
        ask = (FIXTURES / "ask.txt").read_text(encoding="utf-8")
        text = (FIXTURES / "regurgitate.md").read_text(encoding="utf-8")
        got = ids(text, ask=ask)
        self.assertIn("G004", got)
        self.assertIn("G013", got)

    def test_drift(self) -> None:
        ask = "explain how to rotate the canary after tests pass"
        text = (FIXTURES / "drift.md").read_text(encoding="utf-8")
        self.assertIn("G012", ids(text, ask=ask))


class LintShapes(unittest.TestCase):
    def test_hard_negative_numbered_contrast(self) -> None:
        text = "AI didn't take my job. It created 12 new jobs.\n"
        self.assertNotIn("G001", ids(text))

    def test_empty_reversal(self) -> None:
        text = "It's not a tool. It's a teammate.\n"
        self.assertIn("G001", ids(text))

    def test_blockquote_skipped(self) -> None:
        text = "> It's not a tool. It's a teammate.\n"
        self.assertNotIn("G001", ids(text))

    def test_code_fence_skipped(self) -> None:
        text = "use the call.\n\n```\nIt's not a tool. It's a teammate.\n```\n"
        self.assertNotIn("G001", ids(text))

    def test_contained_analogy_ok(self) -> None:
        text = (
            "Think of spacetime as a warm loaf of bread. Slice it. Each slice is a now.\n\n"
            "The equations stay in physics from here.\n"
        )
        self.assertNotIn("G006", ids(text))

    def test_single_emdash_ok(self) -> None:
        text = "The host stores a number — the agent must read the file.\n"
        self.assertNotIn("G007", ids(text))


if __name__ == "__main__":
    unittest.main()
