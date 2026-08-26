# Project template — how to instantiate

This folder is the project-method starting point: the ten standard files plus the
enforcement infrastructure. To start a real project, copy this folder, then:

1. Rename the placeholder. Replace `PROJECT NAME` throughout the ten files with the real name.
2. Re-initialise git and wire the pre-commit hook:
   - `git init`
   - `git config core.hooksPath .githooks`   (this is per-repo git config; the `.githooks/`
     directory travels with the copy, but the `core.hooksPath` setting must be re-set after a
     fresh `git init`)
3. Run the project-method kickoff (Ritual 1) to fill BRIEF.md and PLAN.md from a dump and the
   interview. Do not hand-edit; the skill writes these files.

## What enforces what

| Rule | Mechanism |
|---|---|
| PLAN.md/LOG.md move with specs/, checks/, SOURCES.md; no scope change without a CHANGES.md row; CLAUDE.md under 40 lines | `.githooks/pre-commit` (git) |
| The ten standard files present | `.claude/hooks/session-files.py` (SessionStart) |
| No edit to a frozen spec's criteria | `.claude/hooks/frozen-spec-guard.py` (PostToolUse) |
| STATE.md kept fresh when structure changes | `.claude/hooks/state-freshness.py` (Stop) |
| A build reviewed by a context that did not write it (hard rule 5) | `.claude/agents/reviewer.md` (read-only) |

The three Claude Code hooks are wired in `.claude/settings.json`, which carries only what
differs from `~/.claude/settings.json`. Global permissions and the machine-wide guards are
inherited, not restated here.
