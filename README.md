# gfc

You asked for a retry limit of three. The model titled the page *Retry Limit of Three*, listed the things it would skip, added a footnote about advice, and asked what you wanted next. You already knew the request. The tokens billed anyway.

Richard Feynman named the scientific version of this hole **cargo cult science**: the airstrip is perfect and no plane lands. Agent prose has the same shape. The form of helpfulness, without the thing the human needed to understand.

Brian Greene's popular physics, and Feynman's lectures, land the plane the other way. First the reader sees the mechanism in words they already have. Spacetime as a loaf of bread, sliced into nows. Then the name arrives, and it feels like recognition: *oh, that's what that's called.*

**Greene Feynman Clarity** (GFC) is that order, written as a standard for agents producing prose a human will read. This repository is the specification, drop-in prompts, an agent skill, and tooling that runs on the Python standard library. License is **AGPL-3.0-or-later**. `LICENSE` · `COVENANT.md`.

## start

```
python -m unittest discover -s tests -v
python -m gfc prompt genome
python -m gfc lint examples/slop.md
python -m gfc strip examples/slop.md
python -m gfc echo examples/echo_a.md --corpus examples
```

From the repo, no install:

```
# unix
PYTHONPATH=src python -m gfc check

# powershell
$env:PYTHONPATH = "src"
python -m gfc check
```

Install:

```
python -m pip install -e .
gfc check
```

Python 3.10+. stdlib only.

## the is

| move | force |
|---|---|
| **intuition first, name second** | the mechanism in ordinary words. the term arrives as recognition |
| **say the is, once** | one claim. skip by skipping |
| **contained analogy** | a picture that stays in its paragraph, then returns to the thing |
| **match the ask** | length, register, thread |
| **silence over hedge** | unknown points stay off the page. Feynman integrity: report what would make the claim fail, or omit |
| **the artifact is the work** | repeating the request as a heading or a compliance checklist is a second copy |
| **fresh wording** | the same eight-word stretch across two prompts is a fingerprint |

The linter owns the tell-list so the model does not print it. `spec/gfc.v1.json`.

## kin

Word-list slop gates score like a coin flip. [Platitude](https://github.com/vladzima/platitude) measured that (AUC 0.51 against a blind corpus) and built a structural detector with a frontier-model judge (AUC 0.87). GFC agrees: the mush lives in the shape. This gift is the **writing standard** plus **offline gates** plus **cross-prompt echo**. Pair them. Platitude judges rhetorical shape with a model. GFC states the law and catches what a regex can catch at zero API cost, including wording reused across a corpus of prior answers.

[progen](https://github.com/erastudil/progen) is the dialect for agent think and traces. GFC is the standard for prose a stranger will read. An agent may think in progen and publish in GFC.

## tools

```
gfc lint  PATH [--mode prose|educate] [--ask TEXT] [--ask-file FILE] [--corpus DIR] [--json]
gfc echo  FILE --corpus DIR [--n 8]
gfc strip FILE
gfc prompt {genome|canon|warehouse}
gfc check
```

`lint` on a directory walks `.md` `.txt` `.rst`. `educate` adds term-before-mechanism. `--ask` enables prompt regurgitation, heading echo, and thread drift. `--corpus` enables exact-wording reuse.

## read

| file | is |
|---|---|
| [`docs/SPEC.md`](docs/SPEC.md) | the standard. normative |
| [`docs/IMPLEMENTATION.md`](docs/IMPLEMENTATION.md) | desk, skill, CI wiring |
| [`docs/BOUNDARY.md`](docs/BOUNDARY.md) | what this gift is |
| [`prompts/genome.md`](prompts/genome.md) | drop-in system prompt |
| [`skills/gfc/SKILL.md`](skills/gfc/SKILL.md) | when to check, how to fix, when to stop |
| [`examples/rewrite.md`](examples/rewrite.md) | slop → clear, worked |
| [`spec/gfc.v1.json`](spec/gfc.v1.json) | rule ids |

## copyleft

Writing clearly is just writing. Copying this spec, these prompts, or this tooling is AGPL. A hosted modified copy owes its users the source.

Official copy stays $0. No company seat. `COVENANT.md`.

## contribute

`CONTRIBUTING.md`. DCO. tests on every SPEC change. this tree is the standard.
