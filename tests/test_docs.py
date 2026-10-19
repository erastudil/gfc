# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

import gfc
from gfc.lint import lint_text
from gfc.prompt import repo_root

_DOCS = [
    "docs/SPEC.md",
    "docs/IMPLEMENTATION.md",
    "docs/BOUNDARY.md",
    "prompts/genome.md",
    "prompts/canon.md",
    "prompts/warehouse.md",
    "README.md",
    "AGENTS.md",
    "COVENANT.md",
    "examples/clear.md",
    "skills/gfc/SKILL.md",
]

_DATA_PARITY = (
    ("spec/gfc.v1.json", "src/gfc/data/gfc.v1.json"),
    ("prompts/genome.md", "src/gfc/data/genome.md"),
    ("prompts/canon.md", "src/gfc/data/canon.md"),
    ("prompts/warehouse.md", "src/gfc/data/warehouse.md"),
)


class DocsLint(unittest.TestCase):
    def test_tree_is_clean(self) -> None:
        root = repo_root()
        for rel in _DOCS:
            findings = lint_text((root / rel).read_text(encoding="utf-8"), mode="prose")
            self.assertEqual(findings, [], msg=f"{rel}: {findings}")

    def test_tensor_attention_educate_clean(self) -> None:
        root = repo_root()
        text = (root / "examples" / "tensor-attention.md").read_text(encoding="utf-8")
        findings = lint_text(text, mode="educate")
        self.assertEqual(findings, [], msg=f"{findings}")

    def test_readme_does_not_clone_gift_skeleton(self) -> None:
        text = (repo_root() / "README.md").read_text(encoding="utf-8")
        lowered = text.lower()
        self.assertIn("examples/tensor-attention.md", lowered)
        self.assertNotIn("\n## start\n", lowered)
        self.assertNotIn("\n## copyleft\n", lowered)
        self.assertNotIn("\n## contribute\n", lowered)

    def test_packaged_data_byte_parity(self) -> None:
        root = repo_root()
        for src_rel, data_rel in _DATA_PARITY:
            src_path = root / src_rel
            data_path = root / data_rel
            self.assertTrue(src_path.is_file(), f"missing {src_rel}")
            self.assertTrue(data_path.is_file(), f"missing {data_rel}")
            self.assertEqual(
                src_path.read_bytes(),
                data_path.read_bytes(),
                f"byte drift between {src_rel} and {data_rel}",
            )

    def test_version_matches_pyproject(self) -> None:
        pyproject = (repo_root() / "pyproject.toml").read_text(encoding="utf-8")
        match = re.search(r'^version\s*=\s*"([^"]+)"', pyproject, flags=re.MULTILINE)
        self.assertIsNotNone(match, "version field missing in pyproject.toml")
        assert match is not None
        self.assertEqual(gfc.__version__, match.group(1))


if __name__ == "__main__":
    unittest.main()
