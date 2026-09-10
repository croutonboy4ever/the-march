# The March: Sources
Updated: 2026-09-10 by Claude Code

## Honest assessment
Settled by sources: the objective, the container form (interactive web, map-driven spine), the real-geography rule, the own-identity decision, the standalone-chapter rule, the prototype = The Crossing, the eight-phase build method, the accuracy and provenance conventions, the current position (ch 02, P1 next), and the locked design decisions (base register Direction B, roads staged, land-cover handling, world state follows attestation).

Suggested only (confirmed with Tony this session): the audience and stakeholders, and the four parked design questions (2.5D/3D, brand register, unattested world-state marker, prose routing), which enter PLAN.md as open questions with defaults.

Silent, so asked in the interview on 2026-08-26: the project-level win condition and success criteria, the kill/park condition and idle window, and the fuller non-goals. All are now answered by Tony and stand as Definitive.

Strongest source: the Notion Decision Log (17 rows) with the hub, because both are Tony-confirmed and are the project's own source of truth for state and locked calls. Weakest source used: `data/content/02/route-candidates.md`, because its scholar attributions come from a NotebookLM corpus query with locators self-flagged "to be spot-checked at preflight"; it is Informative and its route claims are not verified history.

## Verified historical sources vs Claude-generated material
The project's differentiator is provenance, so its own record must never let generated content pass as attested history. The two are kept separate.

