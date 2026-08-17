# Direction A: ancient-map register

Replaced the paper-map direction on 2026-08-17 (the old renders are archived
under `archive/2026-08-17/site/poc/art-direction/a-paper-map/`). Stylized
toward an ancient artifact, with the Peutinger table as the loose reference:
parchment ground with a subtle deterministic mottle, ink-wash relief that
darkens with height the way engraved maps ink their high ground, green water,
Peutinger-red roads, antique serif lettering (Hoefler Text, old-style
figures).

One boundary named up front: real ancient maps are schematic, and this is
not. Conventions section 6 requires real coordinates and real topography, so
this direction borrows the material language of an ancient object while the
geometry stays the same shared data as B and C. The style says "old"; the map
never lies about where anything is.

## 2.5D terrain tilt (feasibility and cost only; not built)

- Same mesh pipeline as B and C (`dem-corridor.npz` draped as texture), so
  the base cost is identical. But this register resists tilt hardest of the
  three: an ancient map is a flat object, and perspective terrain breaks the
  conceit outright. The only reading that survives is "the artifact itself
  laid on a table and viewed at an angle," which is a framing device, not a
  terrain treatment.
- The baked ink-wash shading conflicts with dynamic light; light stays
  static or the conceit goes.

## Computed viewsheds (feasibility and cost only; not built)

- Compute is style-independent (boolean mask over the grid, milliseconds per
  observer point).
- Styling cost is the highest of the three directions: a translucent overlay
  is flatly anachronistic on parchment. Hidden ground as hatching or a
  lighter ink wash fits, but that is custom fill work, and the green/sepia
  palette leaves little room for another distinguishable tone.
- Provenance note: a viewshed is a computed claim over modern SRTM terrain;
  it displays as inferred with its basis named (conventions sections 3
  and 4). On this register that marking matters double, because the antique
  costume must not imply the computation is ancient testimony.
