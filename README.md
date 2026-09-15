# gfc

You already know what a good explanation feels like. Halfway through a hard page you see the machine. Then the author gives the thing a name, and the name sticks because it labels a picture you already have.

Most pages an agent writes run that order backwards. A term, then a decoding of the term, then a paragraph of what the term is not, then a question about whether you want more. You leave able to repeat the label. You cannot see the machine.

Greene's popular physics and Feynman's lectures go the first way. Mechanism in words you already have. Name as recognition: *oh, that's what that's called.*

This repository is that order, written down for agents producing prose a human will read, plus offline tooling that catches the backwards page. The license is AGPL-3.0-or-later.

The cooked meal is [examples/tensor-attention.md](examples/tensor-attention.md). It teaches the mix that lets every word in a line look at every other word, and only then names tensors, heads, `QK^T`, and the KV cache. Read that. This file is the kitchen.

## What the tools catch

A linter cannot tell whether a page is true. It can tell when a page is doing the backwards dance.

Empty reversal: two short abstractions swapped for rhythm, no number, no name, no measurement. `It's not a tool. It's a teammate.`

A heading that restates the prompt. A six-word stretch of the ask copied into the body. The same eight words in two answers to two prompts. An analogy that escapes its paragraph and becomes the language of the rest of the page. A section that defines the term before anyone has seen the mechanism. A disclaimer costume. A trailing hook that prompts the human for the next token. A run of em dashes doing the work of choosing a period.

The rule definitions live in [`spec/gfc.v1.json`](spec/gfc.v1.json) and [`src/gfc/patterns.py`](src/gfc/patterns.py). Outputs state the is. They do not print the list.

Word-list slop gates score like a coin flip. [Platitude](https://github.com/vladzima/platitude) measured that and built a model-judge on rhetorical shape. Use it when you have a frontier judge and a public English page. This repository stays offline, standard library only, and catches wording reused across a corpus of prior answers, which a single-page judge never sees.

[progen](https://github.com/erastudil/progen) is how an agent thinks. This is how it writes for a stranger. [zcabs](https://github.com/erastudil/zcabs) is how it proves execution.

## Installation and verification

Python 3.10 or higher. No external dependencies.

```bash
# install in editable mode
python -m pip install -e .

# verify installation and test suite
gfc check
```

Directly from a checkout without installation:

```bash
# unix
PYTHONPATH=src python -m gfc check

# powershell
$env:PYTHONPATH = "src"
python -m gfc check
```

## Command reference

The CLI provides five commands:

```bash
gfc lint   PATH [--mode prose|educate] [--ask TEXT] [--ask-file FILE] [--corpus DIR] [--json]
gfc echo   FILE --corpus DIR [--n INT]
gfc strip  FILE
gfc prompt {genome|canon|warehouse}
gfc check
```

### `gfc lint`

Scans files or directories for structural prose failure modes:

```bash
# standard prose check on human-facing documentation
gfc lint docs/

# educational mode for lessons, checking that mechanisms precede terms
gfc lint examples/tensor-attention.md --mode educate

# check for prompt regurgitation and topical drift against the original user prompt
gfc lint output.md --ask "Why did the worker process fail at 02:00?"

# machine-readable JSON output for agent toolchains
gfc lint output.md --json
```

### `gfc echo`

Detects exact n-grams shared across a corpus of previous outputs. Prevents an agent from repeating pet phrases across independent sessions:

```bash
gfc echo current_draft.md --corpus history/ --n 8
```

### `gfc strip`

Performs an automated pass that collapses empty reversals to their surviving claim and strips likeability padding, disclaimers, and trailing hooks:

```bash
gfc strip examples/slop.md
```

### `gfc prompt`

Emits ready-to-use system prompts directly to stdout:

```bash
# core agent writing genome
gfc prompt genome

# standing project canon
gfc prompt canon

# warehouse task template
gfc prompt warehouse
```

## Integration into agent workflows

Agent systems can adopt GFC at three levels:

1. **System Prompt**: Drop [`prompts/genome.md`](prompts/genome.md) into your agent system prompt or model card. It instructs the model to lead with intuition, say the is once, and drop conversational mush.
2. **Skill / Tool**: Place [`skills/gfc/SKILL.md`](skills/gfc/SKILL.md) into your agent skill directory, exposing `gfc lint`, `gfc echo`, and `gfc strip` as tools. The agent drafts, lints, repairs flagged line numbers, and returns clean prose.
3. **Continuous Integration**: Add [`action/action.yml`](action/action.yml) to your repository workflows to lint documentation and educational guides on every pull request.

The formal specification is [`docs/SPEC.md`](docs/SPEC.md). Implementation architecture is documented in [`docs/IMPLEMENTATION.md`](docs/IMPLEMENTATION.md). Repository boundaries are defined in [`docs/BOUNDARY.md`](docs/BOUNDARY.md).

## Philosophy in practice

A picture earns one paragraph. Then the page returns to the thing. Chasing zero findings on creative drafts flattens voice. Stop when the page is clean, or when the remaining hits represent intentional choices.

Writing in this standard is just writing. Copying the specification, the prompts, or the tooling into a modified work is governed by AGPL-3.0-or-later. A hosted modified service owes its users corresponding source. See `LICENSE` and `COVENANT.md`.
