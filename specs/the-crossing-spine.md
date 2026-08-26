# Spec: the-crossing-spine
Milestone: 1   Change row: none   Status: draft

## Pre-build gate
Inputs in hand: `data/content/02/claims-ledger.md` (19 attested claims, P0 done); `docs/build-plan-v1.0.md` section 5 (phase definition and the two disagreements to land as scenes); `docs/conventions-v1.0.md` section 2 (disagreement as content).
Missing: none. The build may start; freeze the criteria below first.

## What this builds
The P1 beat sheet for The Crossing (chapter 02): the 19 ledger claims reordered into narrative order, each beat mapped to its TC ids, its map-journey module behaviour, and the geography it needs. Lands in `data/content/02/` (for example `beat-sheet.md`).

## Acceptance criteria (frozen at build start, read-only during build)
1. Every beat cites at least one TC id from the claims ledger, or is explicitly marked imagined.
2. Both standing disagreements appear as their own scenes, not footnotes: the route (TC-09a Polybius up-river vs TC-09b Livy's turn to the Druentia) and the blocking rock (TC-15a Polybius carving vs TC-15b Livy fire and vinegar).
3. Each beat names the geography it needs (a place, a Pleiades id, or a corridor feature) and its module behaviour.
4. The beat order is a continuous narrative from the Rhone crossing to arrival in Italy, and no beat references a place the sources do not put the army (conventions section 7).
5. Gap G-1 (the modern pass identification) is carried as a debate, not resolved.

## Check
`checks/the-crossing.md`, section P1. Manual reproduction: read the beat sheet against the claims ledger and confirm each criterion by inspection.

## Review
Reviewer context: subagent (.claude/agents/reviewer.md), fresh context.   Result: <date, pass/fail, notes>

<!-- Status is draft. The building session freezes these criteria (Status: frozen) before starting P1. -->
