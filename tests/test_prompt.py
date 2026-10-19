# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import load_rules
from gfc.prompt import load_prompt, repo_root


class Prompts(unittest.TestCase):
    def test_genome_states_the_is(self) -> None:
        text = load_prompt("genome")
        for token in ("intuition first", "gfc lint", "ERROR", "DONT_KNOW"):
            self.assertIn(token, text)

    def test_canon_points_at_linter(self) -> None:
        text = load_prompt("canon")
        self.assertIn("gfc lint", text)
        self.assertIn("AGPL", text)

    def test_warehouse_names_spec(self) -> None:
        text = load_prompt("warehouse")
        self.assertIn("docs/SPEC.md", text)

    def test_unknown_prompt(self) -> None:
        with self.assertRaises(ValueError):
            load_prompt("house-pools")

    def test_machine_spec_matches_lint_ids(self) -> None:
        spec = json.loads((repo_root() / "spec" / "gfc.v1.json").read_text(encoding="utf-8"))
        ids = {r["id"] for r in spec["lint_rules"]}
        self.assertEqual(
            ids,
            {
                "G001",
                "G002",
                "G003",
                "G004",
                "G005",
                "G006",
                "G007",
                "G008",
                "G009",
                "G010",
                "G011",
                "G012",
                "G013",
            },
        )

    def test_packaged_data_fallback_without_repo_root(self) -> None:
        missing_root = repo_root() / "__nonexistent_wheel_root__"
        with patch("gfc.prompt.repo_root", return_value=missing_root):
            for name in ("genome", "canon", "warehouse"):
                self.assertTrue(load_prompt(name).strip())
        with patch("gfc.lint.repo_root", return_value=missing_root):
            rules = load_rules()
            self.assertEqual(len(rules), 13)

    def test_license_files_exist(self) -> None:
        root = repo_root()
        for name in ("LICENSE", "COVENANT.md", "COPYRIGHT", "docs/SPEC.md"):
            self.assertTrue((root / name).is_file(), name)


if __name__ == "__main__":
    unittest.main()