Verified historical (evidence and scholarship, the fact base):
- Ancient primary texts, used verbatim and confirmed by content search for the 19 chapter-02 claims: Polybius, Histories (Shuckburgh trans.) Book III 42 to 56; Livy, History of Rome (Church & Brodribb trans.) Book XXI 27 to 38; Cornelius Nepos, Life of Hannibal 3.4. Fact-base ids are recorded in `data/content/02/claims-ledger.md`.
- Modern scholarship in `~/Claude/research/carthaginian-conflicts/` (149 sources; for example Goldsworthy, Miles, MacDonald, Lazenby, Lancel, Bagnall, Mahaney's soil-core studies). Modern work is interpretation: it enters as inferred with attribution and is never upgraded to attested (conventions section 3).
- Tertiary and popular material in the same library (Wikipedia, Study.com, YouTube documentary transcripts, Reddit): leads and orientation only, never a shipping anchor.

Claude-generated material (NOT verified history; must always carry a marker or an explicit exemption, and never default to attested):
- The R1 to R7 route-candidate scholar attributions in `route-candidates.md` (from a corpus query; locators unspot-checked; each argument marked inferred).
- The least-cost Tobler traverse route lines on the identity plates (computed from the DEM, marked inferred, not an attested itinerary).
- All renders, art-direction plates, register variations, and the POC map styling (presentation, not evidence).
- The subtitle "Hannibal and the war that nearly ended Rome" (a framing claim carrying no marker; its provenance status is an open brand question).
- No chapter prose exists yet. When it does, every attested line must resolve to a fact-base anchor before P2 passes.

## Inventory
| # | Source | Type | Date | Read as | Grade | Location |
|---|--------|------|------|---------|-------|----------|
| 1 | Notion hub "The March" | project source of truth (page) | read 2026-08-26 (page as of 2026-08-20) | original | Definitive | Notion 3b72ada8-7f88-812b-8bb4-ef724a2e3cda |
| 2 | Decision Log (17 rows) | decision database | 2026-08-26 | original | Definitive | Notion collection://0a9ed107-5fcf-48af-9b5b-47948defea3b |
| 3 | conventions-v1.0.md | canonical accuracy/design doc | approved 2026-08-09 | original | Definitive | docs/conventions-v1.0.md |
| 4 | build-plan-v1.0.md | canonical build method | 2026-08-20 | original | Definitive | docs/build-plan-v1.0.md |
| 5 | data/geo/SOURCES.md | data provenance record | 2026-08-17 | original | Definitive | data/geo/SOURCES.md |
| 6 | claims-ledger.md (ch 02) | evidentiary ledger, 19 verbatim-confirmed claims | 2026-08-11 | original | Definitive | data/content/02/claims-ledger.md |
| 7 | route-candidates.md | route-debate attributions | 2026-08-11 | original (self-flagged lead-grade) | Informative | data/content/02/route-candidates.md |
| 8 | roads-period-filter-memo.md | options memo (decision Locked) | 2026-08-17 | original | Informative | docs/roads-period-filter-memo.md |
| 9 | site/index.html + poc NOTES/READMEs | work products, design options | 2026-08-17 to 20 | original | Informative | site/poc/** |
| 10 | README.md | project self-description | 2026-08-20 | original | Informative | README.md |
| 11 | Carthaginian-conflicts fact base | historical corpus (149 sources) | indexed 2026-08-25 | original (index + sources on disk) | Mixed (see split above) | ~/Claude/research/carthaginian-conflicts/ |
| 12 | Prior Claude chats (14+ sessions) | working sessions | 2026-08-09 to 25 | via transcript search | Leads only | CCD session history |
| 13 | Tony interview answers (Q1 to Q4) | Tony's own recorded decisions | 2026-08-26 | original (this session) | Definitive | this session / DECISIONS.md |
| 14 | conventions-v0.2.md | superseded conventions | 2026-08-09 | original | Stale | docs/conventions-v0.2.md |
| 15 | the-march-opportunities-for-consideration (Astra review) | advisory review doc | 2026-09-10 | original (advisory input; leads only, never a fact source) | Informative | docs/the-march-opportunities-for-consideration-2026-09-10.md |

## Extracted statements
| Informs | Statement | Source # | Where | Verbatim? | Grade | Conflicts with |
|---------|-----------|----------|-------|-----------|-------|----------------|
| Objective/Scope | Interactive web experience on the Second Punic War, map-driven spine, deep-zoom chapters, for newcomers | 1, 2 | hub; DL 2026-08-07 rows | paraphrase | Definitive | none |
| Scope | Real coordinates and real topography, never freehand geography | 2 | DL 2026-08-07 Locked | verbatim | Definitive | none |
| Scope | Every chapter ships standalone, never a build designed to halt midway | 2 | DL 2026-08-07 Locked | verbatim | Definitive | none |
| Scope/MVP | The win is The Crossing shipped through P7 | 13 | interview Q1 | paraphrase | Definitive | none |
| Method | Eight gated phases P0 to P7; one chapter is the unit of work | 4 | build-plan sections 1 to 2 | paraphrase | Definitive | none |
| Plan/position | The Crossing (ch 02): P0 done 2026-08-11, P1 Spine next, then P2 Draft | 1 | hub position line | verbatim | Definitive | none |
| Kill condition | Park only on 60-day idleness, never on the idea | 13 | interview Q2 | paraphrase | Definitive | none |
| Non-goals | Seven non-goals (see brief) | 13 | interview Q3 | paraphrase | Definitive | none |
| Stakeholders | Newcomer on a phone; Tony as accuracy owner; no client | 13 | interview Q4 | paraphrase | Definitive | none |
| Assumptions | Chapter count: build-plan and folders say twelve (00 to 11) | 4 | build-plan section 3; data/content/ | paraphrase | Definitive | hub "thirteen chapters" (# 1) |
| Open question | 2.5D/3D undecided; recommendation is 3D not in the prototype | 2 | DL 2026-08-09 Open | paraphrase | Directive | none |
| Open question | Brand register undecided, deferred, off the critical path | 2 | DL 2026-08-17 Open | paraphrase | Directive | none |
| Design (locked) | Experience base register = Direction B, C as data-view | 2 | DL 2026-08-17 Locked | paraphrase | Definitive | none |
| Design (locked) | World state follows the attestation of the time | 2 | DL 2026-08-20 Locked | verbatim | Definitive | none |

## Conflicts
- Chapter count: the Notion hub says "thirteen chapters" (# 1); build-plan section 3 and the `data/content/` folders (00 to 11) say twelve (# 4). Open, left for Tony, not resolved here.
- Fact-base pointer: CLOSED 2026-09-10. The Notion hub Links were repointed to the local carthaginian-conflicts library on Tony's instruction, and NotebookLM is retired as a reference (DECISIONS.md 2026-09-10). The repo and the hub now agree.

## Stale
| Statement | Source # | Superseded by |
|-----------|----------|---------------|
| conventions v0.2 (accuracy and design) | 14 | conventions-v1.0.md (# 3), approved 2026-08-09 |
| "pick the framework" as a next step | 12 | the README revisit-when-chapters-exist clause; withdrawn 2026-08-20 |
| route-candidates locators "to be spot-checked" method | 7 | the claims-ledger SD-13 verbatim-pull method (# 6), 2026-08-11 |
