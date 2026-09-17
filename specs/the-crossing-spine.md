# Spec: the-crossing-spine
Milestone: 1   Change row: CHANGES.md rows 1 and 2   Status: frozen

## Pre-build gate
Inputs in hand: `data/content/02/claims-ledger.md` (19 attested claims, P0 done); `docs/build-plan-v1.1.md` section 5 (phase definition and the two disagreements to land as scenes); `docs/conventions-v1.2.md` section 2 (disagreement as content).
Missing: none. The build may start; freeze the criteria below first.

## What this builds
The P1 beat sheet for The Crossing (chapter 02): the 19 ledger claims reordered into narrative order, each beat mapped to its TC ids, its map-journey module behaviour, and the geography it needs. Lands as `data/content/02/chapter-spine.md`, the filename the Notion P1 and Astra-review tasks name.

## Acceptance criteria (frozen at build start, read-only during build)
1. Every beat cites at least one TC id from the claims ledger, or is explicitly marked imagined.
2. Both standing disagreements appear as their own scenes, not footnotes: the route (TC-09a Polybius up-river vs TC-09b Livy's turn to the Druentia) and the blocking rock (TC-15a Polybius carving vs TC-15b Livy fire and vinegar).
3. Each beat names the geography it needs (a place, a Pleiades id, or a corridor feature) and its module behaviour.
4. The beat order is a continuous narrative from the Rhone crossing to arrival in Italy, and no beat references a place the sources do not put the army (conventions section 7).
5. Gap G-1 (the modern pass identification) is carried as a debate, not resolved.
6. Every beat states the question its view answers for the reader (why the army is here, how position shapes what happens, or what could plausibly be seen).
7. Every scale transition is flagged and names the continuity triple that persists across it (date or phase, army identifier, place reference) and the consequence visible on return to campaign scale.
8. The opening three beats follow the shape orientation, one concrete situation, one interaction; quiet beats with no interaction are permitted and marked as such.
9. Two candidate beats are placed or declined with a one-line reason each: the Rhone raft construction (Polybius and Livy differ, so a candidate disagreement scene) and the roadside column passage (an inferred calculation from attested army size, provisions and pack animals, anchors shown).
10. Astra's independent review of the beat sheet is recorded in the Review block before the P1 gate is called passed.

## Check
`checks/the-crossing.md`, section P1. Manual reproduction: read the beat sheet against the claims ledger and confirm each criterion by inspection.

## Review
Reviewer context: subagent (.claude/agents/reviewer.md), fresh context.   Result: 2026-09-16, criteria 1 to 9 pass, criterion 10 not met (awaiting Astra), so REVIEW: FAIL (10). Nine content findings (attribution slips at B7, B10, B15, B16; an unmarked imagined vantage at B16; unsourced camera and question wording at B4; a misleading day-count framing at B14; two question tags at B2, B11) were applied to `chapter-spine.md` after the review; the applied version has not been re-reviewed. Correction 2026-09-16: the B7 finding (Livy does not name the Island) was wrong; Livy 21.31 names it (verified in the local library copy, now recorded at ledger TC-08, CHANGES row 11), so the B7 edit was reverted. Two spec-wording notes for the next amendment, criteria unchanged: criterion 4 "references a place" reads wider than the conventions section 7 camera rule (B15 renders disputed passes as candidates); criterion 7 defines no return consequence for downward transitions (the sheet uses "carried to").
Astra independent review (beat sheet, by handoff; Tony gives Astra the files, no repo access):   Result: <date, notes>

<!-- Status frozen 2026-09-16 at P1 build start. Criteria are read-only; a needed change stops the build and files a CHANGES.md row. -->
