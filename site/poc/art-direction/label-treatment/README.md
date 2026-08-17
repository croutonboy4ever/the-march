# Label treatment

Response to the legibility finding on the state strips: settlement and
landmark names were hard to read against terrain in every direction and
scene state. Diagnosis: labels rendered at 8.5pt with a halo stroke at 67
percent opacity and 2.2px width, too thin and too transparent over busy
mid-tone relief.

Demonstrated fix, applied on the three hardest backgrounds (clear summer
day, autumn crossing, deep night): labels 10pt, keys 9.5pt, halo stroke
fully opaque, widened to 3.2px (keys 3.0px). The halo color already tracks
each style's page ground, so the same treatment carries across every
direction and scene state without per-state tuning. `before-after.png`
shows the summer-day pair side by side.

Implementation: the shared renderer now exposes label parameters
(`LABEL_DEFAULTS` in `render_art_direction.py`); the defaults are unchanged
and were verified to reproduce every committed render byte-for-byte before
these demos were made. The demo values live only in
`render_label_treatment.py`. Folding them into the three direction styles
is a three-line change once the treatment is approved.

Scope note: this is the raster-side bound. In the shipped product, labels
belong to the screen-space reading layer (vector or HTML above the terrain
render): resolution-independent, decluttered by zoom, and the natural home
of the provenance chips. Raster halos are the fallback, not the plan.
