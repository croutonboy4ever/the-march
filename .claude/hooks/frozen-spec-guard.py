#!/usr/bin/env python3
"""PostToolUse hook (Write / Edit / NotebookEdit): flag an edit to a frozen spec.

project-method hard rule 3: acceptance criteria in a spec are written before the build
and are read-only during it. A build that needs a criterion changed stops, files a
CHANGES.md row, and waits. references/hooks.md maps this to "PostToolUse on edits to
specs/ — flags any edit to a spec whose status is frozen; build stops and files a
change row".

PostToolUse fires after the edit has landed, so this cannot block the write; it flags
it, feeding the notice back to Claude via additionalContext so the session stops and
files the change row rather than editing frozen criteria in place.

Reads local state only. Fails open and silent.
"""
import os
import re
import sys
import json


def edited_path(data):
    ti = data.get("tool_input") or {}
    return ti.get("file_path") or ti.get("notebook_path") or ""


def is_frozen_spec(path):
    """True when path is a real spec under a specs/ directory whose Status VALUE is
    exactly 'frozen'. Skips `_`-prefixed template files, and matches the value exactly
    rather than as a substring, so a legend line like
    'Status: draft / frozen / built / reviewed' does not misfire."""
    parts = os.path.normpath(path).split(os.sep)
    if "specs" not in parts:
        return False
    if not path.endswith(".md"):
        return False
    if os.path.basename(path).startswith("_"):
        return False  # spec template / legend, not a live spec
    try:
        text = open(path, errors="replace").read()
    except Exception:
        return False
    m = re.search(r"(?im)^\s*(?:#+\s*)?.*\bStatus:\s*([A-Za-z]+)", text)
    if not m:
        return False
    return m.group(1).strip().lower() == "frozen"


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("tool_name") not in ("Write", "Edit", "NotebookEdit"):
        return
    path = edited_path(data)
    if not path:
        return
    if not os.path.isabs(path):
        path = os.path.join(data.get("cwd") or os.getcwd(), path)
    if not is_frozen_spec(path):
        return
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                f"FROZEN-SPEC EDIT FLAGGED: {os.path.basename(path)} has Status: frozen. "
                "Acceptance criteria are read-only during a build (project-method hard "
                "rule 3). If this build needs a criterion changed, stop, file a CHANGES.md "
                "row, and wait for a disposition before editing the spec. If the edit was "
                "only appending review results, note that in the change log."),
        }
    }))


try:
    main()
except Exception:
    pass  # fail open
sys.exit(0)
