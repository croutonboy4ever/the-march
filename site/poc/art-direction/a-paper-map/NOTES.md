# Direction A: paper-map register

The current POC direction refined: parchment ground, warm hypsometric tints,
serif labels, ink-toned linework. The map reads as a made object, a plate in a
book about the march.

## 2.5D terrain tilt (feasibility and cost only; not built)

- Feasible: drape this exact colormap as a texture over a mesh built from
  `dem-corridor.npz` (three.js or MapLibre terrain). Moderate cost, roughly a
  week of POC work, no new data.
- The register fights the treatment. Paper is a flat artifact; tilting it
  breaks the conceit unless the tilt is presented as a curled or raised sheet,
  which is its own design project. Low tilt angles (10 to 20 degrees) survive;
  a free camera does not.
- The baked hillshade in the texture conflicts with any dynamic light source.
  Either keep light static (cheap) or re-derive shading in a shader from the
  raw grid and keep only the tint ramp from this style (more work).

## Computed viewsheds (feasibility and cost only; not built)

- Compute cost is style-independent: line-of-sight over the 120 m render grid
  is milliseconds per observer point in numpy, and the result is a boolean
  mask.
- Styling cost is where this direction pays: a flat translucent overlay looks
  anachronistic on parchment. An engraved treatment (hatching or stipple for
  hidden ground) fits the register but costs custom fill rendering.
- Provenance note either way: a viewshed is a computed claim over modern SRTM
  terrain. Under conventions sections 3 and 4 it displays as inferred, never
  attested, and its terrain basis is named.
