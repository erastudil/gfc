---
title: "gfc — implementation"
version: "1.0.0"
status: normative-adjacent · reference implementation
license: AGPL-3.0-or-later
---

# implementation

SPEC is the standard. this file is the wiring.

Python 3.10+, standard library only.

```
python -m pip install -e .
gfc lint docs --mode educate
gfc echo draft.md --corpus history/
gfc strip draft.md
gfc prompt genome
```

Checkout without install:

```
# unix
PYTHONPATH=src python -m gfc check

# powershell
$env:PYTHONPATH = "src"
python -m gfc check
```

---

## 1. why this shape

an agent writing for a human is trained to be likeable, long, and finished-looking. that training fights the job. the human needed the mechanism, then the name.

gfc is the counterweight:

- a short genome that states the is
- a linter that owns the tell-list
- an echo detector for wording reused across prompts
- `gfc strip` for a mechanical pass
- a skill that says when to stop polishing

start at the genome. a fourth prompt stack of "don't do X" is the hole this gift exists to close.

---

## 2. load order

every automated turn that will publish prose:

1. **genome**: `gfc prompt genome` plus your tool list
2. **named source**: the page the prose is about
3. **write**
4. **lint**: `gfc lint FILE --ask-file ASK [--corpus history/] [--mode educate]`
5. **fix the named spans**. re-lint. stop when clean, or when the only remaining hits are deliberate voice

the skill file is the same loop in agent-readable form.

---

## 3. genome states the is

effort sliders control volume. the standard stays.

bans live in `spec/gfc.v1.json` and `src/gfc/patterns.py`. the model does not print them. quoting the instruction is a second copy.

---

## 4. coding agent

drop in the skill:

```
cp -r skills/gfc ~/.codex/skills/     # or ~/.claude/skills or .grok/skills
```

or paste `prompts/genome.md` into the system prompt and expose the CLI as a tool:

| tool | args | returns |
|---|---|---|
| `gfc_lint` | path, mode, ask, corpus | findings or `clean` |
| `gfc_echo` | file, corpus | shared n-grams or `clean` |
| `gfc_strip` | file | rewritten text |

typical loop: draft → lint with the ask → edit the named lines → lint again. full regeneration swaps one tell for another.

`--json` is the machine form.

---

## 5. CI

```yaml
- name: gfc
  uses: erastudil/gfc/action@v1
  with:
    path: docs
    mode: educate
```

or:

```
PYTHONPATH=src python -m gfc lint docs --mode prose
```

lint the human pages. leave `CHANGELOG`, lockfiles, and generated API dumps off the path.

---

## 6. educate vs prose

README, essays, UI copy, mail: `--mode prose`.

textbooks, primers, lessons, onboarding that teaches a term: `--mode educate`.

the specification in this repo is a standard, so it names terms early on purpose. `gfc check` lints it in prose mode.

---

## 7. corpus for echo

keep prior published answers in a directory. pass it as `--corpus`. the current file is skipped when linting a path inside that directory.

eight content-bearing tokens is the default stretch. legal boilerplate is allowed.

---

## 8. pair with platitude

when a frontier judge is available and the page is public-facing English:

1. `gfc lint` offline, fix the named spans
2. `platitude --file draft.md` for rhetorical shape the regex will miss
3. stop when both are clean, or when remaining hits are voice

gfc does not call a model. platitude does. they share the claim that slop is structure.

---

## 9. pair with progen

think and traces: progen. published prose: gfc. keep the dialect marks off the page the stranger reads. `progen iron` is for topic-comment. `gfc strip` is for the is in ordinary english.

---

## 10. holes takeable later

| hole | note |
|---|---|
| JS port | python is the reference. a second runtime is a later gift |
| MCP stdio | the CLI `--json` is enough for v1 |
| trained FTPO | [Antislop](https://github.com/sam-paech/auto-antislop) is that job |
| non-English | SPEC is English. other tongues need their own corpus |

patches that add torch, spaCy, or an API key as a required path are off this gift.
