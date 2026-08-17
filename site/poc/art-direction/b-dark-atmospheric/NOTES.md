# Direction B: dark atmospheric

Night-march register: near-black blue ground, terrain-forward relief under a
single restrained low light (altitude 30 degrees, stronger vertical
exaggeration), warm pale markers and labels. Terrain carries the mood; the
data layers sit on top as points of light.

## 2.5D terrain tilt (feasibility and cost only; not built)

- Strongest fit of the three. The style is already lit like a scene, so a
  tilted mesh with one directional light reproduces it almost for free; the
  palette is a shader ramp plus a light direction. Same mesh source
  (`dem-corridor.npz`), same rough cost as A for the mesh itself, but the
  least added styling work of the three directions.
- Risks are performance and floor contrast, not design: dark scenes hide mesh
  seams well but crush detail on low-end screens, so the black floor needs a
  lifted minimum.

## Computed viewsheds (feasibility and cost only; not built)

- Same compute as the other directions (boolean mask over the grid).
- Natural metaphor: visible ground lit, hidden ground falling to dark. This
  reads as light behaving, not as an overlay, so styling cost is low. The
  risk is legibility of the boundary; a thin edge line may be needed.
- The commander's-eye toggle in conventions section 7 is exactly this
  operation, which makes B the direction where viewsheds would earn their
  cost soonest.
- Provenance note: a viewshed is a computed claim over modern SRTM terrain;
  it displays as inferred with its basis named (conventions sections 3
  and 4).
