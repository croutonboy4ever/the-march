# The March: Build Plan

Version 1.0, 2026-08-20. **This is the method.** Every chapter is built the same way,
in the same phases, against the same gates. The Crossing is the first instance.

This doc is canonical for **the method**: phases, gates, definitions, module economics.
It is not where current position lives. **Position is tracked in the Notion hub**, in the
Current phase line and at the top of every close-out board. One place, so it cannot drift.

Changes to this doc route through the Decision Log, never by silent edit, same as
`conventions-v1.0.md`. Superseded versions are archive-renamed, never deleted.

## 1. The unit of work is one chapter

Not one feature, not one render, not one data layer. A chapter is the smallest thing a
reader can receive, and the hub already commits to every chapter shipping standalone.
Work that does not move a chapter toward a reader is infrastructure, and infrastructure
is scheduled by the chapter that needs it, never in advance of one.

The corollary, which is the point: **nothing gets built because it would be good to
have.** It gets built because the chapter in flight cannot ship without it.

## 2. The phase pipeline

Eight phases, P0 to P7. A phase is done when its gate passes, not when it feels finished.

| Phase | What gets made | Gate (all must pass to advance) |
| --- | --- | --- |
| **P0 Ledger** | The chapter's claims ledger: every claim it will rest on, with marker, source id, locator, and the verbatim supporting text | Every claim carries verbatim text pulled with `source_read`, never a chat summary (SD-13). Gaps are listed as gaps, not dropped |
| **P1 Spine** | The beat sheet: ledger claims reordered into narrative order, each beat mapped to its TC ids, its module behaviour, and the geography it needs | Every beat cites a TC id or is explicitly marked imagined. Both standing disagreements appear as **scenes**, not footnotes |
| **P2 Draft** | The chapter prose, marker-tagged | Preflight items 1 to 3 pass on the draft: every attested claim resolves to an anchor, every inference names its basis, every imagined element is labelled and claim-free |
| **P3 Scenes** | The visual score: for each beat, the bbox, world state, layers, markers | Every world state cites its attestation (see the world-state decision, 2026-08-20). No scene visits a place the sources do not put the army (conventions §7) |
| **P4 Modules** | Whatever interactive module this chapter's Primary module needs, built or extended | The module renders the chapter's scene list end to end from committed data. No hand-placed geography |
| **P5 Assemble** | Prose, scenes and reading layer in one page | The chapter reads start to finish on a phone without a dead end |
| **P6 Preflight** | The conventions §9 six-item gate, run and logged | All six items pass and the result is logged in the Notion Source Log |
| **P7 Ship** | Deployed, on a URL, read by five people who are not Tony | Five reads happened and their reactions are written down |

**A phase may not start before the previous gate passes.** The one exception is P4, which
may start early where it is a module the project has already built for another chapter,
because then it is reuse rather than a build.

### Why this order and not another

P1 before P2 because the beat sheet is reviewable in ten minutes and the prose is a week.
P2 before P3 because the scene list is derived from the beats, not chosen alongside them.
P3 before P4 because a module built without a scene list is a module built for an
imagined chapter. P4 before P5 for the obvious reason. P6 before P7 because conventions
§9 says nothing ships without it.

## 3. Module economics, which is what makes chapters 2 to 12 cheaper

The Chapter Tracker assigns each chapter a Primary module. Across twelve chapters there
are only **six module types**:

| Module | Chapters | First built by |
| --- | --- | --- |
| Map journey | 1 (ch 02) | The Crossing |
| Battle stepper | 3 (ch 03, 05, 10), plus a hybrid at ch 04 | not yet |
| Ground vignette | 1 (ch 01), plus hybrids at ch 06 and 07 | not yet |
| Map + context | 1 (ch 00) | not yet |
| Map convergence | 1 (ch 08) | not yet |
| Consequence tracer | 1 (ch 11) | not yet |

