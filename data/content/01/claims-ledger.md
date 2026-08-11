# Chapter 01 — The Crossing: Claims Ledger

The evidentiary backbone for chapter one (Hannibal's crossing of the Rhone and the
Alps). Every claim the chapter rests on is recorded here with its provenance marker,
its source, the verbatim supporting text, when it was retrieved, and any source that
contradicts it. The chapter's preflight gate (conventions v1.0 §9) checks against this
ledger.

## Why this ledger exists (SD-13)

Standing Decision SD-13 (Notion "Canonical: Standing Decisions"): a NotebookLM chat
answer is a **lead, not a source**. It is a model-generated summary, and its citation
offsets can point to the wrong passage of the right source. So no claim here is
recorded from a chat answer. The chat answer only tells us *where to look*; the
supporting text below is then pulled verbatim with `source_read` and confirmed to say
what the claim says before it is written down. This supersedes the older practice
(see `../02/route-candidates.md`) of attributing to a corpus query with locators left
"to be spot-checked at preflight."

## Fact base

- Notebook: **Carthaginian Conflicts** (`f1b5cae8-7652-4e4e-9ae0-d6bf8f74d3e8`), 149 sources.
- Ancient primary texts used for this chapter:
  - **Polybius**, *Histories* (Shuckburgh trans., Gutenberg Vol. I) — `afc8c222-7f8d-4ea6-af7e-bd290815b984`. Book III chs. 42–56 carry the whole crossing.
  - **Livy**, *History of Rome* Books XXI–XXV (Edmonds trans., scanned pdf) — `abe8d234-1163-4918-95da-494dee9cfba3`. Book XXI carries the crossing. OCR text; quotes transcribed faithfully, line-break hyphenation joined, words unchanged.
  - **Cornelius Nepos**, *Life of Hannibal* (Latin text + notes) — `46d26c93-2f36-4ad5-99dd-305f89692f36`. One sentence, ch. 3.4.
- Markers are the three canonical ones in `docs/conventions-v1.0.md` §1: **attested**
  (present in the ancient sources, carries a source anchor), **inferred** (reasoned
  from attested material, names its basis), **imagined** (invented texture, claim-free,
  never recorded here with a source because it asserts no fact).
- Attested means attested in the **ancient** sources only. Modern scholarship (e.g. any
  identification of *which* modern pass) enters as **inferred**, with the modern work
  named (conventions §3). See the gap list for the pass identification.

## Method (per claim) — as actually run 2026-08-11

1. **Source-scoped ask, one ancient author at a time.** `chat_ask` scoped with
   `source_ids` to a single author. Run: Polybius (scoped to `afc8c222`); Livy (scoped
   to the Livy XXI–XXV pdf `abe8d234`); Nepos (scoped to the two Nepos sources).
2. **Ask for contradictions.** A dedicated cross-author ask (scoped to Livy + Nepos +
   Appian, excluding Polybius) for where those sources differ from Polybius on the
   descent-rock, the numbers, the days, and the route. Disagreement is recorded as
   content (conventions §2), not resolved.
3. **Pull supporting text with `source_read`, not the chat answer.** Each full source
   body was paged into a local file and every recorded quote was located **by content
   search** in that text, then transcribed verbatim.
4. **Confirm the snippet (known-defect workaround).** Returned citation offsets were in
   fact **null** (`start_char`/`end_char` = None), so offsets could not be trusted at
   all — every quote below was confirmed present in the source by string match, and read
   in context to confirm it supports the claim. Nothing was copied from a chat answer.

**Scoping caveat discovered this session (recorded for the next run):** the source
titled *"...The History of Rome; Books Nine to Twenty-Six..."* (`539a6fd4`) does **not**
contain Book XXI — it is actually a translation of Books XXVII–XXXVI. A Livy ask scoped
to it returned an **ungrounded** answer (zero citations); nothing from it was recorded.
The real Book XXI text is the `abe8d234` pdf. Use `abe8d234` for Book XXI.

## Session-health note (known defect, hit live this session)

