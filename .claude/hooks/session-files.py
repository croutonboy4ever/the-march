#!/usr/bin/env python3
"""SessionStart hook: the ten standard files present.

project-method mandates ten standard items in every project folder. This hook warns
at session start when any are missing and lists them, so the first session that
notices creates them (project-method SKILL.md: "the first session that notices creates
the missing file from the template and records a LOG.md line").

NOTE ON THE COUNT: references/hooks.md labels this row "Nine files present". The method
mandates TEN items (eight files plus specs/ and checks/). This hook checks all ten; the
"nine" in the reference table is a wording slip, flagged at install and enforced here as
ten so the gate matches the rule it serves.

Reads local state only. Fails open and silent: a broken hook here must never block a
session from starting.
"""
import os
import sys
import json
import glob

REQUIRED_FILES = ["BRIEF.md", "PLAN.md", "STATE.md", "DECISIONS.md", "CHANGES.md",
                  "LOG.md", "SOURCES.md", "CLAUDE.md"]
REQUIRED_DIRS = ["specs", "checks"]


def project_dir():
    d = os.environ.get("CLAUDE_PROJECT_DIR")
    if d:
        return d
    try:
        data = json.load(sys.stdin)
        return data.get("cwd") or os.getcwd()
    except Exception:
        return os.getcwd()


def main():
    root = project_dir()
    # Only speak inside a project folder: one that already has a BRIEF.md or CLAUDE.md.
    if not (os.path.exists(os.path.join(root, "BRIEF.md"))
            or os.path.exists(os.path.join(root, "CLAUDE.md"))):
        return
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(os.path.join(root, f))]
    missing += [d + "/" for d in REQUIRED_DIRS if not os.path.isdir(os.path.join(root, d))]
    if not missing:
        return
    body = (
        "PROJECT-METHOD FILE CHECK: this project folder is missing "
        f"{len(missing)} of the ten standard items: {', '.join(missing)}. "
        "A folder missing any of these is non-compliant. Create each missing file from "
        "the project-template schema (project-method references/file-schemas.md) and "
        "record a LOG.md line, before other work.")
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": body,
        }
    }))


try:
    main()
except Exception:
    pass  # never block a session from starting
sys.exit(0)
