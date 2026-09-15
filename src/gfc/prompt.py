# SPDX-License-Identifier: AGPL-3.0-or-later
"""emit drop-in prompts from this tree."""

from __future__ import annotations

from pathlib import Path

_NAMES = {
    "genome": "prompts/genome.md",
    "canon": "prompts/canon.md",
    "warehouse": "prompts/warehouse.md",
}

_DATA_DIR = Path(__file__).resolve().parent / "data"


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_prompt(name: str) -> str:
    key = name.strip().lower()
    if key not in _NAMES:
        known = ", ".join(sorted(_NAMES))
        raise ValueError(f"unknown prompt {name!r}. known: {known}")
    candidate = repo_root() / _NAMES[key]
    if candidate.is_file():
        return candidate.read_text(encoding="utf-8")
    data_candidate = _DATA_DIR / f"{key}.md"
    if data_candidate.is_file():
        return data_candidate.read_text(encoding="utf-8")
    raise FileNotFoundError(f"prompt {key!r} not found at {candidate} or {data_candidate}")
