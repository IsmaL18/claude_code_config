#!/usr/bin/env python3
"""PreToolUse guard for the product-owner agent.

Only PRODUCT.md, USER.md and specs/ of the current project are reachable.
Exit 2 blocks the tool call and shows stderr to the agent.
"""
import json
import os
import sys

ALLOWED_FILES = ("PRODUCT.md", "USER.md")
ALLOWED_DIRS = ("specs",)


def allowed(root: str, raw: str) -> bool:
    if not raw:
        return False
    path = os.path.realpath(raw if os.path.isabs(raw) else os.path.join(root, raw))
    rel = os.path.relpath(path, root)
    if rel.startswith(".."):
        return False
    first = rel.split(os.sep)[0]
    return rel in ALLOWED_FILES or first in ALLOWED_DIRS


def main() -> int:
    data = json.load(sys.stdin)
    root = os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd())
    tool = data.get("tool_name", "")
    inp = data.get("tool_input", {}) or {}
    if tool == "Glob":
        base = inp.get("path") or root
        target = os.path.join(base, inp.get("pattern", "")).split("*")[0] or base
    else:
        target = inp.get("file_path") or inp.get("path") or ""
    if allowed(root, target):
        return 0
    print("Accès refusé : le product-owner ne lit et n'écrit que PRODUCT.md, USER.md et specs/.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
