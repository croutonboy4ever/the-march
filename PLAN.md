# The March: Plan
Updated: 2026-08-26 by Claude Code

## Milestones
| # | Milestone | Deliverable (thing you can open) | Done check | Status | Closed |
|---|-----------|----------------------------------|------------|--------|--------|
| 1 | The Crossing: spine + draft | Beat sheet in `data/content/02/`, then the marker-tagged chapter prose | checks/the-crossing.md P1 then P2: every beat cites a TC id or is marked imagined and both standing disagreements land as scenes; then preflight items 1 to 3 pass on the draft. Prose-routing decision resolved at P2. | in progress | |
| 2 | The Crossing: scenes + map-journey module | The visual score (bbox / world state / layers / markers per beat) and a working map-journey module rendering that score from committed data, with the reading layer (provenance chips, sources-disagree affordance) | checks/the-crossing.md P3 then P4: every world state cites attestation and no scene visits a place the sources do not put the army; module renders the scene list end to end from committed data with no hand-placed geography; chip-density test passed on a real phone. | not started | |
| 3 | The Crossing: assembled + preflighted | The full chapter on one page | checks/the-crossing.md P5 then P6: reads start to finish on a phone with no dead end; the six-item conventions section 9 preflight run and logged in the Notion Source Log. | not started | |
| 4 | The Crossing shipped (MVP) | Deployed on a Netlify URL, read by five people who are not Tony | checks/the-crossing.md P7: five reads happened and their reactions are written down. | not started | |

Status is one of: not started, in progress, blocked, done, parked.

## Current focus
Milestone 1, P1 Spine: the beat sheet for The Crossing. This is the single next actionable step, and it is writing, not pipeline. The claims ledger (`data/content/02/claims-ledger.md`, 19 anchored beats in narrative order) is the outline; P1 reorders those claims into narrative order, maps each beat to its TC ids, its map-journey module behaviour, and the geography it needs, and lands both standing disagreements as their own scenes (route TC-09a Polybius up-river vs TC-09b Livy's turn to the Druentia; blocking rock TC-15a Polybius carving vs TC-15b Livy fire and vinegar). A draft spec is ready at `specs/the-crossing-spine.md`; the building session freezes its criteria before starting. Do not open `site/poc/` or `data/geo/scripts/` this session: a commit touching those instead of `data/content/02/` is the relapse signal (see risks).

## Open questions
| Question | Default if unanswered | Applies on |
|----------|-----------------------|------------|
| Does outward-facing chapter prose route through Tony's voice chain? | Draft P2 prose in plain newcomer register per conventions section 10, without the professional voice chain, and flag the draft for Tony's read before P3. | P2 start (Milestone 1) |
| 2.5D / 3D approach for scenes? | Flat shaded relief (option 1, the current pipeline); 3D stays out of the prototype chapter (recommendation on record). | P3 scene design (Milestone 2) |
| Which identity register leads the brand (with display face and subtitle provenance)? | Leave undecided; it blocks only the title card and frontispiece, not chapter production. The Crossing ships in the locked experience base (Direction B) with no brand dependency. | never blocks chapters; whenever brand work is queued |
| Does an unattested world state display as inferred, or as styling outside the marker system? | Treat it as inferred and name its basis (conventions section 1), the conservative reading. | first scene the sources do not time (Milestone 2) |

## Risks and tripwires
| Milestone | What could fail | Early signal |
|-----------|-----------------|--------------|
| 1 | The relapse: a session does exploratory or pipeline work instead of writing the chapter. | A commit touches `site/poc/` or `data/geo/scripts/` instead of `data/content/02/`. |
| 1 | The load-bearing assumption fails: the draft cannot be both newcomer-readable and preflight-clean. | The P2 draft either reads well but fails preflight (unanchored claims), or passes preflight but reads as a citation list on a phone. |
| 2 | Chip density makes the narrative unreadable on a phone. | The first real paragraph with real chips on a real phone stops reading (build-plan flags this between P2 and P4). |
| 2 | The map-journey module is built against an imagined scene list. | Module work starts before the P3 scene score is frozen. |
| 4 | Ship slips indefinitely and the project idles. | 60 days with no commit and no session (the kill-or-park trip). |
