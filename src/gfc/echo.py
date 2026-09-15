# SPDX-License-Identifier: AGPL-3.0-or-later
"""exact wording reused across prompts. humans vary. models loop."""

from __future__ import annotations

from dataclasses import dataclass

from . import text

# legal and boilerplate stretches that every file in this line may share
_ALLOW = {
    ("gnu", "affero", "general", "public", "license"),
    ("agpl", "3", "0", "or", "later"),
    ("spdx", "license", "identifier", "agpl", "3"),
    ("this", "program", "comes", "with", "absolutely", "no", "warranty"),
    ("python", "3", "10", "standard", "library", "only"),
    ("signed", "off", "by"),
}


@dataclass(frozen=True)
class EchoHit:
    ngram: tuple[str, ...]
    other: str
    excerpt: str


def echo_ngrams(source: str, n: int = 8) -> set[tuple[str, ...]]:
    toks = text.tokens(text.mask_fences(source))
    out: set[tuple[str, ...]] = set()
    for gram in text.ngrams(toks, n):
        if not text.ngram_has_content(gram, need=3):
            continue
        if _allowed(gram):
            continue
        out.add(gram)
    return out


def echo_hits(
    source: str,
    corpus: list[tuple[str, str]],
    n: int = 8,
) -> list[EchoHit]:
    mine = echo_ngrams(source, n=n)
    if not mine:
        return []
    found: list[EchoHit] = []
    seen: set[tuple[str, ...]] = set()
    for label, other in corpus:
        other_grams = echo_ngrams(other, n=n)
        overlap = mine & other_grams
        for gram in sorted(overlap):
            if gram in seen:
                continue
            seen.add(gram)
            found.append(
                EchoHit(
                    ngram=gram,
                    other=label,
                    excerpt=" ".join(gram),
                )
            )
    return found


def _allowed(gram: tuple[str, ...]) -> bool:
    joined = " ".join(gram)
    for span in _ALLOW:
        needle = " ".join(span)
        if needle in joined:
            return True
    return False
