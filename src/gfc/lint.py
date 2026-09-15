# SPDX-License-Identifier: AGPL-3.0-or-later
"""GFC linter. owns the tell-list so agents state the is."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from pathlib import Path
from typing import Iterable, Optional

from . import echo, patterns, text
from .prompt import repo_root


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    line: int
    excerpt: str
    title: str


def load_rules() -> list[dict]:
    path = repo_root() / "spec" / "gfc.v1.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return list(data["lint_rules"])


def lint_text(
    source: str,
    *,
    mode: str = "prose",
    ask: Optional[str] = None,
    corpus: Optional[list[tuple[str, str]]] = None,
) -> list[Finding]:
    findings: list[Finding] = []
    rules = {r["id"]: r for r in load_rules()}
    visible = text.mask_fences(source)
    lines = visible.splitlines()

    def add(rule_id: str, line: int, excerpt: str) -> None:
        meta = rules[rule_id]
        findings.append(
            Finding(
                rule=rule_id,
                severity=meta["severity"],
                line=line,
                excerpt=text.clip(excerpt),
                title=meta["title"],
            )
        )

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if text.quote_line(line):
            continue
        check = stripped.strip("|") if stripped.startswith("|") else stripped
        if patterns.MUSH.search(check) or patterns.AS_AI.search(check):
            add("G009", i, stripped)
        if patterns.DISCLAIMER.search(check):
            add("G003", i, stripped)
        if patterns.MARKETING.search(check) or patterns.ROBUST.search(check):
            add("G009", i, stripped)
        if patterns.RECAP.search(check):
            add("G010", i, stripped)
        if _reversal_empty(check):
            add("G001", i, stripped)

    last = text.last_content_line(visible)
    if last and last[1].rstrip().endswith("?"):
        blob = last[1]
        if patterns.HOOK.search(blob) or patterns.HOOK_END.search(blob):
            add("G008", last[0], blob)

    _will_not(lines, add)
    _emdash(visible, add)
    _latch(visible, add)
    if mode == "educate":
        _order(source, add)
    if ask:
        _regurgitate(source, ask, add)
        _heading(source, ask, add)
        _drift(source, ask, add)
    if corpus:
        _echo(source, corpus, add)
    return findings


def _reversal_empty(line: str) -> bool:
    hit = (
        patterns.REVERSAL.search(line)
        or patterns.REVERSAL_NOT_A.search(line)
        or patterns.REVERSAL_PROBLEM.search(line)
        or patterns.REVERSAL_QUESTION.search(line)
        or patterns.REVERSAL_NOT_JUST.search(line)
    )
    if not hit:
        return False
    span = hit.group(0)
    sides = patterns.SIDES.search(span) or patterns.SIDES.search(line)
    if not sides:
        # "the question isn't" has no Y yet. still the shape.
        return True
    x, y = sides.group(1), sides.group(2)
    if _concrete(x) or _concrete(y):
        return False
    if len(text.words(x)) > 8 or len(text.words(y)) > 8:
        return False
    return True


def _concrete(side: str) -> bool:
    if re.search(r"\d", side):
        return True
    if re.search(r"[\"“”'].{1,48}[\"“”']", side):
        return True
    words = text.words(side)
    for w in words[1:]:
        if w[:1].isupper() and w.lower() not in {"i", "a"}:
            return True
    return False


def _will_not(lines: list[str], add) -> None:
    run = 0
    start = 1
    excerpt = ""
    for i, line in enumerate(lines, start=1):
        s = line.strip()
        if patterns.WILL_NOT_BULLET.match(s):
            if run == 0:
                start = i
                excerpt = s
            run += 1
        else:
            if run >= 3:
                add("G002", start, excerpt)
            run = 0
    if run >= 3:
        add("G002", start, excerpt)


def _emdash(visible: str, add) -> None:
    count = 0
    first_line = 1
    consec = 0
    consec_start = 1
    for i, line in enumerate(visible.splitlines(), start=1):
        n = len(patterns.EMDASH.findall(line))
        if n:
            if count == 0:
                first_line = i
            count += n
            if consec == 0:
                consec_start = i
            consec += 1
            if consec >= 3:
                add("G007", consec_start, line.strip() or "em dash run")
                consec = 0
        else:
            if line.strip():
                consec = 0
    if count >= 4:
        add("G007", first_line, f"em dash x{count}")
        return
    wc = text.word_count(visible)
    density = count * 100 / wc
    if count >= 3 and density >= 2.0:
        add("G007", first_line, f"em dash density {density:.1f}/100w")


def _latch(visible: str, add) -> None:
    title_toks = set(text.content_tokens(_title(visible)))
    paras = text.paragraphs(visible)
    if not paras:
        return
    # first analogy in each paragraph is the container for those vehicles
    for start, block in paras:
        for m in patterns.ANALOGY.finditer(block):
            vehicle = m.group(1).strip().lower()
            heads = [t for t in text.content_tokens(vehicle) if len(t) > 2]
            if not heads:
                continue
            for head in heads:
                if head in title_toks:
                    continue
                outside = 0
                for pstart, pblock in paras:
                    if pstart == start:
                        continue
                    outside += len(re.findall(r"\b" + re.escape(head) + r"\b", pblock.lower()))
                if outside >= 3:
                    add("G006", start, f"analogy {head} x{outside} outside container")
                    return


def _title(visible: str) -> str:
    for line in visible.splitlines():
        s = line.strip()
        if s.startswith("#"):
            return re.sub(r"^#+\s*", "", s)
    return ""


def _order(source: str, add) -> None:
    """first prose sentence of a heading section names the term before the mechanism."""
    lines = source.splitlines()
    section_start = 1
    buf: list[tuple[int, str]] = []

    def flush() -> None:
        nonlocal buf
        prose = [(i, ln) for i, ln in buf if ln.strip() and not ln.strip().startswith("#")]
        prose = [(i, ln) for i, ln in prose if not ln.strip().startswith("|")]
        prose = [(i, ln) for i, ln in prose if not ln.strip().startswith(">")]
        prose = [(i, ln) for i, ln in prose if not ln.strip().startswith("-") and not ln.strip().startswith("*")]
        if not prose:
            buf = []
            return
        first_i, first = prose[0]
        sentence = text.sentences(first.strip()) 
        lead = sentence[0] if sentence else first.strip()
        if patterns.TERM_INTRO.search(lead):
            add("G011", first_i, lead)
        buf = []

    for i, line in enumerate(lines, start=1):
        if line.strip().startswith("#") and i != 1:
            flush()
            section_start = i
            buf = [(i, line)]
            continue
        buf.append((i, line))
    flush()
    _ = section_start


def _regurgitate(source: str, ask: str, add) -> None:
    ask_grams = set(text.ngrams(text.tokens(ask), 6))
    ask_grams = {g for g in ask_grams if text.ngram_has_content(g, need=3)}
    if not ask_grams:
        return
    for i, line in enumerate(text.mask_fences(source).splitlines(), start=1):
        if not line.strip() or text.quote_line(line) or line.strip().startswith("#"):
            continue
        grams = set(text.ngrams(text.tokens(line), 6))
        hit = ask_grams & grams
        if hit:
            gram = sorted(hit)[0]
            add("G004", i, " ".join(gram))
            return


def _heading(source: str, ask: str, add) -> None:
    heading = text.first_heading(source)
    if not heading:
        return
    line_no, title = heading
    ask_c = set(text.content_tokens(ask))
    title_c = text.content_tokens(title)
    if not ask_c or not title_c:
        return
    shared = [t for t in title_c if t in ask_c]
    if len(title_c) >= 4 and len(shared) / len(title_c) >= 0.7:
        add("G013", line_no, title)
        return
    # near-copy of the whole ask
    if text.tokens(title) == text.tokens(ask):
        add("G013", line_no, title)


def _drift(source: str, ask: str, add) -> None:
    ask_c = text.content_tokens(ask)
    if len(ask_c) < 4:
        return
    if text.word_count(source) < 80:
        return
    body_c = text.content_tokens(text.mask_fences(source))
    shared = set(ask_c) & set(body_c)
    if len(shared) / len(set(ask_c)) < 0.2:
        add("G012", 1, f"ask overlap {len(shared)}/{len(set(ask_c))}")


def _echo(source: str, corpus: list[tuple[str, str]], add) -> None:
    hits = echo.echo_hits(source, corpus, n=8)
    if not hits:
        return
    add("G005", 1, f"{hits[0].excerpt} also in {hits[0].other}")


def format_findings(findings: Iterable[Finding], path: str = "") -> str:
    rows = list(findings)
    if not rows:
        return "clean"
    parts = []
    for f in rows:
        loc = f"{path}:{f.line}" if path else f"line {f.line}"
        parts.append(f"{f.severity}:{f.rule} {loc} {f.title}: {f.excerpt}")
    return "\n".join(parts)
