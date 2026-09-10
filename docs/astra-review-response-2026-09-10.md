# The March: response to the Astra review of 2026-09-10

This records how the project answered the advisory review at `docs/the-march-opportunities-for-consideration-2026-09-10.md`. Tony read the assessment on 2026-09-10 and accepted the defaults below. The review is advisory input, graded Informative in SOURCES.md: it supplies leads, never facts. The dispositions are logged as CHANGES.md rows 1 to 10 and the decisions as DECISIONS.md lines dated 2026-09-10.

## The four decisions Tony took

1. **P2a adopted.** An integrated reading test moves inside P2. The first three beats of the draft, marker-tagged, are set on one static page at phone width and read on a real phone before the rest of the draft continues. This tests the load-bearing assumption in BRIEF.md, that a chapter can be newcomer-readable and preflight-clean at once, at three beats rather than at a full chapter. It is the P2a gate in build plan v1.1.

2. **3D rejected for The Crossing and parked to Cannae.** Authored 3D scenes stay out of the prototype chapter, consistent with the PLAN default, the brief non-goal, and the relapse tripwire. The idea is parked with an explicit wake condition: Cannae P3 scene design. This closes the PLAN open question "2.5D / 3D approach for scenes" for The Crossing as flat shaded relief.

3. **Astra as reviewer only.** Astra holds an independent reviewer role at the P1 beat sheet and the P2a page, by file handoff, with no repo access. It is not a second builder for this chapter. The second-builder proposal and the AGENTS.md instruction bridge are parked, wake condition: a scene brief exists for a battle chapter.

4. **The remaining dispositions as listed.** The other review items are absorbed, parked, or rejected exactly as recorded in CHANGES.md rows 1 to 10 and summarized below.

## NotebookLM retirement

NotebookLM is retired as a reference. The local research library `~/Claude/research/carthaginian-conflicts/` is the only fact base, and no fallback is named. The Notion hub Links were repointed to the local library on 2026-09-10 on Tony's instruction, which closes the long-standing fact-base pointer drift. Conventions v1.1 was issued for this removal only, and it also logs archaeological evidence as an open question. The historical NotebookLM mentions in `data/content/02/claims-ledger.md` and `route-candidates.md` are left as they are: they record how the P0 pull was actually made and are not live pointers.

## The ten dispositions, with rationale

1. **Views answer a question; continuity across scale; opening shape; quiet passages permitted.** Absorbed into the spec the-crossing-spine as acceptance criteria 6 to 8. Each view now has to state the question it answers, every scale transition names the continuity triple (date or phase, army identifier, place reference) and the consequence visible on return to campaign scale, and the opening three beats follow orientation, one concrete situation, one interaction. Quiet beats are permitted and marked, so the chapter has room to breathe rather than making every paragraph an interaction.

2. **Rhone raft construction and roadside column passage as candidate beats.** Both are already in the claims ledger, so they cost nothing to consider and carry their own anchors. They enter the spec as criterion 9, two candidate beats that P1 either places or declines with a one-line reason each. The raft is a candidate disagreement scene because Polybius and Livy differ; the column passage is an inferred calculation from attested army size, provisions, and pack animals, with its anchors shown.

3. **Early integrated test of prose, chips, and evidence.** Absorbed as the P2a reading test in build plan v1.1. Testing prose and interaction together at three beats catches a problem that prose review alone misses, such as a map that should replace an explanation or a transition that reads badly. The chip-density test that used to sit between P2 and P4 now sits inside P2 as this gate.

4. **Plain-language provenance labels and one chip per passage.** Absorbed as P2a test variants. The reading test compares per-clause chips (A / I / Im) against one chip per passage with tap-through, and against plain-language labels (Ancient account / Reconstruction / Imagined scene). The same claims and anchors appear in every treatment; only the display changes. Conventions section 8 stays as it is until the test reports a recommendation.

5. **"Show the evidence" render mode and the archaeology convention.** The principle is absorbed: every layer in the P3 scene score carries a marker, so a by-marker render is possible later without retrofitting. The toggle itself is a P4 candidate, not a ship requirement. Archaeology is logged as a conventions open question (v1.1 section 12) with the default that it enters as inferred with attribution to the excavation report or catalogue, never as attested.

6. **3D scenes earlier, Blender pipeline, Astra 3D experiments.** Rejected for The Crossing, for the reasons in decision 2, and parked with wake condition Cannae P3 scene design. The measured 3D work already in the repo is evidence of asset feasibility, not of a reader improvement, and nothing here argues for putting a moving camera and unresolved chip placement into the prototype.

7. **Rendered animation as primary medium.** Rejected. Locked decision 2 holds: interactive web is the only load-bearing form, and audio, video, and animation are possible later layers, never primary.

8. **Stay here, wait for news, ordinary objects, then-and-now Carthage, Turner's painting, illustrative age marker.** Parked as leads, each filed under the chapter it belongs to, with the wake condition being that chapter's P0 ledger. The leads live in `data/content/04/leads.md` (wait for news), `06/leads.md` (stay here), `00/leads.md` (then-and-now Carthage and ordinary objects), and `11/leads.md` (Turner and the age marker, then-and-now Carthage cross-listed). Each is written as a lead, unverified, not a claim, with the empty or abstract-only library entries noted so nothing is built on thin material.

9. **Astra as independent reviewer at gates.** Absorbed. Astra reviews the P1 beat sheet and the P2a page by handoff, with Tony giving Astra the files and Astra holding no repo access. The model that did not build a sequence can examine it for clarity, unsupported assumptions, and defects.

10. **Astra as second builder and the AGENTS.md instruction bridge.** Parked, wake condition: a scene brief exists for a battle chapter. The bounded scene handoff is worth testing once there is a concrete scene to hand off, not before, and the single-active-writer default keeps coordination small until then.
