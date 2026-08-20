# Variations within the ancient-map register

Four plates of the same committed Alps-detail data, differing in what "an ancient map"
is taken to mean. **None of these is a decision.** They exist to be argued with.

Rendered 2026-08-20 by `data/geo/scripts/render_register_variants.py`:

```
.venv/bin/python data/geo/scripts/render_register_variants.py
```

Start with `register-variants.png`, the four side by side at a common height.

## The four

| Plate | Register | Relief is drawn as |
| --- | --- | --- |
| `a-peutinger.png` | Peutinger ink wash. The committed Direction A. | Hillshaded wash darkening with height |
| `d-copperplate.png` | Copperplate engraving, Blaeu and Cassini | Hachures: downslope strokes seeded along isolines |
| `e-ptolemaic.png` | Woodcut cosmography, Ulm Ptolemy 1482 | Posterized cut bands with inked band edges |
| `f-incised.png` | Incised stone, Forma Urbis Romae | Unlabelled cut contours with a lit and a shadowed edge |

Direction A is rendered here through the same code path rather than reused from the
art-direction sheet, so the comparison is fair: identical framing, identical marker
grammar, no legend or colorbar chrome on any of the four.

## How each relief treatment is actually generated

All four read the same committed `dem-corridor.npz`. Nothing is drawn freehand and no
place moves (conventions v1.0 section 6).

**Hachures** are built the way an engraver built them, not scattered on a grid. Isolines
are computed at 125 m, strokes are seeded along them at a fixed spacing, and each stroke
runs straight downslope from the terrain gradient. Two things follow for free, and they
are the reason the technique works: because isolines crowd together on steep ground the
ranks of strokes crowd with them, and stroke length, weight and opacity also scale with
slope. Steep ground goes dark, gentle ground stays near-blank paper. About 89,000 strokes
on this view.

**Cut bands** posterize elevation into five bands, filled and then outlined in ink. The
terrain is smoothed harder than in the other treatments on purpose: a block cut by hand
simplifies, and an unsimplified isoline reads as a machine artefact rather than a cut.

**Cut contours** are drawn twice, once offset up and left in a lighter stone tone and
once in shadow, so the line reads as a groove rather than a drawn line.

## What these treatments do not claim

- Hachures carry direction and steepness. They state no magnitude and display no figure.
- Band edges and cut contours are isolines of the render grid and are **deliberately left
  unlabelled**. An unlabelled contour is a relief treatment, not an elevation readout, so
  the section 4 amendment holds: no elevation figure is displayed on any plate here.
- The broken edge on the incised plate is material costume and nothing else. It is applied
  to the plate's outer boundary only and **never punches a hole through the map**. A gap in
  the stone placed over real ground would assert an absence of evidence that does not
  exist there. Using breakage to signal actual evidence gaps is a different and far more
  careful design, and it is not attempted here.

## Colour

Every register declares a closed palette: a handful of named base colours with a stated
reason, and every other colour a declared mix of two of those bases. `verify_palettes()`
runs on import, recomputes every derived value from its bases and raises on mismatch;
for the Peutinger register it additionally checks the bases still equal the committed
`render_art_direction.STYLES["a-ancient-map"]`. No colour in this build is picked by eye.

One value is deliberately held constant across all four registers: the route violet, so
R1 to R7 stay recognisable when the plates sit side by side.

## A read on each, to argue with

- **Copperplate hachure is the most period-honest of the set.** Hachures are how relief
  was drawn before hillshading existed. Smooth hillshade is a twentieth century technique
  wearing an antique costume; this is not. It is also the busiest, and it leaves the Po
  plain almost empty, which is either honest or bare depending on your taste.
- **Ptolemaic woodcut is the best structural fit.** Ptolemy is a coordinate map, so the
  graduated border belongs to the form rather than being decoration laid on top, and that
  border is a natural home for provenance chips. The banding also flattens the terrain
  into readable shapes, which helps a newcomer more than a continuous wash does.
- **Incised stone is the strongest idea and the biggest risk.** Monochrome removes colour
  as a channel, so the three-marker system would have to be carried by mark shape alone.
  It is also the register most likely to read as a gimmick on a second viewing.
- **Peutinger ink wash** remains the warmest and the most immediately legible, and the
  least specific: it is the one that could belong to any historical subject.

## Considered and not built

- **Portolan chart** and **manuscript codex page** were on the table and not selected this
  round. The portolan carries a real tension worth recording: portolans deliberately leave
  interiors blank, and this project's subject is the interior, so it could only work at
  Mediterranean scale for a title card rather than for the chapter plates.
- **Peutinger proper** (the schematic itinerary strip) and **mappa mundi** are ruled out as
  the map layer, not merely unbuilt. Both distort space by design, and conventions section 6
  requires real coordinates and real topography. They can appear as labelled diagrams
  beside a map; they cannot be the map. Direction A's own notes already concede this, which
  is why the current register borrows an ancient object's material language rather than its
  structure.

## Open with Tony

Same three questions as the rest of the identity set, now with more to compare against:
which register, which display face, and the provenance status of the subtitle. Plus one
new one specific to these: whether the marker system survives a monochrome register, which
is the question the incised plate is really asking.
