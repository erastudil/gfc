# SPDX-License-Identifier: AGPL-3.0-or-later
"""Greene Feynman Clarity: standard and tooling for human-facing agent prose."""

from .echo import echo_hits, echo_ngrams
from .lint import Finding, lint_text
from .prompt import load_prompt
from .strip import strip_text

__version__ = "1.0.0"
__all__ = [
    "Finding",
    "echo_hits",
    "echo_ngrams",
    "lint_text",
    "load_prompt",
    "strip_text",
    "__version__",
]
