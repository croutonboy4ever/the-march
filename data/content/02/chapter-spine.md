# Chapter 02, The Crossing: Chapter Spine (P1 beat sheet)

Built 2026-09-16 against `specs/the-crossing-spine.md` (frozen 2026-09-16). Structure only, no prose.
Every beat draws on `claims-ledger.md` (TC ids) and, for the pass debate, `route-candidates.md` (R1 to R7, all inferred modern scholarship).
Status: built 2026-09-16. Reviewer subagent run (criteria 1 to 9 pass; its findings applied). Awaiting Astra's independent review (criterion 10). The P1 gate is not passed.

## Legend

| Field | Values |
|---|---|
| Scale | **campaign** (Rhone to Po, whole corridor) · **regional** (one stretch, tens of km) · **ground** (one spot: a bank, a gorge, a ledge) |
| Question type | **W** why the army is here · **P** how position shapes what happens · **S** what could plausibly be seen |
| Module | map move · held view · vignette (first person, imagined texture on an attested frame, per-detail markers) · disagreement scene (both accounts side by side, no default winner) |
| Interaction | a reader-initiated control beyond scrolling, or **quiet** (no interaction, allowed) |
| Camera | where the view sits, and the source that puts the army (or the named force) there |
| ⇄ | scale transition into this beat; triple and return consequence in the transitions table |

Pleiades ids below were checked against `data/geo/processed/pleiades-places-corridor.geojson`.

---

## Beats

### B1. Orientation: the army at the Rhone
- **TC:** TC-01
- **Reader sees:** the corridor from the sea to the Alps; the army at the Rhone where it runs as a single stream, four days' march from the sea.
- **Question (W):** where is the army, and what river stands between it and the Alps?
- **Module:** map move (campaign pull-in to the river) · **Interaction:** quiet (opening slot 1, orientation)
- **Geography:** Rhodanus (river) 148168; Alpes 783; crossing point shown as a river stretch, not a pin (its modern location is inferred from "four days from the sea")
- **Camera:** the Rhone crossing zone (Polybius 3.42)

### B2. Buying every boat ⇄
- **TC:** TC-02
- **Reader sees:** dugout canoes and wherries bought from the river people, more being built, two days to an ample fleet.
- **Question (S):** what would the bank have looked like as the fleet was gathered?
- **Module:** held view · **Interaction:** quiet (opening slot 2, one concrete situation)
- **Geography:** Rhodanus bank at the crossing zone (corridor feature, unlocated stretch)
- **Camera:** crossing-zone bank (Polybius 3.42)

### B3. The five nights: Hanno's flank and the pincer ⇄
- **TC:** TC-03, TC-04
- **Reader sees:** Hanno's detachment marching 200 stades upstream on the third night, crossing on rafts at an island, then the smoke signal and the joint attack that routs the Gauls.
- **Question (P):** how does a force upstream turn a defended bank into an open one?
- **Module:** map move with a night-by-night stepper · **Interaction:** reader steps night 3 → night 5; the stepper carries Livy's timing ("next day", watches) against Polybius's fifth night as a sources-differ chip
- **Geography:** Rhodanus; the river island about 200 stades / ~25 miles upstream (relative distance along the river, no pinned island); the Gauls' camp on the far bank (unlocated)
- **Camera:** crossing zone and Hanno's line of march up the bank (Polybius 3.42–43, Livy 21.27–28); army identifier splits here (main army / Hanno's detachment, "chiefly Spaniards" per Livy)

### B4. First contact with Roman horse
- **TC:** TC-06
- **Reader sees:** 500 Numidian scouts against 300 Roman and Celtic horse; 140 Romans and Celts dead, more than 200 Numidians dead.
- **Question (P):** Roman horse is already within reach of the army's scouts; what does the first clash cost each side?
- **Module:** held view (casualty figures with anchor) · **Interaction:** quiet
- **Geography:** crossing zone at regional scale; the skirmish site is not in the ledger, so no site pin
- **Camera:** held on the crossing zone at regional scale; the skirmish site is not in the ledger, so the camera does not travel to it

