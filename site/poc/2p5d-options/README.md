# 2.5D options at Col de la Traversette

One pass scene, one register, three options for how much dimensionality the
experience carries. Two of the three are rendered here so the choice can be
made on evidence rather than description. The third is written rather than
built, and one of its two variants has since been measured.
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
- `scene-3d/` — the scoped-3D measurement spike added 2026-08-20: one scene
  exported as a real 3D file, with what it costs and how far it zooms.
  `scene-3d/MEASUREMENTS.md` is the write-up.

Produced by `data/geo/scripts/render_2p5d_options.py`, which imports the
close-zoom window reader and the direction-B state table unmodified and
touches no data. The spike adds `export_scene_3d.py` and `render_3d_bound.py`
in the same directory.

Note on the comparison sheet: its caption prices the free-roam variant of
option 3 (3a below), which was all that existed when it was rendered. The
scoped variant (3b) is priced here and in `scene-3d/MEASUREMENTS.md`, not on
the sheet.

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

## Option 3 — client-side 3D terrain (not built, nothing adopted)

Nothing was built for this option and no library was installed or chosen.

Option 3 comes in two variants, and the difference between them is not a
matter of degree. One is a service that streams terrain on demand; the other
is a handful of files sitting in the repo. They are priced separately below.
Variant 3a is a written bound only. Variant 3b was measured on 2026-08-20 and
its numbers are real.

### 3a. Free-roam terrain (bound only, not measured)

The reader can move anywhere across the corridor and the terrain arrives as
they go. This is the version that is permanently maintained, because serving
arbitrary ground at arbitrary zoom is a service rather than an asset.

**What it needs.**

1. **A site-framework decision first.** The site today is a static page. The
   realistic terrain libraries integrate against whatever the site turns out
   to be (plain static, React/Next, Svelte), and the scroll-driven camera the
   map-journey module needs (conventions section 7) is written against that
   same framework. Picking a terrain library before the framework means
   picking twice.
2. **The DEM cut into a streaming tile pyramid.** Terrain-RGB raster tiles, a
   height-encoded PNG pyramid, standard and well supported. A new build step
   in `data/geo/scripts/` with its own SOURCES.md provenance line, since the
   tiles are a derived product. Unlike a baked scene, the pyramid has to be
   kept in sync with the DEM and carries cache and invalidation rules.
3. **A JS terrain library.** Not evaluated here, deliberately. The candidate
   classes are a general 3D engine (most control, most code), a geospatial
   globe/terrain engine (built for exactly this, heavy, opinionated asset
   format), and a 3D-terrain mode bolted onto a web map library (lightest,
   keeps the existing 2D layers, least camera freedom).

**What it enables beyond 3b.** Continuous movement between places: the reader
travels the corridor rather than arriving at scenes. Scroll-to-camera becomes
one unbroken motion rather than a cut between set pieces.

**What it costs.** A build, not a script run. **Effort class: weeks, not
hours**, and the maintenance surface is permanent: a tile pipeline to keep in
sync with the DEM, mobile GPU and bandwidth budgets, and a no-WebGL fallback
that has to show the same ground honestly.

### 3b. Scoped scenes (measured)

3D exists only at a short list of named places. Everywhere else stays flat.

**The scope this is priced against.** Set by Tony in the 2026-08-20 exchange:
a short list that stays short, and only where the reader's question is
genuinely three-dimensional. Can an army get through this gap. What could the
commander see from where he stood. That means the pass scenes, and possibly
the commander's-eye view in the battle steppers (conventions section 7). It
does not mean the corridor overview and it does not mean every waypoint on the
march. **The decision to build any of this remains open**; the scope above is
the shape it would take if built, not a decision that it will be.

The list staying short is load-bearing rather than cosmetic. If it creeps
toward every waypoint, the result is the 3a pyramid rebuilt by accident and
built worse. Two fixed quality levels per scene is still files; five levels
with logic choosing between them is streaming arriving through the back door.

**What it is.** Each scene is one baked file: a fixed mesh with a shaded image
draped over it, exported once and then frozen exactly as the PNGs in this
directory are frozen. No tile service, no streaming, no cache rules, no
pyramid. The site ships files rather than running a service.

**What it needs.**

1. **The site-framework decision, still first, and still the gate.** The
   viewer component is written against whatever the site becomes. This does
   not get cheaper with scoping.
