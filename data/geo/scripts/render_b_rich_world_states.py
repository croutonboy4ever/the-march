#!/usr/bin/env python3
"""Direction B rich-world states: the same register carrying a living world.

The lighting-states strip isolated the light axis and kept B's desaturated
night ramp, so most panels stayed dark. This strip shows the color axis: the
same rendering system, same structure, same data, with elevation ramps that
carry natural land color (valley green, dry grass, rock, early snow) under
directional light. Together the two strips bound what a viewer-facing "final"
B would look like across scenes.

Honesty note, repeated in the README: the vegetation reading here is
elevation-keyed color, a proxy for vegetation zones, exactly like the POC's
hypsometric tint. A real foliage or land-cover layer would be a new sourced
dataset entering through SOURCES.md; none is invented here. Water is the
same AWMC linework as every other render; settlement richness is the same
Pleiades layer.

States (styling only; no data changes):
  clear-summer-day  full natural hypsometry under high light
  golden-evening    low warm west light over the same living ground
  autumn-crossing   the attested season of the march: russet valleys, early
                    snow on the heights, cold clear light
  blue-dusk         blue hour; valleys hold deep green, settlements read as
                    warm lights; the bridge back to the night register

Output : site/poc/art-direction/b-dark-atmospheric/rich-world-states/<state>.png
         .../rich-world-states/rich-world-states.png

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_b_rich_world_states.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import render_art_direction as rad

OUT_DIR = os.path.join(
    rad.OUT_DIR, "b-dark-atmospheric", "rich-world-states"
)

BASE = rad.STYLES["b-dark-atmospheric"]

# Shared ink set for the light-ground day states (labels must flip dark).
DAY_INK = {
    "dot": "#1f1d18",
    "dot_small": "#5a564c",
    "ring_uncertain": "#3f3a30",
    "ring_candidate": "#c0331f",
    "route": "#6b46a8",
    "halo": "#f2efe6",
    "text": "#242118",
    "tick": "#5c5648",
    "legend_face": "#f4f1e8",
    "legend_edge": "#8a8474",
    "road": "#8a3d2c",
    "road_alpha": 0.85,
}


def variant(label, **overrides):
    s = dict(BASE)
    s.update(overrides)
    s["label"] = label
    return s


STATES = {
    "clear-summer-day": variant(
        "Direction B · state: clear summer day",
        terrain_stops=[
            (0.00, "#4a7247"),
            (0.12, "#6b8b53"),
            (0.28, "#98a065"),
            (0.45, "#c2b078"),
            (0.60, "#a68a5e"),
            (0.75, "#8d7a66"),
            (0.88, "#b9b3ab"),
            (0.96, "#e8e6e2"),
            (1.00, "#ffffff"),
        ],
        shade={"azdeg": 315, "altdeg": 50, "vert_exag": 1.6},
        face="#f2f0e9",
        sea="#7fa8bd",
        lake="#5f97b8",
        river="#2e6ea3",
        shore="#4a6b7a",
        **DAY_INK,
    ),
    "golden-evening": variant(
        "Direction B · state: golden evening",
        terrain_stops=[
            (0.00, "#42603f"),
            (0.15, "#5e7548"),
            (0.30, "#8a8a55"),
            (0.50, "#b39a62"),
            (0.68, "#a37f57"),
            (0.82, "#95806c"),
            (0.93, "#d9c3a8"),
            (1.00, "#f7e3c8"),
        ],
        shade={"azdeg": 265, "altdeg": 18, "vert_exag": 1.8},
        face="#f0e6d4",
        sea="#8fa9b3",
        lake="#6394b3",
        river="#3a6f9e",
        shore="#54707c",
        **DAY_INK,
    ),
    "autumn-crossing": variant(
        "Direction B · state: autumn of the crossing",
        terrain_stops=[
            (0.00, "#66703f"),
            (0.12, "#8a7f48"),
            (0.25, "#a88a52"),
            (0.40, "#9c7448"),
            (0.55, "#8a7258"),
            (0.62, "#9a9891"),
            (0.75, "#cfd2d3"),
            (0.88, "#eceeee"),
            (1.00, "#ffffff"),
        ],
        shade={"azdeg": 320, "altdeg": 30, "vert_exag": 1.7},
        face="#e9e9e6",
        sea="#7ba2ba",
        lake="#6197b6",
        river="#33689b",
        shore="#4e6b7a",
        **DAY_INK,
    ),
    "blue-dusk": variant(
        "Direction B · state: blue dusk, valley lights",
        terrain_stops=[
            (0.00, "#2e4238"),
            (0.20, "#31474a"),
            (0.40, "#3e5258"),
            (0.60, "#54606a"),
            (0.75, "#6f7880"),
            (0.88, "#a5abb2"),
            (1.00, "#e2e7ea"),
        ],
        shade={"azdeg": 280, "altdeg": 12, "vert_exag": 1.9},
        face="#131820",
        sea="#12202c",
        lake="#1e3c54",
        river="#4c7ba3",
        shore="#3f5a6d",
    ),
}


def strip(out_path):
    from PIL import Image

    fig, axes = plt.subplots(2, 2, figsize=(21.5, 16), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    for ax, (state_key, style) in zip(axes.flat, STATES.items()):
        img = Image.open(os.path.join(OUT_DIR, f"{state_key}.png"))
        ax.imshow(np.asarray(img))
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor("#999999")
        ax.set_title(style["label"], fontsize=13, color="#111111")
    fig.suptitle(
        "Direction B rich-world states: natural land color under the same "
        "light system (vegetation reading is elevation-keyed, a proxy)",
        fontsize=15,
        color="#111111",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(out_path, facecolor="#ffffff", dpi=150)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def main():
    data = rad.load_data()
    view_key, view_label, bbox = rad.VIEWS[1]  # alps-detail
    for state_key, style in STATES.items():
        rad.STYLES[f"b-rich-{state_key}"] = style
        rad.render(
            f"b-rich-{state_key}", view_key, view_label, bbox, data,
            os.path.join(OUT_DIR, f"{state_key}.png"),
        )
    strip(os.path.join(OUT_DIR, "rich-world-states.png"))


if __name__ == "__main__":
    main()
