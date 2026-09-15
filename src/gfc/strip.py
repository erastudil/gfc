# SPDX-License-Identifier: AGPL-3.0-or-later
"""mechanical pass toward the is. does not invent a voice."""

from __future__ import annotations

import re

from . import patterns, text

_SENT_SPLIT = re.compile(r"(?<=[!?])\s+|(?<=\.)\s+(?=[A-Z\"“\[])")


def strip_text(source: str) -> str:
    out: list[str] = []
    fence = False
    for raw in source.splitlines():
        stripped = raw.strip()
        if stripped.startswith("```"):
            fence = not fence
            out.append(raw.rstrip())
            continue
        if fence:
            out.append(raw.rstrip())
            continue
        if not stripped:
            if out and out[-1] != "":
                out.append("")
            continue
        if stripped.startswith("#") or stripped.startswith("|"):
            out.append(raw.rstrip())
            continue
        stripped = _positive(stripped)
        pieces = _SENT_SPLIT.split(stripped)
        kept: list[str] = []
        for piece in pieces:
            piece = piece.strip()
            if not piece:
                continue
            if _drop(piece):
                continue
            piece = _dashes(piece)
            piece = _tidy(piece)
            if piece:
                kept.append(piece)
        if kept:
            out.append(" ".join(kept))
    while out and out[-1] == "":
        out.pop()
    return "\n".join(out) + ("\n" if source.endswith("\n") or out else "")


def _drop(s: str) -> bool:
    if patterns.MUSH.search(s) or patterns.AS_AI.search(s) or patterns.DISCLAIMER.search(s):
        return True
    if patterns.RECAP.search(s) or patterns.MARKETING.search(s) or patterns.ROBUST.search(s):
        return True
    if patterns.HOOK.search(s) or patterns.HOOK_END.search(s):
        return True
    return False


def _positive(s: str) -> str:
    m = patterns.SIDES.search(s)
    if not m:
        return s
    y = m.group(2).strip().rstrip(".")
    if not y:
        return s
    if y[0].islower():
        y = y[0].upper() + y[1:]
    if not y.endswith((".", "!", "?")):
        y = y + "."
    return y


def _dashes(s: str) -> str:
    s = patterns.EMDASH.sub(", ", s)
    s = re.sub(r"\s+,", ",", s)
    s = re.sub(r",\s*,", ",", s)
    return s


def _tidy(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.])", r"\1", s)
    return s