The NotebookLM session had **expired** at the start of this run: `server_info` reported
`auth.authenticated: true` while `account.available` was **false** ("unauthenticated"),
and a real `notebook_describe` failed. Ground truth is **`account.available`**, not
`auth.authenticated`. After re-auth (`notebooklm login`), `account.available` returned
true and asks succeeded. Every working session for this ledger must confirm
`account.available: true` before the first ask.

## Schema

Each claim is one entry: **Claim / Marker / Source ID (+ anchor) / Supporting text
(verbatim) / Retrieved / Contradicting sources.** For inferred, the Source ID is the
attested basis; for imagined, "n/a (claim-free)". "Contradicting sources" names any
corpus source giving a different account with its own anchor, or "none found in corpus".

---

## Claims (narrative order)

### TC-01 — The Rhone crossing point
- **Claim:** Hannibal reached the Rhone where it flowed in a single stream, about four days' march from the sea.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.42
- **Supporting text:** "Meanwhile Hannibal had reached the river and was trying to get across it where the stream was single, ... at a distance of four days' march from the sea."
- **Retrieved:** 2026-08-11
- **Contradicting sources:** none found in corpus.

### TC-02 — Assembling the boats
- **Claim:** He bought the natives' dugout canoes and wherries and had them build more, so that within two days he had an ample supply of transports.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.42
- **Supporting text:** "purchased from them all their canoes of hollow trunks, and wherries ... and so in two days had an innumerable supply of transports, every soldier seeking to be independent of his neighbour".
- **Retrieved:** 2026-08-11
- **Contradicting sources:** none found in corpus.

### TC-03 — Hanno's flanking crossing
- **Claim:** On the third night Hannibal sent a detachment under Hanno son of Bomilcar 200 stades upstream, where they crossed on hastily built rafts at a river island and took position behind the hostile Gauls.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.42
- **Supporting text:** "on the third night, sent forward a detachment ... under the command of Hanno, the son of the Suffete Bomilcar. ... This force marched up stream along the bank for two hundred stades, until they arrived at a certain spot where the stream is divided by an eyot ... and on these they crossed in safety, without any one trying to stop them."
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.27, `abe8d234`, confirmed verbatim):** "Hannibal ordered Hanno, son of Bomilcar, to go with part of the army, chiefly Spaniards, one day's march up the stream, starting at the first watch of the night ... The Gallic guides ... told him that, about twenty-five miles higher up, the river encircled a little island, and could be crossed at the point of division, where the channel was broader and consequently shallower." [OCR pdf]
- **Contradicting sources:** Livy's ~25 miles equals Polybius's 200 stades (about 25 Roman miles), so the interval agrees; Livy specifies the detachment as "chiefly Spaniards".

### TC-04 — The fifth-night pincer routs the Gauls
- **Claim:** On the fifth night the two forces attacked together: Hanno's men fired the Gauls' camp from behind while Hannibal crossed, and the barbarians, caught unformed, were put to flight.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.43
- **Supporting text:** "the barbarians, without forming their ranks, poured out of their entrenchments in scattered groups ... having no time to form their ranks, and being taken by surprise, were quickly repulsed and put to flight."
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.27–28, `abe8d234`, confirmed verbatim):** "Next day they advanced, and showed by some smoke from an eminence that they had crossed and were not far off. Hannibal seeing this ... gave the signal for crossing ... a yet more appalling din fell on their ears from the rear, where Hanno had taken their camp ... The Gauls ... broke through where the way seemed most open, and fled in wild panic to their villages." [OCR pdf]
- **Contradicting sources:** none on the outcome. Timing differs: Livy dates the flanking march by watches and puts the joint attack "next day", where Polybius specifies the fifth night.

