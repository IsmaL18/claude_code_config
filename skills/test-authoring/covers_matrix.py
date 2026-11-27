#!/usr/bin/env python3
"""Traceability matrix from `covers:` markers. Read-only, standard library only.

A marker is a comment on the line(s) right above a test (above its decorators):

    # covers: AC-3, ADR-0020#inv9        (Python)
    // covers: AC-3                      (TypeScript / JavaScript)

Tokens: an acceptance criterion (AC-3), an ADR guarantee (ADR-0020#inv9),
regression:<ref>, characterization.

Usage (from the repository root):
    python3 covers_matrix.py                       # markdown report on stdout
    python3 covers_matrix.py --format json
    python3 covers_matrix.py --tests tests web/src --specs specs
    python3 covers_matrix.py --changed-since origin/main   # only tests touched by the diff
    python3 covers_matrix.py --strict              # exit 1 if a test has no marker
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build",
    "static", ".mypy_cache", ".pytest_cache", ".ruff_cache", "coverage",
}
PY_TEST_FILE = re.compile(r"(^test_.*\.py$)|(.*_test\.py$)")
JS_TEST_FILE = re.compile(r".*\.(test|spec)\.[cm]?[jt]sx?$")
PY_TEST_DEF = re.compile(r"^\s*(?:async\s+)?def\s+(test_\w+)\s*\(")
JS_TEST_DEF = re.compile(r"""^\s*(?:it|test)(?:\.(?:only|skip|each\([^)]*\)))?\s*\(\s*(['"`])(.+?)\1""")
MARKER = re.compile(r"^\s*(?:#|//)\s*covers:\s*(.+?)\s*$")
DECORATOR_OR_BLANK_COMMENT = re.compile(r"^\s*(@|#(?!\s*covers:)|//(?!\s*covers:))")
DEFAULT_AC = r"\bAC-\d+\b"


def iter_files(roots: list[Path], pattern_py: re.Pattern, pattern_js: re.Pattern):
    for root in roots:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
                continue
            if pattern_py.match(path.name) or pattern_js.match(path.name):
                yield path


def tokens_of(raw: str) -> list[str]:
    return [t.strip() for t in re.split(r"[,;]", raw) if t.strip()]


def scan_tests(path: Path) -> list[dict]:
    """Return one record per test: name, line, covers (possibly empty)."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    is_py = path.suffix == ".py"
    tests = []
    for i, line in enumerate(lines):
        if is_py:
            m = PY_TEST_DEF.match(line)
            name = m.group(1) if m else None
        else:
            m = JS_TEST_DEF.match(line)
            name = m.group(2) if m else None
        if not name:
            continue
        covers: list[str] = []
        j = i - 1
        while j >= 0:
            marker = MARKER.match(lines[j])
            if marker:
                covers = tokens_of(marker.group(1)) + covers
                j -= 1
            elif DECORATOR_OR_BLANK_COMMENT.match(lines[j]):
                j -= 1
            else:
                break
        tests.append({"file": str(path), "line": i + 1, "name": name, "covers": covers})
    return tests


def criteria_of(spec_roots: list[Path], ac_pattern: str) -> list[str]:
    found: set[str] = set()
    rx = re.compile(ac_pattern)
    for root in spec_roots:
        if root.is_file():
            files = [root]
        elif root.exists():
            files = sorted(root.rglob("*.md"))
        else:
            files = []
        for f in files:
            found.update(rx.findall(f.read_text(encoding="utf-8", errors="replace")))
    return sorted(found, key=natural_key)


def natural_key(s: str):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", s)]


def changed_files(base: str) -> set[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"], capture_output=True, text=True, check=False
    ).stdout.split()
    out += subprocess.run(["git", "diff", "--name-only"], capture_output=True, text=True, check=False).stdout.split()
    return set(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=".", help="repository root (default: .)")
    ap.add_argument("--tests", nargs="*", default=None, help="test directories (default: whole root)")
    ap.add_argument("--specs", nargs="*", default=["specs"], help="spec files or directories (default: specs)")
    ap.add_argument("--ac-pattern", default=DEFAULT_AC, help=f"regex of an acceptance criterion in specs (default: {DEFAULT_AC})")
    ap.add_argument("--format", choices=["md", "json"], default="md")
    ap.add_argument("--changed-since", metavar="REF", help="only tests in files changed since REF (and the working tree)")
    ap.add_argument("--strict", action="store_true", help="exit 1 when a test has no marker")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    test_roots = [root / t for t in args.tests] if args.tests else [root]
    spec_roots = [root / s for s in args.specs]

    changed = changed_files(args.changed_since) if args.changed_since else None
    tests: list[dict] = []
    for path in iter_files(test_roots, PY_TEST_FILE, JS_TEST_FILE):
        rel = str(path.relative_to(root))
        if changed is not None and rel not in changed:
            continue
        for t in scan_tests(path):
            t["file"] = rel
            tests.append(t)

    criteria = criteria_of(spec_roots, args.ac_pattern)
    ac_rx = re.compile(args.ac_pattern)
    by_token: dict[str, list[dict]] = defaultdict(list)
    for t in tests:
        for tok in t["covers"]:
            by_token[tok].append(t)

    unmarked = [t for t in tests if not t["covers"]]
    ac_without_test = [] if changed is not None else [c for c in criteria if c not in by_token]
    unknown_ac = sorted(
        {tok for tok in by_token if ac_rx.fullmatch(tok) and criteria and tok not in criteria}, key=natural_key
    )
    over_budget = sorted(
        (tok for tok, ts in by_token.items() if ac_rx.fullmatch(tok) and len(ts) > 1), key=natural_key
    )
    ratio = (len({tok for tok in by_token if ac_rx.fullmatch(tok)}) and
             len(tests) / len({tok for tok in by_token if ac_rx.fullmatch(tok)}))

    result = {
        "tests": len(tests),
        "criteria_in_specs": len(criteria),
        "criteria_covered": len([c for c in criteria if c in by_token]),
        "tests_per_criterion": round(ratio, 2) if ratio else None,
        "tests_without_marker": [f'{t["file"]}:{t["line"]} {t["name"]}' for t in unmarked],
        "criteria_without_test": ac_without_test,
        "markers_unknown_in_specs": unknown_ac,
        "criteria_with_several_tests": {
            tok: [f'{t["file"]}:{t["line"]} {t["name"]}' for t in by_token[tok]] for tok in over_budget
        },
        "matrix": {
            tok: [f'{t["file"]}:{t["line"]} {t["name"]}' for t in ts]
            for tok, ts in sorted(by_token.items(), key=lambda kv: natural_key(kv[0]))
        },
        "scope": f"changed since {args.changed_since}" if changed is not None else "whole repository",
    }

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(render_md(result))
    return 1 if args.strict and unmarked else 0


def render_md(r: dict) -> str:
    out = [f"# Traceability matrix ({r['scope']})", ""]
    out.append(
        f"- tests: {r['tests']}; criteria in specs: {r['criteria_in_specs']}; "
        f"covered: {r['criteria_covered']}; tests per covered criterion: {r['tests_per_criterion']}"
    )
    out.append(f"- tests without marker: {len(r['tests_without_marker'])}")
    out.append(f"- criteria without test: {len(r['criteria_without_test'])}")
    out.append(f"- criteria with more than one test (budget): {len(r['criteria_with_several_tests'])}")
    out.append(f"- markers naming a criterion absent from the specs: {len(r['markers_unknown_in_specs'])}")
    sections = [
        ("Tests without marker", r["tests_without_marker"]),
        ("Criteria without test", r["criteria_without_test"]),
        ("Markers absent from the specs", r["markers_unknown_in_specs"]),
    ]
    for title, items in sections:
        if items:
            out += ["", f"## {title}", *[f"- {i}" for i in items]]
    if r["criteria_with_several_tests"]:
        out += ["", "## Criteria with more than one test (justify each extra)"]
        for tok, ts in r["criteria_with_several_tests"].items():
            out.append(f"- {tok}: {len(ts)} tests")
            out += [f"  - {t}" for t in ts]
    out += ["", "## Matrix (criterion → tests)"]
    for tok, ts in r["matrix"].items():
        out.append(f"- {tok}")
        out += [f"  - {t}" for t in ts]
    return "\n".join(out)


if __name__ == "__main__":
    sys.exit(main())
