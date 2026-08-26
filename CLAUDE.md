# The March

Read PLAN.md and STATE.md before doing anything. BRIEF.md is why this exists.
Project method: project-method skill governs structure; build-engineer governs builds.
Accuracy is canonical in docs/conventions-v1.0.md; the build method in docs/build-plan-v1.0.md.

## Rules that never change
- No build without a spec in specs/ with frozen acceptance criteria.
- No scope change without a CHANGES.md row first.
- No milestone without a deliverable and a done check.
- Update PLAN.md and LOG.md before any commit lands.
- Read back every write.
- Summaries and recaps are leads; read the original. Grades come from SOURCES.md.
- Attested means attested in the ancient sources only; modern scholarship enters as inferred with attribution. Nothing is invented to fill a gap.
- Never delete; archive-rename under archive/<date>/. All deliverables are complete replacements.
- Position lives in the Notion hub position line; do not let it drift.
- Canonical pages (Notion "Canonical:") are edited only on Tony's explicit instruction naming the page.

## Where things are
- Specs: specs/   Checks: checks/   Project how-tos: .claude/skills/
- Hooks: .githooks/pre-commit (git) and .claude/hooks/ (SessionStart, PostToolUse, Stop), wired in .claude/settings.json.
- Fact base: ~/Claude/research/carthaginian-conflicts/ (local; the NotebookLM notebook is a fallback only).
- Notion hub "The March" 3b72ada8-7f88-812b-8bb4-ef724a2e3cda (source of truth for position and decisions).
- Repo: github.com/croutonboy4ever/the-march (private). Deploy: Netlify (P7, not yet configured).