### TC-05 — The thirty-seven elephants
- **Claim:** Hannibal had thirty-seven elephants; they were ferried across on earth-covered rafts about fifty feet wide reaching some two hundred feet into the stream, led by two females; some panicked into the river but reached the far bank by raising their trunks to breathe.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.42 (count), 3.46 (method)
- **Supporting text:** "his chief difficulty was in getting the elephants across, of which he had thirty-seven." / "They made a number of rafts strongly compacted ... so as to form combined a breadth of about fifty feet ... These combined rafts stretching about two hundred feet across the stream ... they threw a great deal of earth upon all the rafts ... putting two females in front whom the others obediently followed ... though their Indian riders were drowned, the animals themselves got safe to land, saved by the strength and great length of their probosces".
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.28, `abe8d234`, confirmed verbatim):** "there are various traditions how it was accomplished ... A raft two hundred feet long and fifty broad was extended from the bank into the water ... covered like a bridge with a layer of earth ... the elephants were driven, the females taking the lead ... Some in their fury fell off into the stream, but their weight kept them steady, and ... feeling their way into shallow water they reached land." [OCR pdf]
- **Contradicting sources:** Livy gives no count (the thirty-seven is Polybius's) and a different escape mechanism — the elephants' "weight kept them steady", not Polybius's raised trunks; Livy expressly flags "various traditions".

### TC-06 — Cavalry skirmish with Scipio's scouts
- **Claim:** A 500-strong Numidian reconnaissance party clashed with Scipio's 300 Roman/Celtic horse; the Romans and Celts lost 140 men, the Numidians more than 200.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.44–45
- **Supporting text:** "the Romans and Celts lost a hundred and forty men, and the Numidians more than two hundred."
- **Retrieved:** 2026-08-11
- **Contradicting sources:** none found in corpus.

### TC-07 — Scipio arrives three days late
- **Claim:** The consul Publius Cornelius Scipio reached the Rhone crossing about three days after Hannibal had left it, and found the enemy gone.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.49
- **Supporting text:** "Three days after Hannibal had resumed his march, the Consul Publius arrived at the passage of the river. He was in the highest degree astonished to find the enemy gone".
- **Retrieved:** 2026-08-11
- **Contradicting sources:** none — Livy 21.32 (`abe8d234`) **concurs (confirmed):** "About three days after Hannibal had moved from the Rhone, the consul Publius Cornelius reached the enemy's camp ... Seeing, however, that the lines were abandoned and that the enemy must be too far ahead".

### TC-08 — "The Island" and the dynastic intervention
- **Claim:** Four days' march up from the Rhone, at the confluence of the Rhone and the Isara (Isère) — "the Island" — Hannibal settled a succession quarrel in favour of the elder brother, and was rewarded with fresh weapons, clothing and boots and an escort to the foot of the pass.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.49
- **Supporting text:** "after four days' march from the passage of the Rhone, Hannibal arrived at the place called the Island ... the Rhone and Isara flowing on either side of it ... he found two brothers engaged in a dispute for the royal power ... The elder sought his alliance ... he consented ... exchanged all their old and damaged weapons for new ones ... gave most of the men new clothes and boots ... he acted with his army as their rear-guard, and secured them a safe passage as far as the foot of the pass."
- **Retrieved:** 2026-08-11
- **Contradicting sources:** Livy 21.31 (`abe8d234`) **agrees on the event and adds a name (confirmed):** the elder brother is **Brancus**, and the tribe is the **Allobroges** — "Two brothers were contending for the throne. The elder, who had previously been king, Brancus by name ... Hannibal ... restored the elder brother to power". Polybius leaves the brother unnamed.

### TC-09a — Route to the ascent (Polybius)
- **Claim:** From the Island Hannibal continued up the river bank, covering 800 stades in ten days, then began the ascent of the Alps.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.50
- **Supporting text:** "Having in ten days' march accomplished a distance of eight hundred stades along the river bank, Hannibal began the ascent of the Alps".
- **Retrieved:** 2026-08-11
- **Contradicting sources:** **Livy 21.31 (TC-09b)** gives a different route — a standing route debate (conventions §2). See `../02/route-candidates.md`.

### TC-09b — Route to the ascent (Livy)
- **Claim:** Livy has Hannibal leave the Rhone and turn left, marching through the Tricastini, then the Tricorii, along the frontier of the Vocontii, to the river Druentia (Durance).
- **Marker:** attested
- **Source ID:** `abe8d234` — Livy 21.31
- **Supporting text:** "Having composed the feuds of the Allobroges, Hannibal marched towards the Alps, not, however, pursuing a direct course, but turning leftwards to the country of the Tricastini, from which again he passed to that of the Tricorii, along the extreme frontier of the Vocontii, a route at no point embarrassing till he reached the river Druentia." [OCR pdf]
- **Retrieved:** 2026-08-11
- **Contradicting sources:** **Polybius 3.47–50 (TC-09a)** keeps Hannibal marching up-river (the Isère/northern line). The two routes are the core Alpine-route debate; neither ancient text names the modern pass. See gap G-1.

### TC-10 — Allobroges hold the heights; the captured town
- **Claim:** The Allobroges seized the narrow high passes; Hannibal, learning they left the heights at night, took the positions by dark, beat off the day attack that hurled many pack animals over the cliffs, and stormed their near-empty town, taking two or three days' provisions.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.50–51
- **Supporting text:** "the chiefs of the Allobroges collected large numbers of their tribe and occupied the points of vantage ... he ... seized on the spots which had been previously occupied by the enemy ... large numbers of the beasts of burden were hurled down the precipices with their loads on their backs ... he got a supply of corn and cattle sufficient for two or three days".
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.32–33, `abe8d234`, confirmed verbatim):** "he had a multitude of fires lit for show ... taking with him some lightly armed men, the bravest he could pick, he rapidly mounted the passes and established himself on the very hills which the enemy had occupied ... The pressure, too, in the defile, each side of which was a sheer precipice, hurled numbers down to an immense depth ... Next he took a fortress, the capital of the district ... and fed his troops for three days on the corn and cattle he had seized." [OCR pdf]
- **Contradicting sources:** none found in corpus (Polybius and Livy agree on the night seizure, the day attack, and the captured town with three days' provisions).

### TC-11 — The treacherous guides and the gorge
- **Claim:** Tribesmen who met the army with branches and garlands and gave hostages guided it for two days, then ambushed it in a precipitous gorge with rolled boulders; Hannibal had put baggage and cavalry in the van and heavy infantry in the rear, and passed the night by a "white rock".
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.52–53
- **Supporting text:** "They guided the army for two days: and then these tribes ... attacked them just as they were passing through a certain difficult and precipitous gorge ... he had placed his baggage and cavalry in the van and his hoplites in the rear ... Hannibal with half his force was obliged to pass the night near a certain white rock".
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.34, `abe8d234`, confirmed verbatim):** "Some old men, governors of the fortresses, came to him as envoys ... they begged him to accept supplies, guides for his march, and hostages ... His van was formed of the elephants and cavalry, while he marched himself in the rear with the main strength of the infantry ... The moment they entered a narrow pass ... the barbarians sprang out of their ambuscades ... rolling down huge stones upon the army ... One night he had to pass without his cavalry and his baggage." [OCR pdf]
- **Contradicting sources:** correction on earlier verbatim confirmation — the "white rock" (*leukopetron*) is **Polybius's** detail only (3.53). Livy 21.34 records the night separated from cavalry and baggage but names **no** white rock; the earlier note that Livy shared it came from an ungrounded chat answer and is withdrawn.

