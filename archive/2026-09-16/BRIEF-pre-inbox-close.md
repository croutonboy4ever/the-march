# The March: Brief
Kickoff: 2026-08-26   Last reviewed: 2026-09-10

## Objective
The Second Punic War is told as a map-driven interactive web experience for newcomers, where every factual and narrative element shows whether it is attested, inferred, or imagined, delivered chapter by chapter with The Crossing proven first on a real reader.

## Stakeholders
- Primary reader: a curious newcomer to the Second Punic War, no prior knowledge, reading on a phone. A bad outcome for them is confusion or a dead end: chips so dense the narrative stops reading, or a chapter that does not resolve on a small screen.
- Tony, as author and owner: the project carries his accuracy standard. A bad outcome is a claim that ships mislabeled, imagined texture read as fact or a modern reconstruction passed off as attested. The provenance system exists to make that failure structurally hard.
- No client, no external deadline, no third-party obligation. The work is judged as its own, linkable from tonyweber.info later but standing on its own.

## Scope
In: an interactive web experience on the Second Punic War (218 to 202 BC), a map-driven narrative spine with deep-zoom chapters, built for newcomers, with the three-marker provenance system (attested / inferred / imagined) on every element. Chapters are built one at a time through the eight-phase method, each shipping standalone.

(MVP) The Crossing (chapter 02) shipped through P7: live on a URL and read by five people who are not Tony, proving the full method and the provenance system on one real chapter. The remaining chapters are the tracked pipeline behind the MVP, not part of it.

## Non-goals
- Not a comprehensive history or a textbook. Depth lives in the provenance layer, not in prose volume.
- No invented geography and no invented facts to fill gaps. A missing number shows as unknown, a contested route shows as a debate, nothing is drawn freehand.
- Not a framework or engine build yet. Static files until chapters exist; no framework, 3D viewer, or CMS adopted ahead of a chapter that needs it.
- Not a general Punic Wars app. Interactive web is the only load-bearing form; audio, video, and animation are possible later layers, never primary.
- Not a mobile app or app-store product.
- Not gamified.
- Not monetized.

## Success criteria
1. The Crossing passes its six-item conventions section 9 preflight, logged in the Notion Source Log.
2. The Crossing reads start to finish on a phone with no dead end.
3. Five people who are not Tony have read The Crossing and their reactions are written down.
4. In any shipped chapter, every attested claim resolves to a corpus anchor, every inference names its basis, and every imagined element is labelled and claim-free (the provenance system holds under a real reader).

## Assumptions and dependencies
- Assumes The Crossing can be drafted as prose that is at once newcomer-readable and preflight-clean. This has never been demonstrated; every artifact to date is pipeline or renders. If it cannot, the pipeline stalls at P2 Draft. (Named by the adversarial pass, 2026-08-26.)
- Depends on the local fact base `~/Claude/research/carthaginian-conflicts/` (149 sources, ancient primaries plus scholarship). If unreachable, claim verification and preflight halt. It is the only fact base; no fallback.
- Depends on the committed geo-data pipeline (Pleiades, AWMC, DEM, land cover) under `data/geo/`. If a processed file is lost it is reproducible from a committed script over a recorded raw download.
- Depends on Netlify for the P7 deploy (not yet configured). If absent, any static host can serve the `site/` directory.
- Depends on the Notion hub as source of truth for position and decisions. If unreachable, position also lives in the PLAN.md Current focus line and this repo's LOG.md.

## Constraints
- Surfaces: must run on a phone and a Mac. A static site, no build step, no framework until chapters exist (the README revisit clause, trigger "when chapters exist").
- Maintenance tolerance: low. Nothing that adds a permanent maintenance surface is adopted ahead of need.
- Cost: free or near-free tooling (public data sources, Netlify free tier, private GitHub).
- Accuracy: governed by `docs/conventions-v1.1.md`; nothing ships without its preflight gate.

## Kill condition
A passion project with no external deadline: parked, never killed, and parked only on idleness, never on the idea. Idle window: if the folder goes 60 days with no commit and no session, the next session does not silently resume. It runs a kill-or-park decision with Tony (park with a wake condition, or drop). Parking is a recorded state with a wake condition, so a stall becomes a logged decision instead of a lost thread.
