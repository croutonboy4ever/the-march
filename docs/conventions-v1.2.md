# The March: Accuracy and Design Conventions

Version 1.2, 2026-09-16. Supersedes v1.1 (retained beside it as `conventions-v1.1.md`). Change from v1.1: section 7 gains the world-state clause, encoding the locked Decision Log row "World state follows the attestation of the time" (2026-08-20) on Tony's instruction of 2026-09-16; nothing else changed. v1.1 note, retained: supersedes v1.0 (retained beside it as `conventions-v1.0.md`). Changes from v1.0 (Astra review recorded 2026-09-10): section 1 Attested drops the NotebookLM fallback and names the local research library plus the clean Polybius and Livy reference texts as the fact base; section 9 item 1 reads "spot-checked against the fact base"; new section 12, Open questions, logs archaeological evidence. This document is canonical: every chapter, vignette, map, and battle stepper is checked against it before shipping. Changes route through the decision log, never by silent edit.

## 1. Provenance system

Every factual or narrative element in the experience carries exactly one of three markers. They are mutually exclusive and always visible to the reader.

**Attested.** Present in the sources held in the fact base (the local research library `~/Claude/research/carthaginian-conflicts/` plus the clean Polybius and Livy reference texts). Every attested claim carries an anchor: source name plus locator (book and chapter for ancient texts, e.g. Polybius 3.54; page or section for modern works). A claim without an anchor does not ship as attested.

**Inferred.** Reasoned from attested material. The display states both the inference and what it rests on. Example pattern: "The column probably stretched over 15 km (inferred from attested army size and standard march-column spacing, with both anchors shown)." An inference that can't name its attested basis is not an inference, it's invention, and it doesn't ship.

**Imagined.** Invented for narrative texture, consistent with the evidence but making no factual claim. Always labeled. Never carries numbers, named events, quotes attributed to real people, or archaeology. An imagined vignette may put a fictional soldier on an attested march; it may not put words in Hannibal's mouth.

Untagged prose defaults to attested and therefore must carry an anchor. Hedging language ("likely," "probably," "most scholars") is never a substitute for a marker.

## 2. Source disagreement

Where Polybius and Livy (or any two corpus sources) conflict, both readings appear with their anchors and the conflict is named in the experience itself. The UI treats disagreement as content, not as a problem: a "sources disagree" affordance opens both accounts side by side. Known standing debates the experience must present as debates, never resolve silently: the Alpine route, Cannae casualty figures, the Zama battle site, army strength numbers throughout. Choosing one reading for narrative flow without flagging the choice is a defect.

## 3. Ancient sources vs. modern scholarship

Ancient sources are evidence. Modern scholarship is interpretation of evidence. The provenance system encodes the difference:

- Attested means attested in the ancient sources, and only there. Attestation is a provenance claim, not a truth claim: an ancient author can be attested and wrong. The marker tells the reader "the sources say this," never "this is true."
- Modern scholarship never upgrades a claim to attested. A modern reconstruction, correction, or estimate enters as inferred, with the modern work named and the ancient anchors it rests on visible. Example: at Cannae, Polybius's casualty figure and Livy's both display as attested with their locators; the modern statistical argument for preferring one appears as inferred, attributed to the specific study.
- When moderns argue the ancients erred, both layers stay visible. The ancient claim keeps its attested marker and anchor; the correction appears as inferred with attribution. The experience never silently replaces the ancient account with the modern consensus, even where the consensus is near-certain.
- Modern scholarly disagreement gets the identical treatment as ancient disagreement: named as a debate, positions attributed.
- The two registers never blend in one untagged sentence. What the sources say and what scholars conclude from them are separate statements with separate markers.

## 4. Numbers policy

Ancient numbers are contested by default. Every troop strength, casualty figure, and distance carries its anchor, and where sources give different figures, all figures appear. Modern scholarly downward revisions are presented as modern estimates, marked inferred, with the scholar or work named. No number is ever invented to fill a gap; a missing number is displayed as unknown.

Rendered terrain grids are visualization-only: any elevation figure displayed in the experience is sourced from full-resolution elevation tiles or an authoritative reference, never read off the render grid. *(Amendment approved 2026-08-09.)*

## 5. Counterfactual content

The Long Shadow chapter's counterfactual material is always labeled as informed speculation, visually distinct from all three provenance markers. It never mixes into the historical chapters.

## 6. Geography rules

Real coordinates and real topography only. Ancient places resolve to Pleiades IDs; period coastlines and Roman roads come from AWMC data; elevation comes from a real DEM or terrain tiles. The custom visual style may simplify rendering but never moves a place, invents a road, or flattens a pass. Where a location is itself uncertain (contested Alpine route waypoints, the Zama site), the map shows the uncertainty: candidate routes and sites rendered as candidates, labeled with which scholars back which, not one silently promoted to fact.

## 7. Module conventions

**Map journey.** Scroll position maps to space and time. Every waypoint carries provenance like any other claim. The camera never visits a place the sources don't put the army.

**Battle stepper.** Phase divisions follow the sources' own structure where the sources give one, and are marked inferred where the phasing is a modern reconstruction. The commander's-eye toggle shows only what that commander could plausibly see or know at that phase; what he could know is itself an inference and is anchored.

**Ground vignette.** First person, tightly sourced, marker always visible at the top of the vignette, per-detail markers where a vignette mixes attested frame with imagined texture. A reader must always be able to answer "did this happen?" for any line.

**World state.** The season, light and weather of a rendered scene follow what the sources attest for that moment, not what looks best. World state is a provenance-bearing choice, not a styling one, and it applies in every visual register. Where the sources attest the conditions, the state is derived from them and needs no separate decision: at The Crossing summit, Polybius 3.54 and Livy 21.35 both put the setting of the Pleiades and thickening snow at the head of the pass (claims ledger TC-13), so the autumn state with early snow follows. Where the sources attest no season or time of day, the state is never chosen silently for effect. How such a state displays, as inferred with its basis named or as styling outside the marker system, is not settled by this clause. *(Decision Log, locked 2026-08-20; added in v1.2, 2026-09-16.)*

## 8. Citation display

Two layers. Reading layer: unobtrusive marker chips (A / I / Im) inline. Detail layer: tap or click a chip to open the anchor, with the full citation and, where the corpus holds it, the passage itself. Citations use consistent short forms: Polybius 3.54, Livy 21.35 for ancient texts, then modern works as Author Year page.

## 9. Preflight before anything ships

Every chapter or public artifact passes this gate: (1) every attested claim resolves to a corpus anchor, spot-checked against the fact base; (2) every inference names its basis; (3) every imagined element is labeled and claim-free; (4) all known source conflicts on the chapter's ground are surfaced; (5) geography spot-checked against Pleiades/AWMC; (6) the gap list for the chapter is current, with gaps shown as gaps, not papered over. Preflight results are logged in the Notion source log.

## 10. Writing register

For newcomers: plain language, short sentences carrying the load, technical terms introduced once and reused consistently. Grand strategy and ground level alternate by design; neither register apologizes for the other. No em dashes.

## 11. Change control

This doc, the chapter map, and locked decisions live in Notion and in the repo. Proposed changes are logged as decisions with rationale, never made silently. Superseded versions are archive-renamed, never deleted.

## 12. Open questions

Archaeological evidence has no explicit home in sections 1 to 3. Default until decided: it enters as inferred with attribution to the excavation report or catalogue, never as attested. To be settled before the first chapter that renders an archaeological feature.