### TC-12 — The summit reached on the ninth day
- **Claim:** On the ninth day's march Hannibal reached the head of the pass and encamped there two days to rest the men and let stragglers and stray animals catch up.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.53
- **Supporting text:** "The ninth day's march brought him to the head of the pass: and there he encamped for two days, partly to rest his men and partly to allow stragglers to come up."
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.35, `abe8d234`, confirmed verbatim):** "On the ninth day they reached the top of the Alps, passing for the most part over trackless steeps ... Two days they encamped on the height, and the men, worn out with hardships and fighting, were allowed to rest."
- **Contradicting sources:** none found in corpus (Polybius and Livy agree: ninth day to the summit, a two-day halt).

### TC-13 — The setting of the Pleiads and the view of Italy
- **Claim:** With the setting of the Pleiads near and snow thickening, Hannibal rallied his men by pointing to the plains of the Padus (Po) below and the direction of Rome.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.54
- **Supporting text:** "it being nearly the period of the setting of the Pleiads, the snow was beginning to be thick on the heights ... By pointing therefore to the plains of the Padus ... and at the same time indicating the direction of Rome itself, he did somewhat to raise the drooping spirits of his men."
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.35, `abe8d234`, confirmed verbatim):** "a fall of snow coming with the setting of the Pleiades added to their sufferings a terrible fear ... Hannibal ... pointed to Italy and to the plains round the Po, as they lay beneath the heights of the Alps, telling his men, ''Tis the walls not of Italy only but of Rome itself that you are now scaling.'" [OCR pdf] Livy adds the direct speech; both place the address at the summit with the Pleiades setting.
- **Contradicting sources:** none found in corpus. *(The Shuckburgh margin glosses this "9th November"; that date is an editor's note, not Polybius's text, so it is not recorded as attested.)*

