# contributing

patches keep the gift intact.

## license

AGPL-3.0-or-later. you certify the patch is yours to give under that license.

Developer Certificate of Origin. append to each commit message:

```
Signed-off-by: Name <email>
```

No CLA. copyright stays with the authors. the project does not take assignment.

PRs that relicense, dual-license, or add a company CLA are rejected.

## tests

```
python -m unittest discover -s tests -v
PYTHONPATH=src python -m gfc check
```

SPEC changes need a fixture. a new lint rule needs a fail case and a pass case. word-list verdicts stay off this gift: add a shape, or add a measurement.

## voice

normative text is GFC. README teaches in ordinary english first, then names the term.

this tree is the standard. `docs/BOUNDARY.md`.
