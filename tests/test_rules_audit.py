# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text


class RulesAuditTest(unittest.TestCase):
    def test_clean_input_reports_none(self) -> None:
        """One clean input that must report none."""
        clean = "The compiler builds the binary. Tests run on every commit."
        findings = lint_text(clean, mode="prose")
        self.assertEqual(findings, [])

    def test_rules_g001_g002_g003_reported(self) -> None:
        """One test that must report G001, G002, and G003."""
        # G001: empty reversal
        reversal = "It's not a tool. It's a teammate.\n"
        rule_ids_reversal = {f.rule for f in lint_text(reversal, mode="prose")}
        self.assertIn("G001", rule_ids_reversal)

        # G002: will-not / negative bullet list
        negative_list = (
            "- do not add disclaimers\n"
            "- never mention the prior thread\n"
            "- do not use em dashes\n"
        )
        rule_ids_neg = {f.rule for f in lint_text(negative_list, mode="prose")}
        self.assertIn("G002", rule_ids_neg)

        # G003: disclaimer
        disclaimer = "This is not legal advice. Consult a professional.\n"
        rule_ids_disc = {f.rule for f in lint_text(disclaimer, mode="prose")}
        self.assertIn("G003", rule_ids_disc)


if __name__ == "__main__":
    unittest.main()