### TC-14 — The killing descent
- **Claim:** On the descent Hannibal met few enemies but lost nearly as many men as on the ascent to the ground and snow: fresh soft snow lay over old frozen snow, and to slip from the narrow path meant falling down the precipices.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.54–55
- **Supporting text:** "from the dangerous ground and the snow he lost almost as many men as on the ascent. For the path down was narrow and precipitous ... the present fall of snow coming upon the top of that which was there before, and had remained from the last winter".
- **Retrieved:** 2026-08-11
- **Also attested (Livy 21.35–36, `abe8d234`, confirmed verbatim):** "the whole way was precipitous, narrow, and slippery, so much so that they could not keep themselves from falling ... they tumbled one over another and the beasts of burden over the men." [OCR pdf]
- **Contradicting sources:** none found in corpus.

### TC-15a — The blocking rock: Polybius (carving)
- **Claim:** A path narrowed by a landslip "about a stade and a half" long stopped the column; Hannibal carved a road out of the cliff face — one day's work opened it for horses and pack animals, three more days of labour got the elephants across.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.54–55
- **Supporting text:** "narrowed before by landslips extending about a stade and a half ... he encamped upon the ridge ... began constructing a road on the face of the precipice. One day's work sufficed to make a path practicable for beasts of burden and horses ... and after three days' difficult and painful labour he got his elephants across".
- **Retrieved:** 2026-08-11
- **Contradicting sources:** **Livy 21.37 (TC-15b)** — Livy has a fire-and-vinegar method absent from Polybius. A standing source disagreement (conventions §2).

### TC-15b — The blocking rock: Livy (fire and vinegar)
- **Claim:** In Livy the blocking landslip had "been broken away sheer to a depth of a thousand feet"; the soldiers heaped and fired great felled trees against the rock, then poured vinegar on the heated stone to crack it, cleaved it with iron tools, and cut winding tracks down; four days were spent at the pass.
- **Marker:** attested
- **Source ID:** `abe8d234` — Livy 21.36 (the obstacle), 21.37 (the method)
- **Supporting text:** (21.36) "now by a recent landslip had been broken away sheer to a depth of a thousand feet". (21.37) "they heaped up a huge pile of wood from great trees ... they lighted the pile, and melted the rocks, as they heated, by pouring vinegar on them. The burning stone was cleft open with iron implements, and then they relieved the steepness of the slopes by gradual winding tracks, so that even the elephants ... could be led down. Four days were spent in this rocky pass". [OCR pdf]
- **Retrieved:** 2026-08-11
- **Contradicting sources:** **Polybius 3.55 (TC-15a)** describes only carving the road and makes no mention of fire or vinegar. The fire-and-vinegar episode is Livy's; treat as a named debate, not fact.

### TC-16 — Fifteen days over the Alps, five months from New Carthage
- **Claim:** The passage of the Alps took fifteen days; the whole march from New Carthage took five months.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.56
- **Supporting text:** "The whole march from New Carthage had occupied five months, the actual passage of the Alps fifteen days".
- **Retrieved:** 2026-08-11
- **Contradicting sources:** none — Livy 21.38 (`abe8d234`) **concurs (confirmed):** "the passage of the Alps having occupied fifteen days", in the fifth month from New Carthage. (A rare point of full agreement.)

