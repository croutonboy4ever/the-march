#!/usr/bin/env python3
"""Label-treatment demonstration: fixing name legibility on busy terrain.

Diagnosis: place and river labels rendered at 8.5pt with a halo stroke at
67 percent opacity and 2.2px width, which loses names against mid-tone
terrain in every direction and scene state. Fix demonstrated here: label
size up to 10pt (keys 9.5pt), halo stroke fully opaque and widened to 3.2px
(keys 3.0px). The halo color already tracks each style's page ground, so
the treatment carries across every direction and state unchanged.

Rendered on the two hardest backgrounds from the rich-world strip (clear
summer day, autumn of the crossing) plus the committed dark baseline, using
the shared renderer's label parameters. Fold-in approved by Tony 2026-08-17:
the shared LABEL_DEFAULTS in render_art_direction.py now carry the fix, so
LABEL_FIX below matches the defaults, and the before/after sheet renders its
"before" panel explicitly from LABEL_BEFORE (the original values) so the
comparison stays a true record.

This is the raster-side fix. In the shipped product, labels belong to the
screen-space reading layer (vector or HTML over the terrain render), which
is resolution-independent and can declutter by zoom; these renders bound
what the baked-raster form can do.

Output : site/poc/art-direction/label-treatment/<state>-labels.png
         site/poc/art-direction/label-treatment/before-after.png

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_label_treatment.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import render_art_direction as rad
import render_b_rich_world_states as rich

OUT_DIR = os.path.join(rad.OUT_DIR, "label-treatment")

LABEL_FIX = {
    "label_fontsize": 10,
    "key_fontsize": 9.5,
    "label_halo_alpha": "ff",
    "label_halo_lw": 3.2,
    "key_halo_alpha": "ff",
    "key_halo_lw": 3.0,
    "river_halo_lw": 3.0,
}

# The pre-fold-in treatment (the original committed defaults), kept so the
# before/after sheet remains reproducible now that the shared defaults carry
# the fix.
LABEL_BEFORE = {
    "label_fontsize": 8.5,
    "key_fontsize": 8,
    "label_halo_alpha": "aa",
    "label_halo_lw": 2.2,
    "key_halo_alpha": "cc",
    "key_halo_lw": 2.0,
    "river_halo_lw": 2.0,
}

DEMOS = {
    "clear-summer-day": dict(rich.STATES["clear-summer-day"], **LABEL_FIX),
    "autumn-crossing": dict(rich.STATES["autumn-crossing"], **LABEL_FIX),
    "deep-night": dict(rad.STYLES["b-dark-atmospheric"], **LABEL_FIX),
}


def before_after(out_path):
    from PIL import Image

    before = os.path.join(OUT_DIR, "clear-summer-day-labels-before.png")
    after = os.path.join(OUT_DIR, "clear-summer-day-labels.png")
    titles = [
        "Before: 8.5pt labels, halo 67% opacity, 2.2px",
        "After: 10pt labels, halo opaque, 3.2px",
    ]
    fig, axes = plt.subplots(1, 2, figsize=(21.5, 8.6), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    for ax, path, title in zip(axes, [before, after], titles):
        img = Image.open(path)
        ax.imshow(np.asarray(img))
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor("#999999")
        ax.set_title(title, fontsize=13, color="#111111")
    fig.suptitle(
        "Label treatment on the hardest background (clear summer day, "
        "Alps detail)",
        fontsize=15,
        color="#111111",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(out_path, facecolor="#ffffff", dpi=150)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def main():
    data = rad.load_data()
    view_key, view_label, bbox = rad.VIEWS[1]  # alps-detail
    # Explicit "before" panel with the pre-fold-in treatment.
    before_style = dict(rich.STATES["clear-summer-day"], **LABEL_BEFORE)
    before_style["label"] = before_style["label"].replace(
        "Direction B · ", "Direction B · pre-fold-in labels · "
    )
    rad.STYLES["b-labels-before"] = before_style
    rad.render(
        "b-labels-before", view_key, view_label, bbox, data,
        os.path.join(OUT_DIR, "clear-summer-day-labels-before.png"),
    )
    for demo_key, style in DEMOS.items():
        style = dict(style)
        style["label"] = style["label"].replace(
            "Direction B · ", "Direction B · improved labels · "
        )
        rad.STYLES[f"b-labels-{demo_key}"] = style
        rad.render(
            f"b-labels-{demo_key}", view_key, view_label, bbox, data,
            os.path.join(OUT_DIR, f"{demo_key}-labels.png"),
        )
    before_after(os.path.join(OUT_DIR, "before-after.png"))


if __name__ == "__main__":
    main()
