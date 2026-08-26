# Spec: <name>
Milestone: <#>   Change row: <# or none>   Status: draft / frozen / built / reviewed

## Pre-build gate
Inputs in hand: ...   Missing: ...   (build does not start on missing)

## What this builds

## Acceptance criteria (frozen at build start, read-only during build)
Numbered. Each one checkable.
1.

## Check
Which script in checks/ proves it, or the manual reproduction step.

## Review
Reviewer context: <subagent / fresh session>   Result: <date, pass/fail, notes>

<!--
Copy this file to specs/<name>.md for each build. Freeze the acceptance criteria
before the build starts; the frozen-spec hook (.claude/hooks/frozen-spec-guard.py)
flags any edit to a spec whose Status line reads "frozen".
-->