### B5. Elephants on earthed rafts (candidate: Rhone raft construction, placed) ⇄
- **TC:** TC-05
- **Reader sees:** 37 elephants; rafts lashed to about 50 ft wide and run out about 200 ft into the stream, covered in earth; two females in front; some animals go into the river and reach the far bank.
- **Question (S):** what would the bank have looked like as the elephants went over?
- **Module:** held view with a sources-disagree affordance · **Interaction:** reader opens the side-by-side: escape by raised trunks (Polybius 3.46) vs "their weight kept them steady" and "various traditions" with no count (Livy 21.28)
- **Geography:** Rhodanus bank, crossing zone (unlocated stretch)
- **Camera:** crossing-zone bank (Polybius 3.46, Livy 21.28)

### B6. The consul finds an empty camp ⇄
- **TC:** TC-07
- **Reader sees:** Scipio reaching the crossing three days after Hannibal left, the lines abandoned; the army's marker three days up the river.
- **Question (W):** why is there no battle at the Rhone?
- **Module:** map move (time offset: two markers, three days apart) · **Interaction:** quiet
- **Geography:** Rhodanus crossing zone; the Rhone valley northward
- **Camera:** the abandoned camp, where both sources put Scipio's force (Polybius 3.49, Livy 21.32); then Hannibal's marker on the march

### B7. The Island: a succession quarrel settled ⇄
- **TC:** TC-08
- **Reader sees:** four days' march up to the land between the Rhone and the Isara; Hannibal backs the elder brother (Brancus, Allobroges, per Livy); the army is re-armed, re-clothed, re-shod and escorted to the foot of the pass.
- **Question (W):** why does the army stop here, and what does it gain?
- **Module:** map move, then held view · **Interaction:** quiet
- **Geography:** Isara (river) 167793; Rhodanus 148168; their confluence; Allobroges 167634
- **Camera:** the Island (Polybius 3.49); Livy 21.31 gives the event and the Allobroges, not the name "Island"

### B8. Two routes from the Island (standing disagreement 1, scene) ⇄
- **TC:** TC-09a, TC-09b; opens G-1
- **Reader sees:** two tracks leaving the Island. Polybius: up the river bank, 800 stades in ten days, then the ascent. Livy: a left turn through the Tricastini and Tricorii, along the Vocontii frontier, to the Druentia. Neither text names a pass; both tracks end in an open "ascent begins" envelope.
- **Question (W):** which way did the army go to reach the mountains?
- **Module:** disagreement scene · **Interaction:** reader toggles Polybius / Livy / both (default both, no track foregrounded)
- **Geography:** Polybius track: the river bank from the Island (which river is itself part of the debate; drawn as a corridor, labelled Polybius 3.50). Livy track: Tricorii 167940; Vocontii 148241; Druentia (river) 148069; Tricastini have no tribe-label id in the corridor extract (nearest is the later colony Col. Augusta Tricastinorum 167855, not their territory, so it is not used as a waypoint). Tribal territories render as areas labelled inferred-location.
- **Camera:** campaign scale over both tracks; it follows neither to a modern pass (conventions §6 and §7). G-1 opens here as a named open question and stays open.

### B9. Heights taken by night ⇄
- **TC:** TC-10
- **Reader sees:** the Allobroges holding the narrow passes by day; Hannibal taking the heights after dark; the day attack that throws pack animals over the cliffs; their town stormed for two or three days' corn and cattle.
- **Question (P):** how does holding the high ground decide who survives the defile?
- **Module:** held view · **Interaction:** quiet
- **Geography:** the first narrow passes of the ascent, modern location open (G-1); attested terrain type only (heights, defile, precipice); the town unlocated
- **Camera:** the ascent's opening defile as a place-unlocated view (Polybius 3.50–51, Livy 21.32–33); no candidate col's terrain is rendered as though it were the place

### B10. Garlands, then boulders
- **TC:** TC-11
- **Reader sees:** envoys with branches and garlands, hostages, two days of guidance; the ambush in a precipitous gorge with rolled stones. The van differs: baggage and cavalry (Polybius 3.53) vs elephants and cavalry (Livy 21.34). Hannibal with half the force passes the night near a white rock (Polybius only).
- **Question (P):** why does the order of march matter when the attack comes from above?
- **Module:** vignette (a fictional soldier in the rear infantry; attested frame, imagined texture, per-detail markers); the van difference shows as a sources-differ chip · **Interaction:** quiet
- **Geography:** a precipitous gorge and the "white rock" (leukopetron), both unlocated (G-1). The white rock is Polybius 3.53 only; Livy 21.34 has the night apart from cavalry and baggage and no rock.
- **Camera:** with the rear infantry in the gorge (Polybius 3.52–53, Livy 21.34); army identifier splits: Hannibal with half the force (Polybius 3.53) / Hannibal a night without his cavalry and baggage (Livy 21.34)