### TC-17a — Army on arrival: Polybius (the Lacinian column)
- **Claim:** Hannibal entered the Po valley and the territory of the Insubres with 12,000 Libyan and 8,000 Iberian infantry and not more than 6,000 cavalry — figures Hannibal himself recorded on the bronze column at the Lacinian promontory.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.56
- **Supporting text:** "he now boldly entered the valley of the Padus, and the territory of the Insubres, with such of his army as survived, consisting of twelve thousand Libyans and eight thousand Iberians, and not more than six thousand cavalry in all, as he himself distinctly states on the column erected on the promontory of Lacinium".
- **Retrieved:** 2026-08-11
- **Contradicting sources:** **Livy 21.38 (TC-17b)** reports a wide spread of figures. Army-strength numbers are a named standing debate (conventions §2, §4).

### TC-17b — Army on arrival: Livy (historians disagree)
- **Claim:** Livy reports that the sources disagree: the highest figure is 100,000 infantry and 20,000 cavalry, the lowest 20,000 infantry and 6,000 cavalry (matching Polybius); Cincius Alimentus gave 80,000 and 10,000 (which Livy rejects as confused by counting Gauls and Ligurians), and reports Hannibal told Cincius he lost 36,000 men after crossing the Rhone.
- **Marker:** attested
- **Source ID:** `abe8d234` — Livy 21.38
- **Supporting text:** "The highest reckoning [is] a hundred thousand infantry and twenty thousand cavalry; the lowest twenty thousand infantry and six thousand cavalry. Cincius Alimentus ... would have the greatest weight with me, did he not confuse the numbers by adding the Gauls and Ligurians. Including these there arrived eighty thousand infantry and ten thousand cavalry ... Cincius says that Hannibal himself told him that, after crossing the Rhone, he lost thirty-six thousand men". [OCR pdf]
- **Retrieved:** 2026-08-11
- **Contradicting sources:** **Polybius 3.56 (TC-17a)** gives the firm 20,000 foot / 6,000 horse from the Lacinian column, which is Livy's "lowest" reckoning.

