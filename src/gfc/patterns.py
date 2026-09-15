# SPDX-License-Identifier: AGPL-3.0-or-later
"""structural shapes. the linter owns this list. prompts point here."""

from __future__ import annotations

import re

MUSH = re.compile(
    r"\b(i['’]d be happy to|i would be happy to|great question|absolutely!|"
    r"happy to help|thanks for asking|of course!|sure thing)\b",
    re.IGNORECASE,
)
AS_AI = re.compile(r"\b(as an ai|i am an ai|i['’]m an ai|as a language model)\b", re.IGNORECASE)
DISCLAIMER = re.compile(
    r"\b("
    r"not (a |legal |financial |medical )?advice\b|"
    r"i am not a (lawyer|doctor|cpa|professional)\b|"
    r"i['’]m not a (lawyer|doctor|cpa|professional)\b|"
    r"this is not (legal|financial|medical) advice\b|"
    r"consult a (professional|lawyer|doctor|qualified)\b|"
    r"for informational purposes only\b"
    r")",
    re.IGNORECASE,
)
MARKETING = re.compile(
    r"\b(delve|leverage|tapestry|let['’]s dive in|dive in|unlock the power|"
    r"game[- ]changer|in today['’]s (fast[- ]paced|digital) world)\b",
    re.IGNORECASE,
)
ROBUST = re.compile(r"\brobust\b", re.IGNORECASE)
RECAP = re.compile(
    r"\b(in conclusion\b|to recap\b|to summarize\b|full circle\b|"
    r"let me recap\b|as (i|we) mentioned\b|in summary\b)\b",
    re.IGNORECASE,
)
HOOK = re.compile(
    r"\b(what should we\b|what would you like\b|want me to\b|shall i\b|"
    r"let me know if\b|anything else i can\b|how can i (help|assist)\b|"
    r"what would you like (me )?to (do|work on)\b|"
    r"feel free to (ask|reach)\b)\b",
    re.IGNORECASE,
)
HOOK_END = re.compile(
    r"(what should we|what would you like|want me to|shall i|"
    r"let me know if|anything else|how can i help|feel free to).{0,40}\?\s*$",
    re.IGNORECASE,
)
WILL_NOT_BULLET = re.compile(
    r"^[-*]\s+(do not|don't|do\s+not|never|this is not|it is not|it['’]s not)\b",
    re.IGNORECASE,
)

# A2 family: empty reversal of two abstractions.
REVERSAL = re.compile(
    r"\b(?:it['’]s|it is|this is)\s+not\b.{1,80}?\b(?:it['’]s|it is)\b",
    re.IGNORECASE | re.DOTALL,
)
REVERSAL_NOT_A = re.compile(
    r"\bnot a .{1,40},\s*a .{1,40}",
    re.IGNORECASE,
)
REVERSAL_PROBLEM = re.compile(
    r"\bisn['’]t the problem\b.{0,50}\bis\b",
    re.IGNORECASE,
)
REVERSAL_QUESTION = re.compile(
    r"\bthe question isn['’]t\b",
    re.IGNORECASE,
)
REVERSAL_NOT_JUST = re.compile(
    r"\bnot just\b.{1,40}\bbut(?: also)?\b",
    re.IGNORECASE,
)

# unicode dashes, or space-wrapped -- used as a dash. CLI flags stay flags.
EMDASH = re.compile(r"(?:\u2014|\u2013|(?<=\s)--(?=\s))")

ANALOGY = re.compile(
    r"\b(?:like a|like an|"
    r"think of (?:it|this|that|[A-Za-z][\w' -]{0,40}) as(?: a| an)?|"
    r"imagine (?:a|an)|is like a|is like an|as if it were a|as if it were an)\s+"
    r"([a-z][a-z0-9'-]*(?:\s+[a-z][a-z0-9'-]*){0,3})",
    re.IGNORECASE,
)

# educate: first sentence of a section names the term before the mechanism.
TERM_INTRO = re.compile(
    r"(?:"
    r"^\*\*[A-Z][^*]{1,48}\*\*\s+is\b|"
    r"^(?:The\s+)?[A-Z][\w.-]{2,40}(?:\s+[a-z][\w.-]{1,40}){0,3}\s+is\s+(?:a|an|the)\b|"
    r"\b(?:called|known as|termed|the term)\s+[A-Z][\w.-]{2,40}\b"
    r")",
)

SIDES = re.compile(
    r"not\s+(?:just\s+)?(.+?)(?:[.!?]|\u2014|\u2013|--|,)\s*"
    r"(?:it(?:['’]s|\s+is)|but(?:\s+also)?)\s+(.+)",
    re.IGNORECASE | re.DOTALL,
)