### B11. Ninth day: the head of the pass
- **TC:** TC-12
- **Reader sees:** the summit reached on the ninth day; two days encamped while stragglers and strayed animals come in.
- **Question (S):** what does the army look like when it finally stops climbing?
- **Module:** held view · **Interaction:** quiet
- **Geography:** the head of the pass, unlocated (G-1)
- **Camera:** the summit camp (Polybius 3.53, Livy 21.35); stragglers and strayed animals rejoin (TC-12)

### B12. Snow, and the plains of the Padus
- **TC:** TC-13
- **Reader sees:** the setting of the Pleiades near, snow thickening; Hannibal pointing to the plains of the Po and the direction of Rome (Livy adds the speech).
- **Question (S):** what could the men see from the top, and what were they told they were looking at?
- **Module:** held view · **Interaction:** quiet
- **Geography:** the head of the pass (unlocated); the Po plain as a direction, not a rendered vista. No Padus river id in the corridor extract. A rendered vista needs a located pass, which G-1 withholds, so any vista is candidate-specific and labelled as such (P3). World state is attested here: autumn, early snow (conventions §7).
- **Camera:** the summit (Polybius 3.54, Livy 21.35)

### B13. The descent kills as the ascent did
- **TC:** TC-14
- **Reader sees:** few enemies; a narrow, precipitous path; fresh snow over last winter's frozen snow; men and animals falling. Losses nearly as many as on the ascent, with no number given.
- **Question (P):** why is going down as deadly as coming up?
- **Module:** vignette (same fictional soldier; attested frame, imagined texture, per-detail markers) · **Interaction:** quiet
- **Geography:** the descent path, unlocated (G-1)
- **Camera:** on the descent path (Polybius 3.54–55, Livy 21.35–36)

### B14. The blocking rock (standing disagreement 2, scene)
- **TC:** TC-15a, TC-15b
- **Reader sees:** the column stopped at a broken ledge. Polybius: a landslip about a stade and a half long, a road cut into the cliff face, one day for horses and pack animals, three more days for the elephants. Livy: a sheer break of a thousand feet, felled trees fired against the rock, vinegar poured on, the stone split with iron, winding tracks, four days at the spot.
- **Question (P):** how does the army get past rock it cannot go around?
- **Module:** disagreement scene · **Interaction:** reader toggles Polybius / Livy / both; the method is what differs (cutting vs fire and vinegar); the time at the rock is four days in both
- **Geography:** the landslip on the descent, unlocated (G-1); attested dimensions only (a stade and a half long; a thousand feet deep)
- **Camera:** the ledge (Polybius 3.54–55, Livy 21.36–37)