### TC-18 — The first tribe reached in Italy
- **Claim:** Polybius has Hannibal descend among the Insubres; Livy has the Taurini, "a half Gallic race", as the first tribe on the Italian side.
- **Marker:** attested
- **Source ID:** `afc8c222` — Polybius 3.56; `abe8d234` — Livy 21.38
- **Supporting text:** (Polybius) "the territory of the Insubres". / (Livy) "The tribe that he first encountered on his descent into Italy were the Taurini, a half Gallic race. About this all agree". [Livy OCR pdf]
- **Retrieved:** 2026-08-11
- **Contradicting sources:** the two are recorded together above; this is part of the route/descent debate (Livy's Taurini implies the more southerly descent).

### TC-19 — The pass named (Nepos)
- **Claim:** Nepos names the pass only as the "Graian pass" (*saltus Graius*), which he links to the tradition that Hercules Graius had crossed there, and says Hannibal cut down the "Alpine inhabitants" who tried to bar him, opened the region and made roads passable even for a laden elephant.
- **Marker:** attested
- **Source ID:** `46d26c93` — Cornelius Nepos, *Life of Hannibal* 3.4
- **Supporting text:** "Ad Alpés posteaquam venit, quae Italiam ab Gallia seiungunt, quas nemo umquam cum exercitu ante eum praeter Herculem Graium transierat, quo facto is hodié saltus Graius appellatur, Alpicos conantés prohibére transitu concidit; loca patefécit, itinera muniit, effecit, ut ea elephantus Ornatus ire posset, qua antea unus homo inermis vix poterat répere. Hac copias traduxit in Italiamque pervenit." [OCR accents as scanned] — "After he came to the Alps ... which no one before him had ever crossed with an army except the Greek Hercules — whence the pass is today called the Graian pass — he cut down the Alpine tribes trying to prevent his crossing; he opened the region, built up the roads, and made it possible for a laden elephant to go where before a single unarmed man could scarcely crawl."
- **Retrieved:** 2026-08-11
- **Contradicting sources:** the pass identification is itself contested — Livy 21.38 (`abe8d234`) explicitly disputes the Poenine Pass and Caelius Antipater's "heights of Cremo": "the vulgar belief that he marched over the Poenine Pass ... I wonder, too, that Caelius says that he crossed by the heights of Cremo. Both these passes would have brought him, not to the Taurini, but ... to the Libuan Gauls." Polybius names no pass. See gap G-1.

## Coverage notes (checked, thin or silent)

- **Nepos** (`46d26c93`, 3.4) compresses the whole crossing into the one sentence at
  TC-19 and **omits** the route detail, the mountain tribes by name, the descent, the
  number of days, and every troop figure. Confirmed by reading ch. 3 in the source.
- **Appian**, *Punic Wars* ch. I (`2fc38d88`) is **silent** on Hannibal's Alpine
  crossing (that chapter concerns the African/Carthaginian context; Appian's *Hannibalic
  War* is not in the corpus). The contradiction ask scoped to include Appian returned
  nothing on the crossing.
- **Polybius** states he crossed the Alpine pass himself (3.48: "gone over the Alpine
  pass myself"), which is why the experience narrative leans on him first; recorded here
  as a source-authority note, not a chapter claim.

---

## Unverified claims (gap list)

Per the chapter-one directive: a claim with no retrievable supporting text is **kept
here as unverified rather than dropped**, so the gap stays visible (conventions §9(6):
gaps shown as gaps).

### G-1 — Which modern pass (route identification)
- **Would-be claim:** that Hannibal's pass is a specific modern col (Little St Bernard /
  Mont Genèvre / Col de la Traversette / Clapier, etc.).
- **Marker it would carry:** **inferred** (modern scholarship) — never attested. The
  ancient texts do not settle it: Polybius names no pass; Livy (21.38) only rules out
  the Poenine Pass and the "heights of Cremo" and puts the first tribe as the Taurini;
  Nepos (3.4) says only "the Graian pass".
- **Status:** open debate, not a fact. Already carried as candidates in
  `../02/route-candidates.md` (R1–R7). The chapter must present it as a debate, not
  resolve it (conventions §2, §6).

### G-2 — Livy's parallel crossing chapters (RESOLVED 2026-08-11)
- Livy's parallel accounts — the Rhone crossing (21.27–28), the elephants (21.28), the
  night seizure and captured town (21.32–33), the treacherous guides and the night
  without cavalry/baggage (21.34), the ninth-day summit and the address showing Italy
  (21.35), and the descent and landslip (21.35–36) — were pulled verbatim from
  `abe8d234` by content search and are now recorded as **attested-Livy** on the relevant
  entries (TC-03, TC-04, TC-05, TC-10, TC-11, TC-12, TC-13, TC-14, TC-15b), no longer as
  parentheticals.
- One correction landed in the process: Livy does **not** contain the "white rock"
  (*leukopetron*); that is Polybius's detail only. The earlier claim of a Livy parallel,
  taken from an ungrounded chat answer, is withdrawn at TC-11.
- Nothing from this batch remains unconfirmed.

---

## Status

- **Populated 2026-08-11; G-2 closed the same day.** 19 attested claim entries
  (TC-01…TC-19, incl. the 09/15/17 Polybius–Livy pairs), plus coverage notes.
- Sources confirmed verbatim by content search (citation offsets were null and unused):
  Polybius (`afc8c222`, Book III 42–56), Livy (`abe8d234`, Book XXI 27–38), Nepos
  (`46d26c93`, 3.4).
- One open gap remains: **G-1**, the modern pass identification, which the ancient texts
  do not settle and which the chapter must present as a debate (conventions §2).
- One correction recorded this session: the "white rock" (*leukopetron*) is Polybius
  only, not Livy (TC-11).
