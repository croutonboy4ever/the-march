#!/usr/bin/env python3
"""Direction B lighting states: same structure, light and palette adjusted.

Demonstrates that the dark-atmospheric register is a parametric system, not a
fixed darkness: terrain geometry, hillshade computation, marker encoding,
legend, and every data layer are identical across states; each state below
overrides only the color ramp, the light angle, and the ink colors that must
flip for legibility. Rendered over the Alps detail view, where the register
lives.

States (styling only; no data changes):
  deep-night     the baseline exactly as committed in the direction render
  moonlit        lifted floor, cooler silver, higher light
  dawn-alpenglow low light from the east, rose-lit high ground, cool shadows
  overcast-day   high flat light, high-key cool greys, dark ink

Weather, fog, snowline, and foliage are separate effect layers and are NOT
shown here; this strip isolates the light and palette axis only.

Output : site/poc/art-direction/b-dark-atmospheric/lighting-states/<state>.png
         site/poc/art-direction/b-dark-atmospheric/lighting-states/lighting-states.png

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_b_lighting_states.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import render_art_direction as rad

OUT_DIR = os.path.join(
    rad.OUT_DIR, "b-dark-atmospheric", "lighting-states"
)

BASE = rad.STYLES["b-dark-atmospheric"]


def variant(label, **overrides):
    s = dict(BASE)
    s.update(overrides)
    s["label"] = label
    return s


STATES = {
    "deep-night": variant("Direction B · state: deep night (baseline)"),
    "moonlit": variant(
        "Direction B · state: moonlit night",
        terrain_stops=[
            (0.00, "#1b232c"),
            (0.20, "#26303a"),
            (0.42, "#39454f"),
            (0.62, "#57626c"),
            (0.80, "#7e888f"),
            (0.93, "#b7bec3"),
            (1.00, "#e6eaec"),
        ],
        shade={"azdeg": 315, "altdeg": 45, "vert_exag": 1.9},
        face="#10151b",
        sea="#131c26",
        lake="#24405c",
        river="#5786ad",
    ),
    "dawn-alpenglow": variant(
        "Direction B · state: dawn alpenglow",
        terrain_stops=[
            (0.00, "#252b35"),
            (0.25, "#333d49"),
            (0.50, "#4d5560"),
            (0.70, "#6e6a72"),
            (0.85, "#a3828a"),
            (0.95, "#d9a99c"),
            (1.00, "#f2c9b2"),
        ],
        shade={"azdeg": 100, "altdeg": 22, "vert_exag": 1.9},
        face="#141920",
        sea="#1a222d",
        lake="#223a52",
        river="#5b83a8",
    ),
    "overcast-day": variant(
        "Direction B · state: overcast day",
        terrain_stops=[
            (0.00, "#5f6971"),
            (0.30, "#7b838b"),
            (0.55, "#9aa0a6"),
            (0.75, "#b8bcc0"),
            (0.90, "#d5d8da"),
            (1.00, "#eef0f1"),
        ],
        shade={"azdeg": 315, "altdeg": 65, "vert_exag": 1.4},
        face="#dfe3e6",
        sea="#a9bfcc",
        lake="#8fb4cc",
        river="#3c6f9c",
        road="#8a5a40",
        dot="#20242a",
        dot_small="#5c636a",
        ring_uncertain="#4a4f55",
        ring_candidate="#c2403a",
        route="#6b46a8",
        halo="#e6e9eb",
        text="#242a30",
        tick="#4a5258",
        legend_face="#e9eced",
        legend_edge="#9aa4ab",
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
        "Direction B is parametric: same structure and data, "
        "light and palette adjusted per state",
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
        rad.STYLES[f"b-state-{state_key}"] = style
        rad.render(
            f"b-state-{state_key}", view_key, view_label, bbox, data,
            os.path.join(OUT_DIR, f"{state_key}.png"),
        )
    strip(os.path.join(OUT_DIR, "lighting-states.png"))


if __name__ == "__main__":
    main()
