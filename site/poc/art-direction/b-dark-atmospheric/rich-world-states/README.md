# Direction B rich-world states

Companion to `../lighting-states/`, which isolated the light axis and kept
the desaturated night ramp, so most of its panels stayed dark. This strip
shows the color axis: the same rendering system, structure, and data
carrying natural land color under directional light. Together the two strips
bound what a viewer-facing "final" B looks like across scenes: the register
is one system whose ramp, light, and saturation move per scene, not a
permanently dark map.

- `clear-summer-day.png`: full natural hypsometry (valley green, dry grass,
  rock, snow) under high light. The inhabited, living corridor.
- `golden-evening.png`: the same living ground under low warm west light.
- `autumn-crossing.png`: the attested season of the march. Russet valleys,
  early snow on the heights, cold clear light. Snow here is the ramp's top
  band starting near 2,700 m on the render grid, visualization-only like
  every elevation color (conventions section 4).
- `blue-dusk.png`: blue hour with the warm settlement dots reading as valley
  lights; the bridge back to the night register.

Honesty boundary, stated plainly: the vegetation reading in these states is
elevation-keyed color, a proxy, exactly like the POC's hypsometric tint. No
land-cover or foliage dataset exists in this repo yet; a real foliage layer
would be a new sourced input entering through SOURCES.md, and ancient-period
vegetation would additionally be an inference needing its own basis. Water
is the same AWMC linework as every render; settlements are the same Pleiades
layer. Weather and fog remain separate effect layers, still not shown.

Produced by `data/geo/scripts/render_b_rich_world_states.py`, which imports
the direction renderer unmodified and touches no data.
