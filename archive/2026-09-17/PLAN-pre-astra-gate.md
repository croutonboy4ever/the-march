# The March: Plan
Updated: 2026-09-16 by Claude Code

## Milestones
| # | Milestone | Deliverable (thing you can open) | Done check | Status | Closed |
|---|-----------|----------------------------------|------------|--------|--------|
| 1 | The Crossing: spine + draft | Beat sheet in `data/content/02/`, then the marker-tagged chapter prose | checks/the-crossing.md P1 then P2 then P2a: every beat cites a TC id or is marked imagined, both standing disagreements land as scenes, and Astra's review of the beat sheet is recorded; then preflight items 1 to 3 pass on the draft; then the P2a reading test passes on the first three beats (preflight items 1 to 3 on those beats, the page reads on a real phone, Astra's independent read recorded, treatment recommendation filed). Prose routing decided 2026-09-16: newcomer register, no voice chain, Tony reads the draft before P3. | in progress | |
| 2 | The Crossing: scenes + map-journey module | The visual score (bbox / world state / layers / markers per beat) and a working map-journey module rendering that score from committed data, with the reading layer (provenance chips, sources-disagree affordance) | checks/the-crossing.md P3 then P4: every world state cites attestation and no scene visits a place the sources do not put the army; module renders the scene list end to end from committed data with no hand-placed geography. | not started | |
| 3 | The Crossing: assembled + preflighted | The full chapter on one page | checks/the-crossing.md P5 then P6: reads start to finish on a phone with no dead end; the six-item conventions section 9 preflight run and logged in the Notion Source Log. | not started | |
| 4 | The Crossing shipped (MVP) | Deployed on a Netlify URL, read by five people who are not Tony | checks/the-crossing.md P7: five reads happened and their reactions are written down. | not started | |

Status is one of: not started, in progress, blocked, done, parked.

## Current focus
Milestone 1, P1 Spine: beat sheet built 2026-09-16 at `data/content/02/chapter-spine.md` (17 beats, 10 scale transitions, both standing disagreements as scenes at B8 and B14, G-1 open through B15, both candidate beats placed). Spec `specs/the-crossing-spine.md` frozen 2026-09-16. The reviewer subagent passed criteria 1 to 9; its nine content findings were applied. The P1 gate is NOT passed: it waits on Astra's independent review (criterion 10), which Tony runs as a separate task by handing Astra the beat sheet, the claims ledger and the spec, then pastes the result into the next session to record in the spec Review block. P2 Draft does not start until then. Ledger amended the same day on Tony's instruction (CHANGES row 11): TC-20 Polybius 3.60 Rhone strength, TC-06 unit sizes, TC-08 Livy's Island; the spine was updated to use them before Astra's review. Do not open `site/poc/` or `data/geo/scripts/`: a commit touching those instead of `data/content/02/` is the relapse signal (see risks).

## Open questions
| Question | Default if unanswered | Applies on |
|----------|-----------------------|------------|
| Archaeological evidence: which marker? | Default: inferred with attribution (conventions v1.2 section 12) | first chapter rendering an archaeological feature |
| Which identity register leads the brand (with display face and subtitle provenance)? | Leave undecided; it blocks only the title card and frontispiece, not chapter production. The Crossing ships in the locked experience base (Direction B) with no brand dependency. | never blocks chapters; whenever brand work is queued |
| Does an unattested world state display as inferred, or as styling outside the marker system? | Treat it as inferred and name its basis (conventions section 1), the conservative reading. | first scene the sources do not time (Milestone 2) |

## Risks and tripwires
| Milestone | What could fail | Early signal |
|-----------|-----------------|--------------|
| 1 | The relapse: a session does exploratory or pipeline work instead of writing the chapter. | A commit touches `site/poc/` or `data/geo/scripts/` instead of `data/content/02/`. |
| 1 | The load-bearing assumption fails: the draft cannot be both newcomer-readable and preflight-clean. | The P2 draft either reads well but fails preflight (unanchored claims), or passes preflight but reads as a citation list on a phone. |
| 1 | P2a fails: three beats either fail preflight or stop reading on a phone. | Tony cannot read the P2a page aloud from his phone without stopping to decode a chip. |
| 2 | Chip density makes the full chapter unreadable on a phone even after the P2a three-beat gate passes. | The first real paragraph with real chips on a real phone stops reading (build-plan v1.1 flags the three-beat test at P2a, inside P2; this row is the full-chapter risk that remains). |
| 2 | The map-journey module is built against an imagined scene list. | Module work starts before the P3 scene score is frozen. |
| 4 | Ship slips indefinitely and the project idles. | 60 days with no commit and no session (the kill-or-park trip). |
