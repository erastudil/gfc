# SPDX-License-Identifier: AGPL-3.0-or-later
"""masking, tokens, n-grams. code and urls are not prose."""

from __future__ import annotations

import re
from typing import Iterable

STOP = frozenset(
    """
    a an the and or but if then than so as at by for from in into of on onto
    to with without within over under about after before above below between
    this that these those it its itself they them their you your we our i me my
    is are was were be been being do does did doing have has had having
    not no nor only just also too very can could should would may might must
    will shall here there when where why how what which who whom
    up down out off onces once again still already even ever never
    """.split()
)

_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"“\[(])")
_WORD = re.compile(r"[A-Za-z0-9]+(?:['’][A-Za-z]+)?")
_FENCE = re.compile(r"^```")


def mask_fences(source: str) -> str:
    source = _mask_frontmatter(source)
    lines = source.splitlines(True)
    out: list[str] = []
    fence = False
    for line in lines:
        if line.strip().startswith("```"):
            fence = not fence
            out.append("\n" if line.endswith("\n") else "")
            continue
        if fence:
            out.append("\n" if line.endswith("\n") else "")
            continue
        out.append(_mask_inline(line))
    return "".join(out)


def _mask_frontmatter(source: str) -> str:
    if not source.startswith("---"):
        return source
    lines = source.splitlines(True)
    if not lines or lines[0].strip() != "---":
        return source
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "".join("\n" if ln.endswith("\n") else "" for ln in lines[: i + 1]) + "".join(lines[i + 1 :])
    return source


def _mask_inline(line: str) -> str:
    def ticks(m: re.Match) -> str:
        return " " * len(m.group(0))

    line = re.sub(r"`[^`]+`", ticks, line)
    line = re.sub(r"\[[^\]]+\]\([^)]+\)", ticks, line)
    line = re.sub(r"https?://\S+", ticks, line)
    return line


def visible_lines(source: str) -> list[tuple[int, str]]:
    masked = mask_fences(source)
    rows: list[tuple[int, str]] = []
    for i, line in enumerate(masked.splitlines(), start=1):
        rows.append((i, line))
    return rows


def paragraphs(source: str) -> list[tuple[int, str]]:
    """blank-line blocks. line number is the first content line."""
    masked = mask_fences(source)
    blocks: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 1
    for i, line in enumerate(masked.splitlines(), start=1):
        if line.strip():
            if not buf:
                start = i
            buf.append(line)
        else:
            if buf:
                blocks.append((start, "\n".join(buf)))
                buf = []
    if buf:
        blocks.append((start, "\n".join(buf)))
    return blocks


def sentences(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    parts = _SENT.split(text)
    return [p.strip() for p in parts if p.strip()]


def words(text: str) -> list[str]:
    return [m.group(0) for m in _WORD.finditer(text)]


def tokens(text: str) -> list[str]:
    return [w.lower().replace("’", "'") for w in words(text)]


def content_tokens(text: str) -> list[str]:
    return [t for t in tokens(text) if t not in STOP and len(t) > 1]


def ngrams(toks: Iterable[str], n: int) -> list[tuple[str, ...]]:
    seq = list(toks)
    if n <= 0 or len(seq) < n:
        return []
    return [tuple(seq[i : i + n]) for i in range(len(seq) - n + 1)]


def ngram_has_content(gram: tuple[str, ...], need: int = 3) -> bool:
    return sum(1 for t in gram if t not in STOP and len(t) > 1) >= need


def word_count(text: str) -> int:
    return max(1, len(words(mask_fences(text))))


def last_content_line(source: str) -> tuple[int, str] | None:
    last = None
    for i, line in enumerate(mask_fences(source).splitlines(), start=1):
        if line.strip():
            last = (i, line)
    return last


def clip(s: str, n: int = 120) -> str:
    s = s.strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def first_heading(source: str) -> tuple[int, str] | None:
    for i, line in enumerate(source.splitlines(), start=1):
        s = line.strip()
        if s.startswith("#"):
            return i, re.sub(r"^#+\s*", "", s).strip()
    return None


def quote_line(line: str) -> bool:
    s = line.lstrip()
    return s.startswith(">")
