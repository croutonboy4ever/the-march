# 2.5D options at Col de la Traversette

One pass scene, one register, three options for how much dimensionality the
experience carries. Two of the three are rendered here so the choice can be
made on evidence rather than description. The third is a written bound only.
**Nothing is decided in this directory and no framework is adopted.** The
call is Tony's.

Scene: the R1 window, 6.90-7.25 E, 44.60-44.82 N, the same window as
`../close-zoom/`. Register: direction B, autumn-crossing state, the attested
season of the march. Both rendered panels read the full-resolution
1-arc-second tiles (SOURCES.md section 3); neither uses the 4x corridor
render grid. R1 is placed from Wikidata (SOURCES.md section 5) and stays a
route candidate, contested, per conventions section 6.

- `2p5d-options.png` — the comparison sheet: both panels plus the option 3
  caption. This is the file to look at.
- `flat-full-res.png` — option 1 alone.
- `oblique-2p5d.png` — option 2 alone.

Produced by `data/geo/scripts/render_2p5d_options.py`, which imports the
close-zoom window reader and the direction-B state table unmodified and
touches no data.

## Option 1 — flat shaded relief, full resolution

The current pipeline, unchanged. A hillshaded raster in map projection, north
up, markers and labels placed in lon/lat.

What it buys: everything already works. Markers sit at coordinates, labels
have a stable place to live, provenance chips (conventions section 8) attach
to a fixed pixel, the reader can measure position by eye against the graticule,
and a scene costs one script run over data already in the repo.

What it costs: the reader reads the pass as a pattern of light and shadow.
Whether a col is a notch you could walk a column through, or a wall, is
something the flat panel encodes but does not show.

## Option 2 — oblique 2.5D, prerendered per scene

The same window, same data, same palette, drawn as a surface seen from a low
camera to the southwest. Every 1-arc-second sample of the window is a vertex;
this is the same elevation array as option 1, projected differently.

**Prerendered per scene** is the load-bearing phrase. The camera (elevation
28 degrees, azimuth -145, vertical exaggeration x2.5) is baked at render
time. A different angle is a different render, produced by the same script
with different numbers. The reader cannot move it.

What it buys: the crossing reads as a crossing. The col shows as a low point
in a wall of ridges with terrain stacked in front of and behind it, which is
the thing the chapter is actually about.

What it costs: north-up map reading goes away, and with it the easy graticule.
Ground coordinates have to be stated in words rather than drawn as an axis
cage (this panel does exactly that). Labels no longer have an obvious home:
the R1 label here floats above its marker and would need real placement rules
at scale. Each new angle, season, or lighting state is another render and
another file. Vertical exaggeration is a styling choice that has to be
declared on every panel, because an exaggerated slope is a claim about
steepness if it is not labeled as styling.

## Option 3 — client-side 3D terrain (written bound, not built)

Nothing was built for this option and no library was installed or chosen.
This is the bound so the comparison is fair.

### What it needs

1. **A site-framework decision first.** The site today is a static page. The
   realistic terrain libraries integrate against whatever the site turns out
   to be (plain static, React/Next, Svelte), and the scroll-driven camera the
   map-journey module needs (conventions section 7) is written against that
   same framework. Picking a terrain library before the framework means
   picking twice.
2. **The DEM cut into web assets.** The corridor DEM exists; a browser cannot
   read a 11 MB `.npz` per scene. Two shapes are plausible: terrain-RGB raster
   tiles (a height-encoded PNG pyramid, standard, streams well, works with
   raster map layers already in the pipeline), or per-scene meshes exported
   for a bounded window (smaller total job if the experience is a handful of
   named scenes rather than a free-roam corridor). Either is a new build step
   in `data/geo/scripts/` with its own SOURCES.md provenance line, since the
   assets are derived products.
3. **A JS terrain library.** Not evaluated here, deliberately. The candidate
   classes are a general 3D engine (most control, most code), a geospatial
   globe/terrain engine (built for exactly this, heavy, opinionated asset
   format), and a 3D-terrain mode bolted onto a web map library (lightest,
   keeps the existing 2D layers, least camera freedom). Which class fits
   follows from item 1 and from how much camera control the reader is meant
   to have.

### What it enables

The reader moves the camera. One scene then answers "what did this look like
from the other side" without a new render, which is the question a contested
route invites and the question option 2 can only answer by adding files.
Route lines, pass markers, and candidate rings drape on the surface and stay
attached as the view turns, so the seven route candidates could be compared
in one continuous view instead of seven prerendered plates. Scroll-to-camera
becomes continuous rather than a cut between stills.

### What it costs

A build, not a script run. **Effort class: weeks, not hours**, and the
maintenance surface is permanent: an asset pipeline to keep in sync with the
DEM, mobile GPU and bandwidth budgets, and a no-WebGL fallback that has to
show the same scene honestly.

Two costs are specific to this project rather than generic:

- **Provenance on a moving camera.** Conventions section 8 puts marker chips
  in the reading layer and anchors behind them. A chip attached to a place in
  a rotating 3D view is a different component from a chip on a static image:
  it has to survive occlusion, depth, and the reader looking at the back of
  the ridge. That is design work, not just engineering.
- **The visualization-only rule gets harder to hold.** Conventions section 4
  says no displayed elevation figure comes off a render grid. An interactive
  camera invites a hover readout, and a hover readout over a terrain mesh is
  exactly the forbidden thing. The rule survives, but it has to be designed
  around rather than simply obeyed.

### What does not change

All three options draw the same DEM. Accuracy is identical across them, and
so is every provenance obligation. This is a presentation decision, not an
evidence decision.
