# The March

## Experience opportunities for consideration

Prepared for Tony Weber from the discussion with Astra on 10 September 2026

**Status: advisory project input.** This document captures possibilities, recommendations and unresolved questions. It does not approve new scope, alter the build order, assign work or supersede the Notion decisions and canonical project conventions. Authorizing this document did not authorize the experiments described in it. The Word and Markdown editions contain the same substantive text.

### The intent behind the request

Tony is building an interactive experience about the Second Punic War in his spare time. He wants readers to follow armies across the Mediterranean world and then understand events at the scale of a battlefield or a person standing on the ground. He also wants to explore the lives affected by the war and the ways its history remains present today.

The ambition is an enjoyable, informative experience for a curious newcomer. It needs to be achievable by a solo builder with limited time, no coding experience and a modest budget. Claude is the established build surface. Astra could contribute selected visual work, experiments and independent review without requiring Tony to manage two competing projects.

### What the current approach gets right

The map-driven narrative, standalone chapters and phone-first audience remain sound choices. Real geography can explain distance, constraint and the relationship between separate armies. The source ledger and explicit distinction between ancient testimony and reconstruction provide a strong basis for responsible visual storytelling.

The Crossing remains the approved first complete release. Its success criteria include a published chapter, a functioning reading experience on a phone and five readers other than Tony. Direction B has enough visual range to support further experience work without reopening the identity exploration. [1–4]

### The principal opportunity

The work reviewed has established useful geography, visual treatments and research controls. It has not yet demonstrated a complete chapter with readers. The largest opportunity is to connect campaign movement, battlefield explanation and human experience within the same narrative, while learning earlier which interactions help.

There is also room to give the war a world to interrupt. A town can remain in view after an army leaves. A familiar object can explain labor or exchange. Waiting for news can reveal a different experience of an event the reader has already watched unfold.

These possibilities should be judged by what they add to an individual chapter. They do not imply a requirement to build a complete simulated ancient world.

<!-- pagebreak -->

## Making the experience easier to enter

### Connect the changes of scale

Each view should answer a question. At campaign scale, explain why the armies are here and what they are trying to achieve. At battlefield scale, show how positions and movement affect events. At human scale, explore what could plausibly be seen or understood at that moment.

Keep the date or phase, army identifiers and a small location reference consistent during transitions. Returning to the campaign map should reveal the consequence of the scene just examined. A commander’s view should be tied to the same moment as the overhead explanation.

### Offer a clear route through the chapter

A proposed opening would give brief orientation, establish a concrete situation, and introduce one interaction that makes it clearer. Broad exploration and source detail can remain available without being prerequisites for continuing. The data prototype’s dense labels and long caption are useful research displays, but do not establish the desired reading experience.

Interactions can give readers control over pace, replay, comparison and viewpoint while preserving the historical sequence. That is compatible with the project’s current decision against gamification. Avoid making every paragraph an interaction; quieter passages and optional details give the chapter room to breathe.

### Test prose and interaction together earlier

The current method requires a ledger, then a spine, prose, scenes, modules, assembly, preflight and shipping. The proposed adjustment is a bounded test of a short sequence containing actual prose, map states and evidence controls before the full draft is finished. A map may replace an explanation, and an awkward transition may reveal a problem that prose review misses. [3]

This would be a change to the existing method and its restrictions on early exploratory work. It would need an explicit decision. The complete Crossing chapter would remain the finish line; a successful fragment would not replace it.

### Make evidence labels legible to newcomers

The underlying claim-level sourcing should remain. A possible reading treatment would use one visible label for a passage or scene with consistent provenance, separating labels when the status changes. Plain-language labels such as “Ancient account,” “Reconstruction” and “Imagined scene” could be tested against A / I / Im.

A tap would expose individual claims and anchors. Readers must understand that an ancient account is evidence of what an author reported, not a guarantee of truth. Disagreements should remain visible without suggesting every interpretation has equal support. Changing the current always-visible inline treatment would require a conventions decision. [2]

<!-- pagebreak -->

## Where 3D could make a difference

### A capability worth testing

The discussion began with a cautious recommendation to keep 3D selective and later. Tony’s question about Astra and Blender led to a revised assessment: a few authored 3D scenes could be a central feature worth testing earlier. This is the final position from the conversation, still a proposal.

No comparative reader test or project-specific demonstration has established an improvement. There is also no evidence here that Astra is categorically better than Claude at 3D work. A bounded deliverable would test the proposed division of labor.

### Three different kinds of ground level

**Close battlefield view.** Formations and phases can explain movement and spatial relationships with simplified figures or symbols. At Cannae, a controlled transition between overhead and low camera positions could help readers compare a complete pattern with a constrained perspective.

