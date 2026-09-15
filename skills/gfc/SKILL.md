---
name: gfc
description: >
  Apply Greene Feynman Clarity to prose a human will read: docs, READMEs,
  essays, UI copy, mail, textbooks. Use after writing or substantially
  editing that prose. Offline linter plus echo detector. Returns named
  spans so the text gets fixed rather than regenerated.
---

# gfc

A human-facing page that performs explanation without explaining has failed. GFC is the order that lands: mechanism in ordinary words, then the name. The linter owns the tell-list. You state the is.

## run

```
gfc lint PATH [--mode prose|educate] [--ask-file ASK] [--corpus history/] [--json]
gfc echo FILE --corpus history/
gfc strip FILE
```

`--mode educate` for textbooks, primers, lessons. `--ask-file` for regurgitation, heading echo, and drift. `--corpus` for wording reused across prior answers.

## fix loop

1. Rewrite only the flagged spans, guided by each finding's title.
2. Re-lint. Unchanged files stay cheap.
3. Stop when the output is `clean`, or when the only remaining hits are deliberate voice.

Chasing zero findings flattens voice. One contained picture in a concrete page is writing.

## order

intuition first, name second. say the is, once. a picture stays in its paragraph. match the ask. unknown points stay off the page.

## skip

code, configs, logs, diffs, non-English. quoted specimens are mentions.

## kin

[Platitude](https://github.com/vladzima/platitude) is a measured model-judge on rhetorical shape. Run GFC first. Add Platitude when a frontier judge is available and the page is public English. [progen](https://github.com/erastudil/progen) is the think-dialect. published prose stays GFC.
