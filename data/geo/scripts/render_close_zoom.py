#!/usr/bin/env python3
"""Close-zoom terrain prototype: Col de la Traversette (R1) at full resolution.

Purpose: bound what close zoom looks like WITHOUT the 4x downsample. One pass
scene, rendered twice from the same sources at the same window and style:
  left  : the full-resolution 1-arc-second tiles already on disk (~30 m),
          read directly from data/geo/raw/dem/ (SOURCES.md section 3)
  right : the same window from the committed corridor render grid
          (processed/dem-corridor.npz, 4x block-mean, ~120 m)

Window: 6.90-7.25 E, 44.60-44.82 N (upper Guil / upper Po headwaters, spans
the N44E006/N44E007 tile seam). R1, Col de la Traversette (44.7105 N,
7.066361 E, Wikidata Q1107458 per SOURCES.md section 5), is the one marker.

Visualization-only rule (conventions v1.0 section 4): NO elevation figure is
displayed from either grid: no colorbar, no spot heights, no contour labels.
The terrain color ramp is the direction-B autumn-crossing state (the attested
season of the march), styling only. Terrain is modern SRTM.

Output: site/poc/close-zoom/traversette-close-zoom.png

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_close_zoom.py
"""

import gzip
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource, LinearSegmentedColormap

import render_b_rich_world_states as rbw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW_DEM = os.path.join(ROOT, "raw", "dem")
PROC = os.path.join(ROOT, "processed")
OUT = os.path.join(ROOT, "..", "..", "site", "poc", "close-zoom",
                   "traversette-close-zoom.png")

WINDOW = (6.90, 44.60, 7.25, 44.82)  # min lon, min lat, max lon, max lat
R1 = ("R1", "Col de la Traversette", 7.066361, 44.7105)
N = 3601  # samples per 1-degree tile side
STYLE = rbw.STATES["autumn-crossing"]


def read_tile(name):
    with gzip.open(os.path.join(RAW_DEM, name + ".hgt.gz"), "rb") as f:
        data = np.frombuffer(f.read(), dtype=">i2")
    assert data.size == N * N, name
    return data.reshape(N, N).astype(np.float64)

def full_res_window():
    """Mosaic N44E006 + N44E007 (shared edge column dropped), crop to WINDOW."""
    t6, t7 = read_tile("N44E006"), read_tile("N44E007")
    mosaic = np.hstack([t6, t7[:, 1:]])  # lon 6..8, lat 45 (row 0) .. 44
    cells = N - 1  # 3600 per degree
    c0 = round((WINDOW[0] - 6.0) * cells)
    c1 = round((WINDOW[2] - 6.0) * cells) + 1
    r0 = round((45.0 - WINDOW[3]) * cells)
    r1 = round((45.0 - WINDOW[1]) * cells) + 1
    return mosaic[r0:r1, c0:c1], 1.0 / cells


def render_grid_window():
    d = np.load(os.path.join(PROC, "dem-corridor.npz"))
    elev = d["elev"].astype(np.float64)
    west, north, cell = float(d["west"]), float(d["north"]), float(d["cell_deg"])
    c0 = round((WINDOW[0] - west) / cell)
    c1 = round((WINDOW[2] - west) / cell)
    r0 = round((north - WINDOW[3]) / cell)
    r1 = round((north - WINDOW[1]) / cell)
    return elev[r0:r1, c0:c1], cell


def main():
    mean_lat = (WINDOW[1] + WINDOW[3]) / 2
    m_per_deg_lat = 110_574.0
    m_per_deg_lon = 111_320.0 * np.cos(np.radians(mean_lat))
    cmap = LinearSegmentedColormap.from_list("close", STYLE["terrain_stops"])
    ls = LightSource(azdeg=STYLE["shade"]["azdeg"],
                     altdeg=STYLE["shade"]["altdeg"])

    panels = [
        ("full-resolution 1-arc-second tiles (~30 m)", *full_res_window()),
        ("current render grid, 4x block-mean (~120 m)", *render_grid_window()),
    ]

    rc = {
        "font.family": STYLE["font_family"],
        "font.sans-serif": STYLE["font_names"],
        "text.color": STYLE["text"],
        "axes.edgecolor": STYLE["tick"],
        "axes.labelcolor": STYLE["tick"],
        "xtick.color": STYLE["tick"],
        "ytick.color": STYLE["tick"],
    }
    with plt.rc_context(rc):
        fig, axes = plt.subplots(1, 2, figsize=(20, 9.2), dpi=150)
        fig.patch.set_facecolor(STYLE["face"])
        fig.subplots_adjust(left=0.045, right=0.99, top=0.86, bottom=0.13,
                            wspace=0.08)
        for ax, (title, elev, cell) in zip(axes, panels):
            shaded = ls.shade(
                elev,
                cmap=cmap,
                blend_mode="soft",
                vmin=0,
                vmax=4400,
                dx=cell * m_per_deg_lon,
                dy=cell * m_per_deg_lat,
                vert_exag=STYLE["shade"]["vert_exag"],
            )
            ax.imshow(
                shaded,
                extent=(WINDOW[0], WINDOW[2], WINDOW[1], WINDOW[3]),
                origin="upper",
            )
            key, name, lon, lat = R1
            ax.scatter([lon], [lat], s=110, marker="D", facecolors="none",
                       edgecolors=STYLE["route"], lw=2.0, zorder=7)
            ax.annotate(
                f"{key} {name}",
                (lon, lat),
                xytext=(lon + 0.012, lat + 0.010),
                fontsize=11,
                fontweight="bold",
                color=STYLE["route"],
                zorder=8,
                path_effects=[patheffects.withStroke(
                    linewidth=3.0, foreground=STYLE["halo"] + "ee")],
            )
            ax.set_xlim(WINDOW[0], WINDOW[2])
            ax.set_ylim(WINDOW[1], WINDOW[3])
            ax.set_aspect(m_per_deg_lat / m_per_deg_lon)
            ax.set_title(title, fontsize=13, color=STYLE["text"])
            ax.set_xlabel("longitude (°E)")
            ax.set_ylabel("latitude (°N)")
        fig.suptitle(
            "The March: close-zoom terrain bound at Col de la Traversette "
            "(R1, route candidate, contested)\n"
            "Direction B · autumn-crossing state · terrain: SRTM (modern) via "
            "Terrain Tiles on AWS · R1 placement: Wikidata (SOURCES §5)",
            fontsize=13,
            color=STYLE["text"],
        )
        fig.text(
            0.5, 0.03,
            "Visualization-only render (conventions §4): no elevation figures "
            "are displayed from either grid; displayed elevations elsewhere "
            "come from full-res tiles or an authoritative reference.",
            ha="center", fontsize=10, color=STYLE["tick"],
        )
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        fig.savefig(OUT, facecolor=STYLE["face"], dpi=150)
        plt.close(fig)
    print(f"wrote {os.path.relpath(OUT)}")


if __name__ == "__main__":
    main()