**Commander’s information view.** A terrain visibility calculation can contribute, but cannot establish what a commander knew. Position, intervening troops, weather and information received may all matter. Assumptions would need to be identified and grounded where possible.

**Eye-height reconstruction.** The current elevation data cannot supply person-scale terrain detail. Additional authored detail could make such a scene possible, but would remain reconstruction. At Zama, the uncertainty over the battlefield location also limits any claim to an exact historical viewpoint. [2, 5]

### Production and delivery choices

Blender can be used to construct scenes, repeat figures, animate formations and render controlled camera views through scripts. A model can write and revise those scripts; Blender executes them. Browser tools such as Three.js can display interactive 3D, while simpler overlays can use standard web graphics. [7]

**Pre-rendered sequences** offer predictable imagery, authored viewpoints and simpler display. Readers could advance, pause or replay short sections. **Interactive 3D** allows more inspection and viewpoint control, with additional work on phone performance, navigation and fallback views. The current rule that animation is not the primary medium would need review if rendered sequences became the chapter’s main storytelling form.

The existing terrain study includes a 2.2 MB mesh variant and a roughly 5.1 MB exported scene. Those measurements support asset feasibility, not verified phone performance. Mesh fidelity to modern elevation data does not establish ancient terrain accuracy. [5]

A restrained visual style is the practical starting point. Readable formations, terrain and camera placement deserve effort before detailed faces, individual combat or extensive costume variation. No model needs to generate imagery during a reader’s visit.

<!-- pagebreak -->

## Human and material experiences

### Stay in one place

At selected moments, offer “Follow the army” or “Stay here.” Remaining in a town would let readers revisit the same place as the years advance, seeing documented changes in allegiance, government, siege conditions or inhabitants’ circumstances. Familiarity could give later events more weight.

This would extend the planned vignettes into a continuing local perspective. Fronda’s work on southern Italy is a relevant research lead, but the local entry contains an abstract and related material rather than the full book. Begin with one well-supported community. Build effort is moderate; the research burden could be larger. [6, 8]

### Wait for news

Separate the time of an event from the arrival of reports elsewhere. Readers could inspect what a report reveals, what remains unknown and how the situation has moved on. Any modeled travel interval should expose its assumptions.

Livy’s account of people waiting at Rome’s gates after Trasimene provides a potential anchor. A scene could follow the reader’s view of the battle with the uncertainty of people awaiting news. Present it as Livy’s account, without invented family testimony. This is a low to moderate build using text, a map and restrained visual changes. [8]

### Watch an army pass

A fixed roadside view could show the column passing while an illustrative clock advances. Readers could explore how assumed spacing, width and army size change the passage time. A related explanation could show food requirements using sourced inputs and visible uncertainty.

The Crossing ledger already records boats purchased locally, clothing and boots, provisions and pack animals. These details connect movement with the people and resources that support it. Simplified repeated figures are a plausible use of scripted animation. The calculations would be reconstructions, not precise historical readings. Build effort is moderate. [4]

### Inspect ordinary objects

Offer a small number of objects to turn, open or examine: a dated coin, a vessel, a fastening or a tool. Connect the object to its material, use and place in the wider story. A domestic or workshop scene could use three carefully selected objects without requiring a reconstructed city.

This brings curiosity and pleasure into the experience. It also requires period-specific research. The local Florence Dupont daily-life entry is empty, so it cannot support detailed claims. The British Museum coin identified during the discussion is a candidate for research, not proof of any individual’s wartime possessions. Build effort ranges from low for photographs and diagrams to moderate for 3D objects. [6, 8]

<!-- pagebreak -->

## Discovery and the history that remains

### Assemble an explanation

The Rhone elephant crossing could become an inspectable construction sequence. Readers would advance through the raft arrangement described by an ancient account, rotate the assembly or reveal a cross-section, and compare differences between accounts. The relevant descriptions are already in the Crossing ledger. [4]

This offers interaction through curiosity rather than scoring. A visual reconstruction of a described mechanism is not proof that it would have worked. An engineering claim would need separate validation. Build effort is moderate for one bounded mechanism, making it a candidate before a populated battle scene.

### Reveal the evidence inside a scene

A “Show the evidence” control could change the rendering. Archaeologically supported features would remain identified; details from ancient texts would show their anchors; reconstructed positions would become outlines or ranges; illustrative detail would fade.

This could make the provenance system part of the experience. It would also expose how persuasive a complete render can be despite gaps in knowledge. The current conventions need a clearer treatment of archaeological evidence before this becomes a shared visual rule. Planning it into scenes early is easier than retrofitting it. Build effort is moderate. [2]

### Find the ancient place within the present one

