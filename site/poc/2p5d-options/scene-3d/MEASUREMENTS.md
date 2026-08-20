# One scene exported as 3D, measured

Measurement spike answering a specific question: if client-side 3D exists only
at a short list of named scenes rather than across the whole map, what does one
scene actually cost, and how far can a reader zoom into it?

Nothing here is adopted. No library was installed, no framework was chosen, and
no decision is filed. These are numbers to decide on.

Scene: the R1 window (Col de la Traversette), 6.90-7.25 E, 44.60-44.82 N, read
from the full-resolution 1-arc-second tiles (SOURCES.md section 3). Direction B,
autumn-crossing. Same window and register as everything else in
`site/poc/2p5d-options/`.

- `traversette-r1.glb` — the exported scene, one mesh plus one baked texture.
  Structurally validated: 111,565 vertices, 221,760 triangles, all indices in
  range, texture decodes, ground extent 27.7 x 24.3 km as expected.
- `mesh-levels.png` — one view at four mesh densities, same texture on all four.
- `zoom-ladder.png` — one mesh at four view widths, from the whole window down
  to the col.
- `MEASUREMENTS.json` — every level measured, machine-readable.

Produced by `data/geo/scripts/export_scene_3d.py` (export and numbers) and
`data/geo/scripts/render_3d_bound.py` (the two figures).

## What a scene costs

Source window is 793 x 1261 samples, roughly 22 m east-west and 31 m
north-south on the ground, covering 27.7 km across. The baked texture is one
JPEG of 1261 x 793, **0.24 MB**, and it is the same file at every mesh density.
That is the whole trick: geometry gets cheaper, the texture does not.

| Mesh | Triangles | File, texture included | Departs from source, typical | Worst ridge |
|---|---|---|---|---|
| every sample | 1,995,840 | 44.2 MB | 0 m | 0 m |
| one in 2 | 498,960 | 11.2 MB | 3.0 m | 88 m |
| **one in 3** | **221,760** | **5.1 MB** | **4.8 m** | **106 m** |
| one in 4 | 124,740 | 2.2 MB | 6.7 m | 152 m |
| one in 6 | 55,440 | 1.1 MB | 10.8 m | 167 m |
| one in 8 | 31,284 | 0.8 MB | 15.4 m | 161 m |

The bold row is the file committed here.

The worst-ridge column looks alarming and is not. The error concentrates almost
entirely on knife-edge summits: at one-in-3, half of all cells are within 2 m,
nine in ten are within 7 m, and only 0.7 percent exceed 20 m. A decimated mesh
loses sharp summits first and loses very little else.

**Finding: full resolution in 3D means the texture, not the geometry.** At a
normal viewing distance the four densities in `mesh-levels.png` are close to
indistinguishable. One-in-4, at 2.2 MB, reads almost the same as every-sample at
44.2 MB, because the shading the eye reads as detail lives in the texture and
never changed. The 44 MB mesh is not a shipping option and does not need to be.

For scale: the PNGs already committed in this repo run 1.2 to 3.6 MB. A 3D scene
at one-in-3 or one-in-4 is the same order of magnitude as an image the site
already serves.

## How far a reader can zoom

`zoom-ladder.png` is the evidence. Assuming a 1600 px wide viewport:

| View width | Elevation samples per screen pixel | Reads as |
|---|---|---|
| about 28 km (whole window) | one per 5.3 px | comfortable |
| about 14 km | one per 10.5 px | still holding |
| about 7 km | one per 21 px | thinning, faceting visible |
| about 4 km | one per 42 px | past the data, unusable |

So the usable range runs from the whole scene down to roughly half its width,
with a further step available if some softness is acceptable. Call it a genuine
2x zoom, not a 10x one.

**The limit is the source data, not the delivery method.** This is the finding
that matters for the scoped decision. The elevation data is roughly one sample
every 30 m, and at the full-window view that is already only about 5 screen
pixels per sample. Streaming terrain from a tile service would hit the same wall
at the same view width, because it would be serving the same measurements.
Scoping 3D to a short list of baked scenes gives up nothing in zoom depth. It
only gives up roaming between scenes.

**Ground level is far out of reach**, and not by a little. At 30 m sampling the
data can carry the shape of the col, how the ridges stack, and where the gullies
run. It cannot carry a footpath, a boulder field, or anything at the scale of a
person standing there. The ladder's last panel is what asking for that looks
like. A scene that needs a standing-on-the-ground view needs a different method
that is not mapped to the elevation model at all, and under conventions section
1 that would be an illustrated view carrying the imagined marker, not terrain.

## What this does not answer

The asset side is now measured and it is small. The rest of the option 3 bound
in `../README.md` still stands and is untouched by these numbers:

- The viewer component is still real front-end work, and it still comes after
  the site-framework decision.
- Provenance chips on a moving camera are still an open design problem.
- The no-WebGL fallback is still needed, though the oblique render in
  `../oblique-2p5d.png` is a ready answer to it.

## Metric note

The deviation figures above describe how far a decimated mesh departs from the
source surface. They are mesh fidelity metrics in metres. They are not elevation
figures about any place, none of them appears on a rendered panel, and none is
displayed to a reader. Conventions v1.0 section 4 governs displayed elevations
and is unaffected.
