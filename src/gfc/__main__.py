# SPDX-License-Identifier: AGPL-3.0-or-later
"""gfc CLI: lint, echo, strip, prompt, check."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .echo import echo_hits
from .lint import format_findings, lint_text
from .prompt import load_prompt, repo_root
from .strip import strip_text

_DOC_LINT = (
    "docs/SPEC.md",
    "docs/IMPLEMENTATION.md",
    "docs/BOUNDARY.md",
    "prompts/genome.md",
    "prompts/canon.md",
    "README.md",
    "AGENTS.md",
    "COVENANT.md",
    "examples/clear.md",
    "skills/gfc/SKILL.md",
)

_EDUCATE_LINT = ("examples/tensor-attention.md",)

_PROSE_SUFFIX = {".md", ".txt", ".rst"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="gfc",
        description="Greene Feynman Clarity. AGPL-3.0-or-later.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_lint = sub.add_parser("lint", help="check prose against the standard")
    p_lint.add_argument("path")
    p_lint.add_argument("--mode", choices=["prose", "educate"], default="prose")
    p_lint.add_argument("--ask", help="original ask, for regurgitation and drift")
    p_lint.add_argument("--ask-file", help="file containing the original ask")
    p_lint.add_argument("--corpus", help="directory of prior outputs, for echo")
    p_lint.add_argument("--json", action="store_true", dest="as_json")

    p_echo = sub.add_parser("echo", help="exact n-grams shared with a corpus")
    p_echo.add_argument("file")
    p_echo.add_argument("--corpus", required=True)
    p_echo.add_argument("--n", type=int, default=8)

    p_strip = sub.add_parser("strip", help="mechanical pass toward the is")
    p_strip.add_argument("file")

    p_prompt = sub.add_parser("prompt", help="emit a drop-in prompt")
    p_prompt.add_argument("name", choices=["genome", "canon", "warehouse"])

    sub.add_parser("check", help="fixtures and lint this tree")

    args = parser.parse_args(argv)
    if args.cmd == "lint":
        return _cmd_lint(args)
    if args.cmd == "echo":
        return _cmd_echo(args)
    if args.cmd == "strip":
        source = _read(args.file)
        sys.stdout.write(strip_text(source))
        return 0
    if args.cmd == "prompt":
        text = load_prompt(args.name)
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")
        return 0
    if args.cmd == "check":
        return _cmd_check()
    return 2


def _read(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def _iter_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    files: list[Path] = []
    for p in sorted(path.rglob("*")):
        if not p.is_file():
            continue
        if p.suffix.lower() not in _PROSE_SUFFIX:
            continue
        parts = {x.lower() for x in p.parts}
        if parts & {".git", "node_modules", "__pycache__", ".venv", "venv"}:
            continue
        files.append(p)
    return files


def _load_corpus(root: Path, skip: Path | None = None) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for p in _iter_files(root):
        if skip is not None and p.resolve() == skip.resolve():
            continue
        rows.append((str(p), p.read_text(encoding="utf-8")))
    return rows


def _cmd_lint(args: argparse.Namespace) -> int:
    ask = args.ask
    if args.ask_file:
        ask = _read(args.ask_file)
    path = Path(args.path)
    files = _iter_files(path)
    if not files:
        print("ERROR: no prose files", file=sys.stderr)
        return 2
    corpus = _load_corpus(Path(args.corpus)) if args.corpus else None
    rc = 0
    payload = []
    for file in files:
        source = file.read_text(encoding="utf-8")
        corp = corpus
        if corpus is not None:
            corp = [(lab, txt) for lab, txt in corpus if Path(lab).resolve() != file.resolve()]
        findings = lint_text(source, mode=args.mode, ask=ask, corpus=corp)
        if args.as_json:
            payload.append(
                {
                    "path": str(file),
                    "findings": [
                        {
                            "rule": f.rule,
                            "severity": f.severity,
                            "line": f.line,
                            "title": f.title,
                            "excerpt": f.excerpt,
                        }
                        for f in findings
                    ],
                }
            )
        else:
            print(format_findings(findings, path=str(file)))
        if any(f.severity == "error" for f in findings):
            rc = 1
    if args.as_json:
        json.dump(payload if len(payload) > 1 else payload[0], sys.stdout, indent=2)
        sys.stdout.write("\n")
    return rc


def _cmd_echo(args: argparse.Namespace) -> int:
    path = Path(args.file)
    source = _read(args.file)
    corpus = _load_corpus(Path(args.corpus), skip=path)
    hits = echo_hits(source, corpus, n=args.n)
    if not hits:
        print("clean")
        return 0
    for h in hits:
        print(f"echo:{h.other}: {' '.join(h.ngram)}")
    return 1


def _cmd_check() -> int:
    import unittest

    tests = repo_root() / "tests"
    loader = unittest.TestLoader()
    suite = loader.discover(str(tests), pattern="test_*.py")
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    rc = 0 if result.wasSuccessful() else 1
    for rel in _DOC_LINT:
        path = repo_root() / rel
        findings = lint_text(path.read_text(encoding="utf-8"), mode="prose")
        if findings:
            print(format_findings(findings, path=rel))
            rc = 1
    for rel in _EDUCATE_LINT:
        path = repo_root() / rel
        findings = lint_text(path.read_text(encoding="utf-8"), mode="educate")
        if findings:
            print(format_findings(findings, path=rel))
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
