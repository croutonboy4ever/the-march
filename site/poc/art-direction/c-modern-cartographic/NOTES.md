# Direction C: modern cartographic

Clean editorial mapping: near-white ground, neutral grey relief kept subtle,
high-contrast linework, sans labels. The data layers are the loudest thing on
the page; terrain is context, not subject.

## 2.5D terrain tilt (feasibility and cost only; not built)

- Feasible with the same mesh pipeline as A and B, but this direction gains
  the least from it. Subtle neutral relief gives weak depth cues on a tilted
  mesh; making tilt legible would need stronger shading or contour lines,
  which is added styling cost and starts to contradict the flat editorial
  register.
- If the 3D/2.5D decision lands on "yes," C is the direction most likely to
  keep the tilt as an occasional set-piece (a pass fly-over) rather than the
  default view.

## Computed viewsheds (feasibility and cost only; not built)

- Same compute as the other directions.
- Cheapest styling of the three: a flat translucent fill with a labeled edge
  is native to this register and needs no custom rendering. Highest analytic
  legibility; lowest atmosphere.
- Provenance note: a viewshed is a computed claim over modern SRTM terrain;
  it displays as inferred with its basis named (conventions sections 3
  and 4).