At selected endings, preserve orientation while moving into a present-day view. Matched images or map overlays could identify what survives, what changed and what remains uncertain. Carthage is a promising candidate, with Punic and Roman remains that must be distinguished rather than blended into one imagined ancient city. [8]

This can connect the story with living places in Tunisia, Spain and Italy. Contemporary local perspectives would require additional research and attribution. A few accurate comparisons are a low to moderate build; a modern touring application would be a separate project.

### Examine how Hannibal has been pictured

The Long Shadow could include later representations of the war. Turner’s Alpine crossing painting, exhibited in 1812, offers a documented connection to the Napoleonic context. Readers could compare the painting, the ancient account and The March’s own reconstruction. [8]

Specific uses in art, military education, monuments or political language are potential research topics. Modern analogies should be attributed to whoever makes them. They should not imply a simple causal line from the Punic Wars to today’s conflicts. Build effort can remain low with a few carefully chosen comparisons.

Across these experiences, elapsed years can make duration tangible. An explicitly illustrative age marker could show a child reaching adulthood during the war without inventing a biography. Sound or short audio passages remain optional later layers, with equivalent text and no claim to recovered ancient speech.

<!-- pagebreak -->

## Working with Claude and Astra

### A proposed division of work

Claude would remain the lead builder for chapter production, source ledgers, integration and release. Astra could take bounded visual experiments or 3D scenes and provide independent review. The model that did not build an important sequence could examine it for clarity, unsupported assumptions and defects.

Tony would continue to make creative, historical and scope decisions. The assignments are starting hypotheses based on the existing workflow and the capabilities Tony wants to explore. They should change if the outputs justify it. Routine tasks need not be performed twice.

### Shared awareness through the project record

Neither platform should be assumed to know the other’s conversations automatically. Shared files can preserve current decisions, deliverables and unresolved work. The receiving model still needs to read them before proceeding, including when its own conversation remains open.

Notion would retain its designated authority for approved decisions and project position. PLAN.md and STATE.md would hold the implementation view and next step, with LOG.md recording concise handoffs. The sources, specifications and actual deliverables remain the evidence. Models would maintain these during authorized work; Tony should not have to write recaps or transport code. [1, 3]

A small instruction bridge could make Codex read the established project rules. Codex uses AGENTS.md; Claude Code uses CLAUDE.md and supports imported instructions. The project’s Claude-specific hooks do not automatically run in Codex, so equivalent checks or explicit handoff checks would be needed. This setup is proposed, not installed. [7]

### A bounded scene handoff

1. Claude prepares a chapter-specific brief identifying the explanatory purpose, source claims, geography, assumptions and expected controls.
2. Astra produces an editable scene and generation script, a viewable preview, a website-ready export, and a short record of limitations.
3. The handoff identifies the saved version, output files, checks completed and open issues. Claude inspects the deliverable, integrates it and tests it within the chapter.
4. Tony reviews a concrete experience at a meaningful stopping point. Proposed changes to the plan remain separate from accepted decisions.

### Keep coordination small

Default to one active writer in the shared project folder. Sequential handoffs reduce conflicting edits and confusing state. If parallel work becomes useful, isolate it in a separate working copy and let Claude manage integration.

Shared records and short handoffs are sufficient to test the collaboration. Automated messaging, API relays and a new shared-memory service would add maintenance before demonstrating value. The intended overhead is one assignment and a reviewable result, with technical coordination handled by the models.

<!-- pagebreak -->

## Practical limits and ways to learn

### What a solo builder can reasonably pursue

The affordable form is a static website with selected assets, simple controls and a small number of authored scenes. Blender is free. Browser graphics do not inherently require a paid mapping service. Modeling, rendering, image permissions and historical review still require time and sometimes money. A cloud rendering service or live AI feature would introduce separate costs. [7]

The conversation used $0–$10 per month as an initial hosting allowance, separate from existing AI subscriptions, a domain and artwork. This was not a full project budget or a guarantee. Netlify’s pricing reviewed on 10 September 2026 listed a free plan with 300 monthly credits and a $9 Personal plan; traffic and publishing use allowances. Verify terms when choosing a host. [7]

There are no reliable delivery-time estimates yet. The principal constraints are Tony’s review time, source readiness and the amount of custom scene work. Avoid assuming that a model’s ability to generate code eliminates maintenance or historical verification.

### Candidate experiments rather than a new queue

An early integrated reading sequence could test prose, map transitions and evidence labels together. A paired 2D and 3D sequence could test whether a controlled perspective change improves understanding. A raft explanation or column-passage scene could test a bounded interaction tied to the Crossing’s existing ledger.

