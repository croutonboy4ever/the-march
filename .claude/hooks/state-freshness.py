#!/usr/bin/env python3
"""Stop hook: STATE.md freshness.

project-method / references/hooks.md: "Warns if structural files changed this session
and STATE.md did not." STATE.md is the record of what exists right now (structure, live
surfaces, known gaps); a session that changed structure without touching STATE.md has
left the record behind.

Approximation of "this session": the working-tree changes present at Stop (staged plus
unstaged). If any change touches specs/ or checks/ but STATE.md is unchanged, warn.

ADVISORY ONLY — never blocks the stop. It emits a systemMessage and exits 0, so a
misfire can never trap a session. Fails open and silent on internal error.
"""
import os
import sys
import json
import subprocess


def project_dir(data):
    d = os.environ.get("CLAUDE_PROJECT_DIR")
    if d:
        return d
    return data.get("cwd") or os.getcwd()


def changed_paths(root):
    names = set()
    for args in (["diff", "--name-only"], ["diff", "--cached", "--name-only"]):
        r = subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)
        if r.returncode == 0:
            names.update(l.strip() for l in r.stdout.splitlines() if l.strip())
    return names


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        data = {}
    root = project_dir(data)
    if not os.path.isdir(os.path.join(root, ".git")) and not os.path.exists(os.path.join(root, ".git")):
        return
    changed = changed_paths(root)
    if not changed:
        return
    structural = sorted(p for p in changed
                        if p.startswith("specs/") or p.startswith("checks/"))
    if structural and "STATE.md" not in changed:
        print(json.dumps({
            "systemMessage": (
                "STATE.md freshness: structural files changed this session "
                f"({', '.join(structural)}) but STATE.md was not updated. If structure, "
                "live surfaces, or known gaps changed, refresh STATE.md before closing "
                "(project-method: STATE.md is never written from memory).")
        }))


try:
    main()
except Exception:
    pass  # advisory only; never trap the stop
sys.exit(0)
