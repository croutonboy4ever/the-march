# Identity options, ancient-map (A) register

Three treatments for Tony to react to. **None of them is a decision.** The brand
question stays Open in the Decision Log until he answers it.

Rendered 2026-08-20 by `data/geo/scripts/render_identity_options.py`, which imports
the committed Direction A style dict from `render_art_direction.py` rather than
copying it. Reproduce with:

```
.venv/bin/python data/geo/scripts/render_identity_options.py
```

## What is here

| File | What it is | View |
| --- | --- | --- |
| `contact-sheet.png` | All three plates at a common height | mixed |
| `1-title-card/title-card.png` | Title card: The March, over the A corridor render | corridor-full, trimmed to 4:3 |
| `1-title-card/title-card-typography.png` | The same card in three type settings | as above |
| `2-frontispiece-the-crossing/frontispiece-the-crossing.png` | Chapter frontispiece for chapter one | committed Alps detail bbox |
| `3-route-debate/route-debate.png` | R1 to R7 drawn as competing corridors, with the backer key | 5.3 to 8.0 E, 44.0 to 45.95 N |
| `4-register-variants/register-variants.png` | Four ideas of what an ancient map is, side by side. See its own [NOTES](4-register-variants/NOTES.md) | committed Alps detail bbox |

## Rules this build held to

**Colour.** Every colour traces to the declared `PALETTE` in the script. Each entry is
either pulled verbatim from `STYLES["a-ancient-map"]` or a stated deterministic mix of
two such pulls, with the mix recorded next to the value. `verify_palette()` runs on
import and raises if any pull has drifted from the A dict, so these plates cannot
silently disagree with the register they claim to be in. Nothing was picked by eye.

**Typography.** The one layer explored, per the brief. Three settings, same colour and
same layout in all three:

| Setting | Display | Text | Reads as |
| --- | --- | --- | --- |
| Inscriptional (used for the three primary plates) | Copperplate | Hoefler Text | Roman lettering cut in stone, book text underneath |
| Register-true | Hoefler Text, letterspaced caps | Hoefler Text | The A register's own lettering, nothing added |
| Engraved plate | Didot | Cochin | An eighteenth century atlas plate, not an ancient object |

Every stack ends in a font matplotlib ships, so the plates still render on a machine
without the macOS faces.

**Geography.** No place moved, no road invented, nothing freehand (conventions v1.0
section 6). Terrain, places, roads, rivers, shoreline and inland water are the same
committed processed files the art-direction renders use.

**Numbers.** No elevation figure appears anywhere on these plates, so the section 4
amendment about visualization-only render grids is not put under strain.

## How the seven routes on option 3 are drawn

This is the part that needed a decision, because the repo holds no route geometry and
none of the seven candidates has an attested line. Each drawn corridor is built from two
visually separated parts:

| Part | Drawn as | What it is |
| --- | --- | --- |
| Trunk and descent | solid line | The AWMC river polyline itself: Druentia or Isara on the west, the named descent river on the east. Committed geometry, drawn unaltered. |
| Branch | dashed line | A least-cost traverse computed over the corridor DEM between the river and the candidate pass. Tobler's hiking function as the cost, so it follows valleys. Computed on the visualization render grid coarsened 3x, roughly 370 m cells. |

**Neither part is an attested itinerary, and the plate says so on its face.** Polybius
names no pass; Livy 21.38 rules out the Poenine Pass and Caelius Antipater's "heights of
Cremo"; Nepos 3.4 says only "the Graian pass" (claims ledger TC-19, gap G-1). The
computed branches carry the inferred marker.

Two things are declared in the script rather than discovered, and both are recorded
there with their reason:

- **The western gate.** All corridors are drawn from the point on their trunk river
  nearest 5.60 E. That is a drawing convention so the seven start from a common line.
  It is not a claim that the army passed there.
- **Where a corridor leaves its trunk.** R2 and R7 are constrained to leave the Isara
  below the confluence of the Arc, because the Maurienne is the corridor every Clapier
  and Mont Cenis reconstruction uses and the Arc itself is not in the committed AWMC
  river set. R6 leaves the Druentia below the Ubaye. R1, R3 and R4 are unconstrained;
  least cost finds the Guil, the Durance head and the Tarentaise on its own.

Uncertainty stays visible three ways: R5 is drawn in a muted ink and tagged refuted in
antiquity, R7 is tagged as having no backer recorded, and R5 is drawn on its eastern
descent only because its western approach, the Valais Rhone, lies outside the committed
corridor DEM. That gap is named on the plate rather than filled in.

## Register variations (added later the same day)

Options 1 to 3 all sit in one reading of "ancient map": the Peutinger-inspired ink wash.
`4-register-variants/` puts three more readings beside it on the same Alps-detail data,
each with its own relief renderer generated from the committed DEM: copperplate hachure,
Ptolemaic woodcut, and incised stone. Full write-up in
[4-register-variants/NOTES.md](4-register-variants/NOTES.md), including which traditions
were ruled out and why.

## Open with Tony

1. **The brand direction itself.** Which treatment, and now also which register, if any,
   is the shape the identity should take. Decision Log row stays Open.
2. **The subtitle's provenance status.** "Hannibal and the war that nearly ended Rome"
   is a framing claim, not a sourced one. Under conventions section 1, untagged prose
   defaults to attested and needs an anchor. Cover and identity copy probably needs
   either its own marker treatment or a stated exemption. It has neither yet.
3. **Typography.** Whether the display face is Copperplate, Hoefler Text, or Didot, and
   whether the display line is letterspaced caps at all.

## Corrected since

- **Aquae Sextiae gloss, fixed 2026-08-20 at Tony's direction.** `render_art_direction.py`
  and `render_poc.py` glossed Pleiades 167650 as "Aquae Sextiae (Aix)". The record sits at
  5.9155 E, 45.6891 N in Savoie and its own Pleiades description reads "modern
  Aix-les-Bains"; the old gloss read as Aix-en-Provence, which is Aquae Sextiae
  Salluviorum, about 240 km south. Both shared dicts now read "(Aix-les-Bains)" and every
  corridor-full render was regenerated. The local `LABEL_GLOSS` override in
  `render_identity_options.py` is now empty; the hook stays for per-plate label needs.
  Only the route-debate plate ever carried this label, and it already showed the
  corrected form; the title card crop stops short of it in latitude.

## Flagged, not fixed here

- The top-level `README.md` still points at `docs/conventions-v0.2.md` as canonical.
  `conventions-v1.0.md` supersedes it.