P4 is expensive the first time a module type appears and cheap every time after. Plan the
chapter order around that, not around narrative order.

**One warning that follows directly from this table.** Everything built so far serves
*map journey*, which is one chapter. Cannae, the flagship, is a battle stepper on a flat
plain: its interesting data is formations and phase timing, and the terrain pipeline
barely helps. Budget the battle stepper as a second, full build. A successful Crossing
does not make Cannae downhill.

## 4. Knowing where we are

**Position lives in the Notion hub**, in two places, in one fixed format:

```
Position: <chapter> · <phase> · <last gate passed, dated> · next <phase>
```

- The hub's **Current phase** line carries it, always current.
- Every **close-out board** opens with it, so the history reads as a track record.

No close-out board without a position line. That is a proposed amendment to the
close-out board standing decision; folding it into the canonical Standing Decisions page
needs Tony's explicit instruction naming that page, so it is applied here and flagged
there rather than edited in.

**Only the next actionable tasks become Notion task rows.** The rest of the pipeline
lives in this doc. A board of nine Not-started rows is a wall, not a plan.

## 5. The Crossing: the first instance

Chapter 02. First to be **built** because it makes a good prototype; its position in the
plan is unchanged.

| Phase | State | Notes |
| --- | --- | --- |
| P0 Ledger | **Done** 2026-08-11 | `data/content/02/claims-ledger.md`, 19 attested entries, sources confirmed verbatim. One open gap, G-1, the modern pass identification, which the chapter presents as a debate rather than resolving. The Chapter Tracker's older 8/9 note asking for a locator spot-check is superseded by the 8/11 verbatim pull |
| P1 Spine | **Next** | Two standing disagreements must land as scenes: the route (TC-09a Polybius up-river vs TC-09b Livy's left turn to the Druentia) and the blocking rock (TC-15a Polybius carving vs TC-15b Livy's fire and vinegar) |
| P2 Draft | Blocked on P1 | Outward-facing prose. See the routing note below |
| P3 Scenes | Blocked on P2 | World state is already settled for the summit: Polybius 3.54 and Livy 21.35 both give the setting of the Pleiades and thickening snow, so autumn-crossing with early snow is derived, not chosen |
| P4 Modules | Blocked on P3 | Builds **map journey**, the first module. Includes the reading layer: provenance chips (conventions §8), the sources-disagree affordance (§2), and labels moving from baked raster to screen-space vector, which the label-treatment README already names as the destination |
| P5 Assemble | Blocked on P4 | |
| P6 Preflight | Blocked on P5 | |
| P7 Ship | Blocked on P6 | Netlify, not yet configured |

### Two things that will bite if they are not handled early

**Prose routing.** The chapter is outward-facing text. Tony's global routing rule sends
any composed outward text through the voice chain with a row in the outbound coverage
log. Whether a history chapter in a built experience is inside or outside that rule is
**Tony's call and is not assumed here**. It is a gate on P2 either way, because deciding
it after a draft exists is worse than deciding it before.

**Chip density.** The provenance system is the project's real differentiator and its
biggest reader risk. Nobody knows how chips read until there is a real paragraph with
real chips on a real phone. This is not a decision to argue out; it is a test, and it
sits between P2 and P4.

## 6. What binds every phase

Not restated here, only pointed at. On conflict, the named source wins.

- `docs/conventions-v1.0.md` is canonical for accuracy and design. §9 preflight gates
  everything that ships.
- Every file under `data/geo` is a recorded raw download or the output of a committed
  script over one. No hand-drawn geography, ever.
- Never delete. Archive-rename with a date under `archive/<date>/`.
- All file deliverables are complete replacements, never patches or insert-here notes.
- Canonical pages, meaning any Notion page titled "Canonical:", are edited only on Tony's
  explicit instruction naming that page.

## 7. Change control

This doc versions like the conventions doc. Proposed changes are logged as Decision Log
entries with rationale. Superseded versions are archive-renamed under `archive/<date>/`.
