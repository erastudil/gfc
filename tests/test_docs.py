# SPDX-License-Identifier: AGPL-3.0-or-later
from __future__ import annotations

import sys
import unittest
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from gfc.lint import lint_text
from gfc.prompt import repo_root

_DOCS = [
    "docs/SPEC.md",
    "docs/IMPLEMENTATION.md",
    "docs/BOUNDARY.md",
    "prompts/genome.md",
    "prompts/canon.md",
    "README.md",
    "AGENTS.md",
    "COVENANT.md",
    "examples/clear.md",
    "skills/gfc/SKILL.md",
]


class DocsLint(unittest.TestCase):
    def test_tree_is_clean(self) -> None:
        root = repo_root()
        for rel in _DOCS:
            findings = lint_text((root / rel).read_text(encoding="utf-8"), mode="prose")
            self.assertEqual(findings, [], msg=f"{rel}: {findings}")


if __name__ == "__main__":
    unittest.main()