### B15. Into Italy: which tribe, which pass (G-1 debate) ⇄
- **TC:** TC-18, TC-19; G-1; route-candidates R1–R7
- **Reader sees:** the army down on the Italian side. Polybius puts it among the Insubres; Livy puts it among the Taurini and argues from that against the Poenine Pass and Caelius's "heights of Cremo". Nepos names only the "Graian pass". Seven modern candidates are shown, all marked inferred, with backers where recorded (R5 and R7 have none) and the ancient anchors each backer cites.
- **Question (W):** where did the army come down, and why can nobody say which pass it crossed?
- **Module:** disagreement scene (debate, unresolved) · **Interaction:** reader taps a candidate to open its backers and anchors; no candidate is selected by default and none is drawn heavier
- **Geography:** Taurini 383794; Insubres have no tribe-label id in the corridor extract (the only match is Victumulae 383821, a settlement, not used); Poeninus 167871 (R5, which Livy 21.38 disputes); *Alpis Graia 167639 (R4; matching Nepos's "Graian" to this col is a modern identification, so inferred); R1 Traversette, R2 Clapier, R3 Montgenèvre, R6 Larche, R7 Mont Cenis rendered as candidates only
- **Camera:** campaign scale over the arc of candidates; it enters no candidate col (conventions §6)

### B16. The column comes down (candidate: column passage, placed) ⇄
- **TC:** TC-17a, TC-17b; anchors for the inference: TC-10, TC-14, TC-05
- **Reader sees:** the surviving army going by, seen from beside the line of march (an imagined vantage, labelled; the watcher is not a character and asserts nothing). Polybius: 12,000 Libyan and 8,000 Iberian foot and no more than 6,000 horse, from Hannibal's own column at Lacinium. Livy reports other writers' reckonings, from 20,000 foot and 6,000 horse up to 100,000 and 20,000, and Cincius's 80,000 and 10,000, which Livy rejects as counting Gauls and Ligurians; Cincius also has Hannibal losing 36,000 after the Rhone. The column's length is an inferred calculation with its anchors shown; pack-animal and elephant counts on arrival are shown as unknown.
- **Question (S):** what would it have looked like to watch this army pass?
- **Module:** held view with an inferred calculation panel · **Interaction:** reader switches between the figures (Polybius / lowest reckoning / highest reckoning / Cincius, rejected by Livy), each labelled with who gave it; the column length recomputes and every figure keeps its anchor
- **Geography:** the foot of the descent on the Italian side, labelled with both tribal readings (Insubres / Taurini); no road rendered (conventions §6)
- **Camera:** beside the arriving army (Polybius 3.56, Livy 21.38)
- **Dependency for P2:** the ledger holds no spacing basis for a marching column. P2 either pulls a named modern basis from the fact base, which then enters as inferred with its work named, or the length displays as unknown and the view shows only the attested components.

### B17. Fifteen days, five months ⇄
- **TC:** TC-16
- **Reader sees:** the full path at campaign scale: the Rhone, the Island, the two route tracks into the unresolved envelope, the Italian side. The passage took fifteen days and the march from New Carthage five months, with both sources agreeing.
- **Question (W):** what did the crossing cost in time, and where does it leave the army?
- **Module:** map move (full pull-back) · **Interaction:** quiet
- **Geography:** full corridor; the stretch from ascent to descent stays an envelope, not a line
- **Camera:** campaign scale (Polybius 3.56, Livy 21.38)

---

## Scale transitions

Each triple lists the phase or date, the army identifier, and the place reference. The last column gives what the reader sees change when the view returns to campaign scale.

| # | Beats | Direction | Phase | Army identifier | Place reference | Consequence on return to campaign scale |
|---|---|---|---|---|---|---|
| T1 | B1→B2 | campaign → ground | at the Rhone, the two boat-gathering days (TC-02) | Hannibal's army, whole | Rhone crossing point, single stream, four days from the sea | carried to T4 |
| T2 | B2→B3 | ground → regional | third night (Polybius) / first watch (Livy) to fifth night / "next day" | main army; Hanno's detachment splits off | crossing point + river island ~200 stades upstream | carried to T4 |
| T3 | B4→B5 | regional → ground | after the fifth-night crossing; elephants still on the near bank | Hannibal's army (reunited, far bank); 37 elephants | crossing point | carried to T4 |
| T4 | B5→B6 | ground → campaign | departure from the Rhone; Scipio +3 days | Hannibal's army; Scipio's consular force | crossing point → the Rhone valley northward | army and elephants across (TC-05); dead from the skirmish: 140 Romans and Celts, 200+ Numidians (TC-06); a Roman marker at the empty camp, three days behind (TC-07) |
| T5 | B6→B7 | campaign → regional | four days' march from the crossing | Hannibal's army | the Island, Rhodanus–Isara confluence | carried to T6 |
| T6 | B7→B8 | regional → campaign | leaving the Island | Hannibal's army, now escorted | the Island | army marker changes to re-armed, re-clothed, re-shod, with an escort to the foot of the pass (TC-08); no count shown, none attested |
| T7 | B8→B9 | campaign → ground | start of the ascent (Polybius: after 10 days / 800 stades; Livy: after the Druentia) | Hannibal's army | "the ascent", modern location open (G-1); the place label is the unresolved envelope from B8 and persists through B14 | carried to T8 |
| T8 | B14→B15 | ground → campaign | descent complete | Hannibal's army (B10's split closed; stragglers rejoined at the summit, TC-12) | foot of the descent: Insubres (Polybius) / Taurini (Livy) | pack animals lost over the cliffs, count unknown (TC-10); descent losses near those of the ascent, unquantified (TC-14); elephants past the rock (TC-15a/b); the envelope stays unresolved |
| T9 | B15→B16 | campaign → ground | arrival in Italy | Hannibal's army "as survived" (TC-17a) | foot of the descent, both tribal readings | carried to T10 |
| T10 | B16→B17 | ground → campaign | passage complete: 15 days; 5 months from New Carthage | Hannibal's army | the Italian side, both tribal readings | arrival strength on the army marker with every figure and anchor (TC-17a, TC-17b), including Cincius's 36,000 lost after the Rhone; no single figure is promoted |

