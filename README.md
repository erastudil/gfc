# gfc

You already know what a good explanation feels like. Halfway through a hard page you see the machine. Then the author gives the thing a name, and the name sticks because it labels a picture you already have.

Most pages an agent writes run that order backwards. A term, then a decoding of the term, then a paragraph of what the term is not, then a question about whether you want more. You leave able to repeat the label. You cannot see the machine.

Greene's popular physics and Feynman's lectures go the first way. Mechanism in words you already have. Name as recognition: *oh, that's what that's called.*

This repository is that order, written down for agents that produce prose a human will read, plus tools that catch the backwards page. The license is AGPL-3.0-or-later.

The cooked meal is [examples/tensor-attention.md](examples/tensor-attention.md). It teaches the mix that lets every word in a line look at every other word, and only then names tensors, heads, `QK^T`, and the KV cache. Read that. This file is the kitchen.

## What the tools catch

A linter cannot tell whether a page is true. It can tell when a page is doing the backwards dance.

Empty reversal: two short abstractions swapped for rhythm, no number, no name, no measurement. `It's not a tool. It's a teammate.`

A heading that restates the prompt. A six-word stretch of the ask copied into the body. The same eight words in two answers to two prompts. An analogy that escapes its paragraph and becomes the language of the rest of the page. A section that defines the term before anyone has seen the mechanism. A disclaimer costume. A trailing hook that prompts the human for the next token. A run of em dashes doing the work of choosing a period.

The list lives in [`spec/gfc.v1.json`](spec/gfc.v1.json) and [`src/gfc/patterns.py`](src/gfc/patterns.py). Outputs state the is. They do not print the list.

Word-list slop gates score like a coin flip. [Platitude](https://github.com/vladzima/platitude) measured that and built a model-judge on rhetorical shape. Use it when you have a frontier judge and a public English page. This repo stays offline, stdlib only, and also catches wording reused across a corpus of prior answers, which a single-page judge never sees.

[progen](https://github.com/erastudil/progen) is how an agent thinks. This is how it writes for a stranger.

## Run

Python 3.10+. No third-party packages.

```
python -m pip install -e .
gfc lint examples/tensor-attention.md --mode educate
gfc lint examples/slop.md
gfc strip examples/slop.md
gfc echo examples/echo_a.md --corpus examples
gfc prompt genome
gfc check
```

From a checkout, no install:

```
# unix
PYTHONPATH=src python -m gfc check

# powershell
$env:PYTHONPATH = "src"
python -m gfc check
```

```
gfc lint  PATH [--mode prose|educate] [--ask TEXT] [--ask-file FILE] [--corpus DIR] [--json]
gfc echo  FILE --corpus DIR
gfc strip FILE
gfc prompt {genome|canon|warehouse}
gfc check
```

`--mode educate` is for lessons and primers. It flags a section that names the term before the mechanism. `--ask` catches regurgitation and drift. `--corpus` catches echo.

Drop [`prompts/genome.md`](prompts/genome.md) into a system prompt. Drop [`skills/gfc/SKILL.md`](skills/gfc/SKILL.md) into a skill slot. Wire CI with [`action/action.yml`](action/action.yml). The law is [`docs/SPEC.md`](docs/SPEC.md). Desk wiring is [`docs/IMPLEMENTATION.md`](docs/IMPLEMENTATION.md). Scope is [`docs/BOUNDARY.md`](docs/BOUNDARY.md).

A picture earns one paragraph. Then the page returns to the thing. Chasing zero findings flattens voice. Stop when the page is clean, or when the remaining hits are deliberate.

Writing this way is just writing. Copying the spec, the prompts, or the tools is AGPL. A hosted modified copy owes its users the source. Official copy stays $0. `LICENSE` · `COVENANT.md` · `CONTRIBUTING.md`.