Keep narration and historical content equivalent when comparing treatments. Observe whether newcomers can explain the spatial problem, distinguish testimony from reconstruction, find the controls and choose to continue. Check loading, responsiveness and a usable fallback on a phone. Longer viewing time alone is ambiguous; it can indicate interest or confusion. Five readers can expose problems and promising differences, but cannot establish a statistically reliable improvement.

### Questions that would need explicit decisions

Moving an integrated test ahead of the full draft changes the gated method. Giving 3D a role in the prototype revisits the current default. Grouping provenance labels changes citation display. Making rendered animation primary revisits the medium rule. Civilian viewpoints may require clarification of the rule that the camera only visits places the sources put the army. Archaeology and authored detail need a clear place in the evidence conventions.

All remain open for consideration. No new task, installation, procurement or build follows automatically from this document.

### How this input could be used

When Tony returns to a chapter decision, choose the idea most likely to help that chapter and identify the smallest convincing test. Preserve the first complete release as the delivery goal. A functioning Crossing would still leave the battle interaction to be proved, potentially at Cannae, before broader expansion.

The purpose of these proposals is to widen the available choices without making the project harder to finish. Keep the pieces that improve understanding or enjoyment enough to justify their continuing cost.

<!-- pagebreak -->

## Sources and reading status

### Project records reviewed

**1. Project authority and intent.** [The March Notion hub](https://app.notion.com/p/3b72ada87f88812b8bb4ef724a2e3cda), its Chapter Tracker, Decision Log and Source Log; local [BRIEF.md](/Users/tonyweber/Projects/the-march/BRIEF.md), [PLAN.md](/Users/tonyweber/Projects/the-march/PLAN.md) and [STATE.md](/Users/tonyweber/Projects/the-march/STATE.md). The reviewed records place The Crossing at P1 after its P0 gate. The hub’s thirteen-chapter description and the twelve local chapter folders remain an existing discrepancy, not resolved here.

**2. Accuracy and design.** [Canonical Notion conventions](https://app.notion.com/p/3b72ada87f88815ca4f6db741797f0de) and [local conventions v1.0](/Users/tonyweber/Projects/the-march/docs/conventions-v1.0.md). These remain authoritative over suggestions in this document.

**3. Build method and coordination.** [Build plan v1.0](/Users/tonyweber/Projects/the-march/docs/build-plan-v1.0.md), [CLAUDE.md](/Users/tonyweber/Projects/the-march/CLAUDE.md), [LOG.md](/Users/tonyweber/Projects/the-march/LOG.md) and the local hook configuration. Source pointers already show some drift between older Notion records and the migrated local research library.

**4. Crossing evidence.** [Claims ledger](/Users/tonyweber/Projects/the-march/data/content/02/claims-ledger.md), including local boats, clothing and supplies, the Rhone crossing and the Alpine descent. Route-candidate attributions still need the verification specified in the project record.

**5. Visual and terrain work.** The prototype page, Direction B samples and [3D measurements](/Users/tonyweber/Projects/the-march/site/poc/2p5d-options/scene-3d/MEASUREMENTS.md). Asset measurements and visual inspection are not reader tests or device-performance validation.

**6. Research library.** [Local source index](/Users/tonyweber/Claude/research/carthaginian-conflicts/index.md), with 149 indexed records. This is an inventory, not a claim that every entry contains a complete, verified source. The daily-life entry inspected was empty; the Fronda record contained an abstract and related material. A source’s presence in the inventory does not make it ready for a scene.

### External references checked during the discussion

**7. Tools and cost.** [Blender](https://www.blender.org/); [Three.js animation example](https://threejs.org/examples/webgl_animation_skinning_morph.html); [SVG documentation](https://developer.mozilla.org/en-US/docs/Web/SVG); [Netlify pricing](https://www.netlify.com/pricing/); [Codex project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md); [Claude Code memory and instructions](https://code.claude.com/docs/en/memory). Product details and prices can change.

**8. Historical and cultural leads.** [Fronda at Cambridge](https://www.cambridge.org/core/books/between-rome-and-carthage/AF20772D2B328FD83D113B6383A5E2F6); [Livy 22.7 at Perseus](https://www.perseus.tufts.edu/hopper/text?doc=Perseus%3Atext%3A1999.02.0144%3Abook%3D22%3Achapter%3D7); [British Museum coin record](https://www.britishmuseum.org/collection/object/C_1931-0103-2); [UNESCO Carthage](https://whc.unesco.org/en/list/37); [Met Turner commentary](https://www.metmuseum.org/exhibitions/listings/2008/j-m-w-turner/photo-gallery). These support the stated research directions. Full passages, dating, relevance and asset permissions need checking before production use.

The project review did not include a complete audit of the historical corpus, a completed 3D build or comparative user testing. Effort assessments are relative judgments. The proposed benefits remain hypotheses until the work is made and tried.