No transition: B3→B4 (regional), B9→B14 (ground, one unlocated place reference throughout).

## Opening three beats

| Slot | Beat | Shape | Interaction |
|---|---|---|---|
| 1 | B1 | orientation | quiet |
| 2 | B2 | one concrete situation | quiet |
| 3 | B3 | one interaction | night stepper |

Quiet beats (marked above): B1, B2, B4, B6, B7, B9, B10, B11, B12, B13, B17.

## Candidate beats

| Candidate | Disposition | Reason (one line) |
|---|---|---|
| Rhone raft construction | **Placed as B5**, held view with an in-beat sources-disagree affordance, not a standalone disagreement scene | The two accounts agree on the raft (about 200 by 50 ft, earthed, females leading) and differ only on the count and on how fallen elephants reached shore, which is too narrow a difference to carry a scene. |
| Roadside column passage | **Placed as B16**, held view with an inferred calculation, anchors shown | The ledger holds army strength only on arrival (TC-17a/b), so the view sits at the foot of the descent where figures, camera and army coincide; no road is rendered, and the length waits on a named spacing basis (P2 dependency). |

## Standing disagreements and G-1

| Item | Where | How it lands |
|---|---|---|
| Route: TC-09a vs TC-09b | B8 | own disagreement scene, both tracks, no default |
| Blocking rock: TC-15a vs TC-15b | B14 | own disagreement scene, both methods and day counts, no default |
| G-1: which modern pass | opens B8, carried as the unlocated place reference B9–B14, debated B15 | open debate; seven candidates, none selected; ancient arguments (Livy 21.38, Nepos 3.4) separate from modern (R1–R7, inferred) |
| Also shown in-beat (not standing) | B3 timing, B5 elephants, B10 white rock, B15 tribe, B16 numbers | both readings and anchors visible; army strength is a named debate (conventions §2) |

## TC coverage

| TC | Beat | TC | Beat | TC | Beat |
|---|---|---|---|---|---|
| 01 | B1 | 09a | B8 | 15b | B14 |
| 02 | B2 | 09b | B8 | 16 | B17 |
| 03 | B3 | 10 | B9, B16 anchor | 17a | B16 |
| 04 | B3 | 11 | B10 | 17b | B16 |
| 05 | B5, B16 anchor | 12 | B11 | 18 | B15 |
| 06 | B4 | 13 | B12 | 19 | B15 |
| 07 | B6 | 14 | B13, B16 anchor | G-1 | B8, B15 |
| 08 | B7 | 15a | B14 | | |

No beat is imagined-only. Imagined elements: the B10 and B13 vignettes (texture on attested frames) and the B16 vantage (labelled, claim-free).

## Carried forward (not decided here)

| For | Item |
|---|---|
| P2 | B16 column-spacing basis: a named modern work from the fact base, or length shown as unknown |
| P0 addition (needs a CHANGES row) | Polybius 3.60, confirmed verbatim this session in fact-base source 116: 38,000 infantry and more than 8,000 cavalry when Hannibal crossed the Rhone, "nearly half" lost in the pass. Not in the ledger, so no beat uses it. If added, it gives B5/T4 a strength at the Rhone and T10 an attested loss, and B16 could move to the Rhone |
| P0 addition | TC-06 unit sizes: the 500 Numidians (Polybius 3.44) and the 300 Roman horse with Celtic guides (Polybius 3.41) confirmed verbatim this session in source 116; the ledger's supporting text quotes only the casualties |
| P2 | B15 candidate anchors come from `route-candidates.md`, still marked "to be spot-checked"; each is confirmed against the fact base before display |
| P3 | How ground-scale views render where the place is unlocated (B9–B14) without inventing terrain (conventions §6) |
| P3 | B12 vista: candidate-specific and labelled, or directional only |
| P3 | Crossing point, skirmish site and the Island's extent are stretches or areas, not pins; Insubres, Tricastini and the Padus lack label ids in the corridor extract |
