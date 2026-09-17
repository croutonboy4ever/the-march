# The March: State
Updated: 2026-09-16 by Claude Code   Last known-good: 143cc3b

## Structure
- Position (mirrors the Notion hub, which stays the single canonical place): The Crossing (ch 02) · P1 Spine · P0 gate passed 2026-08-11 · next P2 Draft.
- Repo: `/Users/tonyweber/Projects/the-march` (git; private remote github.com/croutonboy4ever/the-march, live since 2026-08-11).
- Folder layout: `/site` (static root, POC page), `/data/geo` (raw gitignored, processed committed, scripts), `/data/content/00..11` (chapter folders; only 02 is populated), `/docs` (canonical docs), `/archive/<date>` (superseded files), plus the ten method files added this session.
- Canonical docs: `docs/conventions-v1.2.md` (accuracy and design), `docs/build-plan-v1.1.md` (build method), `docs/roads-period-filter-memo.md`. Earlier versions are retained beside each (`conventions-v1.0.md`, `conventions-v1.1.md`, `build-plan-v1.0.md`).
- Chapter 02 content: `data/content/02/claims-ledger.md` (19 attested claims, P0 done), `route-candidates.md` (R1 to R7), `chapter-spine.md` (P1 beat sheet, built 2026-09-16, awaiting Astra's review).
- Geo pipeline (processed, committed): Pleiades corridor (705 places), AWMC rivers / roads / shoreline / inland water, DEM npz, land-cover npz. Raw downloads on disk, gitignored, checksummed in `data/geo/SOURCES.md`.
- Enforcement added this session: `.githooks/pre-commit` (core.hooksPath = .githooks), `.claude/hooks/` (session-files, frozen-spec-guard, state-freshness), `.claude/agents/reviewer.md`, `.claude/settings.json`.
- Notion database IDs: hub `3b72ada8-7f88-812b-8bb4-ef724a2e3cda`; Decision Log `collection://0a9ed107-5fcf-48af-9b5b-47948defea3b`; Chapter Tracker `collection://33c3d2ae-bad0-44b1-919d-b377ac054c6d`; Source Log `collection://801deedd-86e5-4ecf-b789-7795b2dfa087`.

## Live surfaces
- Repo remote: github.com/croutonboy4ever/the-march (private).
- POC page: `site/index.html`, served static (`python3 -m http.server --directory site 8000`). Not deployed.
- Deploy: Netlify, not yet configured (needed at P7).
- Notion hub "The March" (source of truth for position and decisions).
- Fact base: `~/Claude/research/carthaginian-conflicts/` (local, git-tracked, Drive-mirrored). The only fact base; no fallback (NotebookLM retired 2026-09-10). Credentials: none needed (local files).

## Known gaps
- No chapter prose exists yet: P0 done; P1 beat sheet built 2026-09-16, gate not passed (Astra's review pending, spec criterion 10).
- The ledger lacks army strength before arrival: Polybius 3.60 (38,000 foot, 8,000+ horse at the Rhone) confirmed verbatim in fact-base source 116, not yet a ledger entry.
- Netlify deploy not configured.
- G-1: the modern-pass identification is an open debate, presented as a debate, never resolved (conventions section 2).
- Geo gaps recorded in `data/geo/SOURCES.md`: Camargue shoreline vs DEM sea mask, unplaceable Pleiades places, uncertain pass identifications.
- Notion hub Links repointed to the local library 2026-09-10 (Tony's instruction; the drift is closed).