2. **An export step.** Already exists as a spike:
   `data/geo/scripts/export_scene_3d.py` writes a scene to binary glTF from
   the full-resolution tiles. It would need a scene list and a provenance line
   in SOURCES.md to become a real build step, since the models are a derived
   product.
3. **A viewer component, not a terrain engine.** Because the geometry is fixed
   and the camera is bounded, a general 3D viewer is enough and the heavy
   geospatial engines are not needed. Still unpicked, and picking follows item
   1.

**What it costs, measured.** Full numbers and the evidence figures are in
`scene-3d/MEASUREMENTS.md`. In short, for the R1 window (27.7 km across):

| Mesh | Triangles | File, texture included | Departs from source, typical |
|---|---|---|---|
| every sample | 1,995,840 | 44.2 MB | 0 m |
| one in 2 | 498,960 | 11.2 MB | 3.0 m |
| one in 3 | 221,760 | 5.1 MB | 4.8 m |
| one in 4 | 124,740 | 2.2 MB | 6.7 m |

A shipping scene is 2.2 to 5.1 MB, the same order as the PNGs this repo
already serves. The baked texture is 0.24 MB and is the same file at every
mesh density, which is why thinning the geometry is close to free: at normal
viewing distance one sample in 4 reads almost the same as every sample, twenty
times smaller. **Full resolution in 3D means the texture, not the geometry.**
The 44 MB mesh is not a shipping option and does not need to be.

**How far a reader can zoom**, on a 1600 px viewport: comfortable across the
whole 28 km scene, still holding at 14 km, thinning at 7 km, unusable by 4 km.
A genuine 2x zoom, not a 10x one.

**What it enables.** The reader turns the scene and looks at the pass from the
other side, which is the question a contested route invites and the one option
2 can only answer by adding files. Route lines, pass markers, and candidate
rings drape on the surface and stay attached as the view turns, so route
candidates could be compared in one view rather than as separate plates.

**What it does not enable.** Travel between scenes. Arrival at a 3D scene is a
cut, the same way arrival at a rendered panel is a cut today.

**Effort class, split honestly.** The asset side is measured and small: the
exporter exists, a scene is a few MB, and adding a scene is a script run. The
viewer side is real front-end work and **cannot be priced until the framework
decision lands**, because that decision determines what is being written. What
scoping removes is not the build. It is the permanent upkeep, which was the
part that made 3a a standing commitment rather than a project.

**What stays open in 3b, unchanged by the measurements.**

- **Provenance on a moving camera.** Conventions section 8 puts marker chips
  in the reading layer with anchors behind them. A chip attached to a place in
  a turning view is a different component from a chip on a static image: it
  has to survive occlusion, depth, and the reader looking at the back of the
  ridge. Scoping narrows the problem, because a bounded camera has far fewer
  positions to design for than a free one, but it does not remove it. Design
  work, not just engineering.
- **The visualization-only rule gets harder to hold.** Conventions section 4
  says no displayed elevation figure comes off a render grid. An interactive
  camera invites a hover readout, and a hover readout over a terrain mesh is
  exactly the forbidden thing. The rule survives, but it has to be designed
  around rather than simply obeyed.
- **A no-WebGL fallback**, which now has an easy answer: the option 2 oblique
  render is the same scene from a fixed camera, and it already exists.

### What the measurements settled for both variants

The zoom limit belongs to the elevation data, not to the delivery method. The
source is roughly one measurement every 30 m, and at the full-scene view that
is already only about 5 screen pixels per measurement. A streaming pyramid
would hit the same wall at the same view width, because it would be serving
the same measurements.

**So 3a buys no additional detail at any given scene.** What it buys is
roaming between scenes. That is the entire difference in reader experience,
and it is the thing to weigh against a permanent maintenance surface.

### Where scoped 3D stops: ground level

At 30 m sampling the data carries the shape of the col, how the ridges stack,
and where the gullies run. It cannot carry a footpath, a boulder field, or
anything at the scale of a person standing there. The last panel of
`scene-3d/zoom-ladder.png` is what asking for it looks like.

A scene that needs a standing-on-the-ground view therefore needs a method that
is not mapped to the elevation model at all. Under conventions section 1 that
would be an illustrated view carrying the imagined marker, not terrain, and it
would carry no numbers, no named events, and no archaeology. Raised by Tony in
the same exchange and recorded here as the boundary; not designed, and out of
scope for this directory.

## What does not change

All three options draw the same DEM. Accuracy is identical across them, and
so is every provenance obligation. This is a presentation decision, not an
evidence decision.
