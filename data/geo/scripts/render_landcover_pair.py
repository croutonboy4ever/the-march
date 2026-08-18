#!/usr/bin/env python3
"""Demonstration pair: land-cover-driven color vs elevation-keyed color.

Left panel : base color per ESA WorldCover class (modern-basis texture,
             processed/landcover-corridor.npz); the DEM contributes
             HILLSHADE ONLY. This is the decoupling the land-cover layer
             exists to prove: color no longer encodes elevation.
Right panel: the current elevation-keyed equivalent (the clear-summer-day
             state from render_b_rich_world_states.py, unchanged), where
             the same greens and browns are a ramp over elevation, a proxy.

Both panels are the direction-B system over identical corridor data; every
marker rule, label, and legend behavior is shared via render_art_direction.

Modern-basis caption rule (SOURCES.md section 6): WorldCover is a 2021
dataset. The land-cover panel is captioned as modern-basis texture in its
label, its attribution line, and its legend; ancient vegetation is a
separate inference and out of scope here.

Class handling (render-time; the data file keeps all classes). Decided by
Tony 2026-08-17 (Decision Log, Locked):
  natural classes render as texture basis: tree, shrub, grass, bare/sparse
  (moss/lichen grouped with bare, ratified), snow/ice, permanent water.
  built-up (50) is MASKED: drawn as the neutral ground tone, no texture claim.
  cropland (40) renders in the open-land tone (same family as grassland);
  the honesty lives in the legend label "cropland (modern, rendered as
  open land)" and the modern-basis caption.
  herbaceous wetland (90) renders in its own marsh tone, distinct from
  open water; most delta wetland cells sit at or below 0 m and stay under
  the sea mask until shoreline-accurate rendering lands (SOURCES gap 2).

Output : site/poc/landcover-pair/landcover-driven.png
         site/poc/landcover-pair/elevation-keyed.png
         site/poc/landcover-pair/landcover-pair.png   (side-by-side sheet)

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_landcover_pair.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib.pyplot as plt
import numpy as np

import render_art_direction as rad
import render_b_rich_world_states as rbw

OUT_DIR = os.path.join(rad.OUT_DIR, "..", "landcover-pair")

# WorldCover class -> render color. Natural classes in the clear-summer-day
# family; masked/pending classes in neutrals that claim nothing.
NEUTRAL = "#d8d3c4"           # built-up (masked) and nodata
CLASS_COLORS = {
    0: NEUTRAL,               # nodata (open sea is drawn by the sea mask)
    10: "#4a7247",            # tree cover
    20: "#8a9a58",            # shrubland
    30: "#a8b070",            # grassland
    40: "#a8b070",            # cropland: open-land tone (decided 2026-08-17)
    50: NEUTRAL,              # built-up — masked
    60: "#b0a184",            # bare / sparse vegetation
    70: "#f0f3f5",            # snow and ice
    80: "#5f97b8",            # permanent water
    90: "#7fa98e",            # herbaceous wetland: marsh tone (decided 2026-08-17)
    100: "#b0a184",           # moss/lichen, grouped with bare (ratified)
}

LEGEND_PATCHES = [
    ("tree cover (WorldCover 2021, modern basis)", CLASS_COLORS[10]),
    ("shrubland", CLASS_COLORS[20]),
    ("grassland", CLASS_COLORS[30]),
    ("bare / sparse (incl. moss & lichen)", CLASS_COLORS[60]),
    ("snow / ice", CLASS_COLORS[70]),
    ("permanent water (land cover)", CLASS_COLORS[80]),
    ("cropland (modern, rendered as open land)", CLASS_COLORS[40]),
    ("herbaceous wetland (marsh)", CLASS_COLORS[90]),
    ("built-up (masked) / no data", NEUTRAL),
]

WC_ATTRIBUTION = (
    "Land-cover base color: © ESA WorldCover project 2021 (CC-BY 4.0), "
    "MODERN-basis texture · terrain hillshade only: SRTM via Terrain Tiles · "
    "Places: Pleiades · Roads, shoreline, rivers: AWMC (Barrington)"
)


def build_base_rgb():
    lc = np.load(os.path.join(rad.PROC, "landcover-corridor.npz"))
    dem = np.load(os.path.join(rad.PROC, "dem-corridor.npz"))
    assert lc["cls"].shape == dem["elev"].shape
    assert float(lc["west"]) == float(dem["west"])
    assert float(lc["north"]) == float(dem["north"])
    assert float(lc["cell_deg"]) == float(dem["cell_deg"])
    cls = lc["cls"]
    lut = np.zeros((256, 3))
    for code, color in CLASS_COLORS.items():
        lut[code] = plt.matplotlib.colors.to_rgb(color)
    return lut[cls]


def main():
    data = rad.load_data()
    view_key, view_label, bbox = rad.VIEWS[0]  # corridor-full

    lc_style = dict(rbw.STATES["clear-summer-day"])
    lc_style["label"] = (
        "Direction B · land-cover-driven color: ESA WorldCover 2021 "
        "(modern-basis texture), DEM as hillshade only"
    )
    lc_style["base_rgb"] = build_base_rgb()
    lc_style["extra_legend_patches"] = LEGEND_PATCHES
    lc_style["attribution"] = WC_ATTRIBUTION
    lc_style["legend_ncol"] = 4
    lc_style["bottom_margin"] = 0.185

    ek_style = dict(rbw.STATES["clear-summer-day"])
    ek_style["label"] = (
        "Direction B · elevation-keyed color (current): one ramp over "
        "elevation, a proxy for vegetation"
    )

    panels = [
        ("landcover-driven", lc_style),
        ("elevation-keyed", ek_style),
    ]
    for key, style in panels:
        rad.STYLES[f"pair-{key}"] = style
        rad.render(
            f"pair-{key}", view_key, view_label, bbox, data,
            os.path.join(OUT_DIR, f"{key}.png"),
        )

    from PIL import Image

    fig, axes = plt.subplots(2, 1, figsize=(16, 24), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    for ax, (key, style) in zip(axes.flat, panels):
        img = Image.open(os.path.join(OUT_DIR, f"{key}.png"))
        ax.imshow(np.asarray(img))
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor("#999999")
        ax.set_title(style["label"], fontsize=13, color="#111111")
    fig.suptitle(
        "The March: base color from land cover vs from elevation — same "
        "data, same system, color decoupled from height",
        fontsize=15,
        color="#111111",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    out = os.path.join(OUT_DIR, "landcover-pair.png")
    fig.savefig(out, facecolor="#ffffff", dpi=150)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out)}")


if __name__ == "__main__":
    main()
