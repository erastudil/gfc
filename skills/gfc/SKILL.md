---
name: gfc
description: >
  Greene Feynman Clarity: the writing standard for prose a human will read,
  plus its offline linter. Reach for it when a session names gfc, when
  drafting or revising docs, READMEs, essays, UI copy, mail, or lessons, and
  when a draft needs a tell check before it ships. The linter names the
  flagged spans; the writer fixes the spans and keeps the voice.
---

# gfc

Greene Feynman Clarity is an order for explaining: show the mechanism in
ordinary words first, then give the name. A page that performs explanation
without explaining has failed its job. The standard lives in `docs/SPEC.md`.
The tools in this repo check the parts of the standard a machine can check:
thirteen rules, G001 to G013, defined in `spec/gfc.v1.json` and matched by
`src/gfc/patterns.py`.

The linter owns the tell list. Prompts and skills point at the linter and
state the is. A draft gets linted, the flagged spans get fixed, the page
ships.

## when to use

- A session names gfc: `/gfc`, a named gfc request, or a request to lint prose.
- A human-facing page is being drafted or revised: docs, READMEs, essays, UI copy, mail, release notes.
- A lesson, primer, or textbook is in play: educate mode adds the order check.
- An answer was produced from a known prompt: pass the prompt along and catch regurgitation, heading echo, and drift.
- A desk produces many answers over time: run the corpus check and catch wording that repeats across answers.

## setup

Python 3.10 or higher, standard library only, no network.

Install from a checkout:

```
python -m pip install -e .
gfc check
```

`gfc check` runs the fixture suite and lints the gfc tree itself. Exit 0
means the install works and this skill file is clean.

Skip the install and run from the checkout:

```
# powershell
$env:PYTHONPATH = "src"
python -m gfc check

# unix
PYTHONPATH=src python -m gfc check
```

## inputs

| input | shape |
|---|---|
| target | a `.md`, `.txt`, or `.rst` file, or a directory scanned recursively |
| mode | `prose` for ordinary pages, `educate` for lessons and textbooks |
| ask | the original prompt, inline with `--ask` or from a file with `--ask-file` |
| corpus | a directory of prior outputs, used by the echo check |

## commands

```
gfc lint PATH [--mode prose|educate] [--ask TEXT] [--ask-file FILE] [--corpus DIR] [--json]
gfc echo FILE --corpus DIR [--n INT]
gfc strip FILE
gfc prompt {genome|canon|warehouse}
gfc check
```

`lint` prints one line per finding: severity, rule id, file and line, title,
excerpt. A clean file prints `clean`. Exit codes: 0 clean, 1 findings at
error severity, 2 no prose files found. `--json` emits the findings as JSON
for agent toolchains.

`echo` reports exact eight-word stretches the file shares with the corpus.
`--n` changes the stretch length.

`strip` writes a mechanically cleaned copy to stdout. The source file stays
untouched. Strip collapses an empty reversal to its surviving claim, drops
padding sentences, and turns em dashes into commas. Review the output
before anything ships: strip is a first pass, with no judgment about which
sentences carried weight.

`prompt` prints a drop-in system prompt. `genome` carries the writing
order. `canon` carries standing project rules. `warehouse` is a task
template.

## the rules

| id | catches |
|---|---|
| G001 | an empty reversal: two short abstractions swapped for rhythm, with no number, name, or measurement |
| G002 | a will-not list: three or more bullets that only say what the text skips |
| G003 | a disclaimer doing the work of honesty |
| G004 | a six-word stretch of the ask copied into the body |
| G005 | exact wording shared with a prior answer in the corpus |
| G006 | an analogy that escaped its paragraph and became the language of the page |
| G007 | em dash density: a run of dashed sentences, or four or more in a page |
| G008 | a trailing conversational hook on the last line |
| G009 | likeability padding and marketing verbs |
| G010 | a recap closer |
| G011 | educate mode: a section that names the term before the mechanism |
| G012 | drift: a long answer whose content words miss the ask |
| G013 | a heading that restates the ask |

## procedure

1. Draft the page.
2. Run `gfc lint` on it. Add `--mode educate` for lessons. Add `--ask-file` when the prompt is on hand. Add `--corpus` when prior answers exist.
3. Fix each flagged span by hand, guided by the title of the finding. Rewrite the span; keep the rest of the page untouched.
4. Re-lint. Stop when the output reads `clean`, or when the only remaining findings are deliberate voice: a picture the author chose, a contrast that carries a number.
5. For a page with heavy padding, run `gfc strip` once, read the result, and repair from there.

Chasing zero findings on a creative draft flattens the voice. The gate is a
floor. Judgment decides the rest.

## scope

Lint prose: `.md`, `.txt`, `.rst`. Code, configs, logs, and diffs stay out.
Quoted lines and fenced code blocks count as mentions and are skipped. The
checker reads English prose; other languages are out of scope.

## pitfalls

- Linting without `--ask` when the prompt exists: regurgitation, heading echo, and drift stay invisible, because those three rules need the ask.
- Treating strip output as final copy: strip deletes by shape, and a sentence the page needed can match a shape.
- Regenerating the whole page after a lint: findings name spans, and a full rewrite trades known text for new risk.
- Reciting the rule list inside a deliverable: the list lives in the linter, and a page that prints its own fences has missed the point of G002.
- A corpus directory holding near-duplicate drafts of the target page: the drafts echo each other, and the report fills with sibling overlap.

## kin

[progen](https://github.com/erastudil/progen) is the dialect an agent thinks
in. gfc is the order it writes in for a stranger.
[zcabs](https://github.com/erastudil/zcabs) proves execution.
[Platitude](https://github.com/vladzima/platitude) judges rhetorical shape
with a model, for public English pages with a frontier judge on hand. Run
gfc first: gfc is offline, and it catches wording reused across a corpus,
which a single-page judge never sees.
