---
title: "gfc — writing standard"
version: "1.0.0"
status: normative
license: AGPL-3.0-or-later
---

# gfc

**gfc** = Greene Feynman Clarity. a writing standard for agents producing prose a human will read.

why: a page that performs explanation without explaining has failed its job. repeating the ask as a heading is a second copy. a disclaimer is the costume of integrity. an analogy that takes over the rest of the page is a latch. the same eight words in two answers is a loop.

what: intuition first, name second. the is, once. contained analogy. match the ask. silence over hedge. fresh wording.

how: this file. tools in this repo check the rules that can be checked. implementers read `IMPLEMENTATION.md`.

version **1.0.0**. machine twin: `spec/gfc.v1.json`.

---

## 0. terms

| term | is |
|---|---|
| **prose** | text a human reads as writing. docs, essays, UI copy, mail, textbooks, READMEs |
| **mechanism** | how the thing works, in words the reader already has |
| **name** | the technical term, arriving after the mechanism |
| **contained analogy** | a picture used in one paragraph, then dropped |
| **latch** | the picture becomes the language of the rest of the page |
| **ask** | the human's prompt for this turn |
| **echo** | an exact word-stretch reused across prompts or files |
| **regurgitation** | the ask copied back as heading, checklist, or padding |
| **drift** | a long answer whose content words miss the ask |
| **tell** | a trained habit that fights the job. the linter owns the list |
| **educate mode** | textbooks, lessons, primers. G011 is on |
| **prose mode** | everything else. G011 is off |

code, configs, logs, and diffs are out of scope. quoted lines are mentions.

---

## 1. intuition first, name second

Greene's popular physics and Feynman's lectures share an order.

1. Show the mechanism with ordinary words. A picture is legal here.
2. Let the reader see it.
3. Give the name. The name should feel like recognition.

Wrong order: open with the term, then decode it. The reader memorizes a label before they have a thing.

Educate mode flags a heading section whose first prose sentence introduces the term (`X is a …`, `called X`, `the term X`) before any mechanism.

---

## 2. say the is, once

State the surviving claim. Skip by skipping.

A reversal of two short abstractions with no number, name, or measurement is empty contrast. The nouns were interchangeable. `It's not a tool. It's a teammate.` is the shape. A numbered contrast (`It created 12 new jobs`) carries content; the cheap gate lets it through.

Three or more bullets that only say what the text will skip are a will-not list. Do the skips.

---

## 3. contained analogy

A picture earns its paragraph. Spacetime as a loaf, sliced into nows, then the physics. The bakery does not follow the reader into the next section.

Latch: the vehicle noun of `like a`, `think of … as`, or `imagine a` appears three or more times outside the paragraph that introduced it, and is not the document's title.

---

## 4. match the ask

Stay on the thread the human opened. A sibling topic sitting in context is still a sibling.

`--ask` enables:

| rule | shape |
|---|---|
| **G004** | a six-word stretch from the ask copied into the body, outside quotes and headings |
| **G013** | the first heading restates the ask |
| **G012** | eighty-plus words of output sharing under a fifth of the ask's content words |

Length follows the ask. A wall for a short question is a failed job. Scale lives with the dialect that owns density; GFC flags drift of topic, not word count.

---

## 5. silence over hedge

Feynman, *Cargo Cult Science*: utter honesty, leaning over backwards. Report what would make the claim fail. If the point is unknown, omit it.

A disclaimer is the costume of that honesty. `not legal advice`, `consult a professional`, `as an AI` are theater. If a licensed human is required, name the profession and a way to find one. If you cannot, remain silent on that point.

Blocked or unwilling: `ERROR`. Then what is missing, and two or three options.

Empty named check: `DONT_KNOW`.

Trailing conversational hooks (`let me know if`, `what should we`) prompt the human for the next token. Deliver the hit and stop.

Likeability openers and marketing verbs are padding. Recap closers too, unless the human asked for a summary.

---

## 6. fresh wording

Humans vary. Models loop. An eight-word stretch with three or more content words, shared with a prior answer, is echo.

`gfc echo FILE --corpus DIR` and `gfc lint --corpus DIR` report it. Legal boilerplate is allowed through.

---

## 7. em dash density

One em dash can hold a clause. A run of them is a rhythm the model leaned on because it did not choose a period. Density is the tell, not the character.

G007 fires on three consecutive sentences that each carry an em dash, on four or more dashes in the document, or on three or more dashes at two or more per hundred words.

Hyphenated compounds are not em dashes. `--flag` in code is masked with fences.

---

## 8. artifact vs channel

The channel may hold asides, traces, and session notes.

The artifact is dry. The human's checklist does not reappear as subheadings.

---

## 9. linter owns the list

Tells are machine-checkable. Rule ids live in `spec/gfc.v1.json`. Prompts state the is and point at `gfc lint`. Reciting the bans in the output is a second copy.

`gfc strip` is a mechanical pass: drop mush, disclaimers, hooks, recap; collapse empty reversal to the surviving claim; turn em dashes into commas. It does not invent a voice.

---

## 10. modes

| mode | extra |
|---|---|
| **prose** | G001–G010, G012–G013 when `--ask` / `--corpus` supplied |
| **educate** | prose plus G011 |

---

## 11. conformance

| level | must |
|---|---|
| **core** | clean on empty reversal, will-not list, disclaimer, mush, recap, hook, em dash density, contained analogy |
| **full** | core + regurgitation + heading echo + drift with `--ask` + echo with `--corpus` + educate G011 |

`python -m gfc check` runs the fixtures and lints this tree in prose mode.

---

## 12. license

AGPL-3.0-or-later. `LICENSE` · `COVENANT.md`.

Writing in the standard does not make a derivative work. Copying this file, the prompts, or the tools does.
