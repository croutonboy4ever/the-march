# Direction B lighting states

Answers the question "is B always that deep darkness?" It is not. The
register is parametric: terrain geometry, hillshade computation, marker
encoding, legend, and every data layer are identical across these four
renders. Each state overrides only the color ramp, the light angle, and the
ink colors that must flip for legibility. Produced by
`data/geo/scripts/render_b_lighting_states.py`, which imports the direction
renderer and touches no data.

- `deep-night.png`: the baseline, exactly the committed direction style.
- `moonlit.png`: floor lifted, silver ramp, higher light. Structure fully
  readable while the register stays nocturnal.
- `dawn-alpenglow.png`: low east light, rose-lit high ground, cool valley
  shadows. The scene-state B would bring to a summit chapter.
- `overcast-day.png`: high flat light, high-key cool greys, dark ink. B's
  daylight limit; note how far it converges toward direction C.

Weather, fog, snowline, and foliage are separate effect layers, not shown
here; this strip isolates light and palette only. In the product, any
depicted scene state is a claim: attested states (snow on the pass, fog at
Trasimene) carry their anchors; anything else is imagined texture and is
labeled as such (conventions sections 1 and 3).
