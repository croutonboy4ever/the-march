#!/usr/bin/env python3
"""2.5D options sheet: one pass scene, two dimensionality options, side by side.

Purpose: let Tony choose dimensionality on evidence rather than description.
One scene, one register, two rendered options from the same full-resolution
elevation data:

  option 1  flat shaded relief at full 1-arc-second resolution. This is the
            current pipeline, the same treatment as
            site/poc/close-zoom/traversette-close-zoom.png (left panel).
  option 2  oblique 2.5D perspective of the same window, same data, same
            palette, camera set low to the west looking at the crest.
            Prerendered per scene: the camera is baked at render time, so a
            new angle is a new render, not a viewer action.

  option 3  client-side 3D terrain. Not built here. Written bound only, in
            this file's caption and in the sheet README.

Window and marker match render_close_zoom.py exactly: 6.90-7.25 E,
44.60-44.82 N, with R1 Col de la Traversette (44.7105 N, 7.066361 E,
Wikidata Q1107458 per SOURCES.md section 5) as the one marker. Both panels
read the full-resolution tiles in data/geo/raw/dem/ (SOURCES.md section 3);
neither uses the 4x corridor render grid.

Register: direction B, autumn-crossing state (the attested season of the
march), imported unmodified from render_b_rich_world_states.py.

Visualization-only rule (conventions v1.0 section 4): no elevation figure is
displayed on any panel. No colorbar, no spot heights, no z-axis ticks, no
contour labels. The oblique panel's vertical exaggeration is a styling
multiplier, stated as such, and carries no scale.

Outputs, all under site/poc/2p5d-options/:
  flat-full-res.png     option 1 alone
  oblique-2p5d.png      option 2 alone
  2p5d-options.png      the comparison sheet (both panels plus caption)

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_2p5d_options.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource, LinearSegmentedColormap

import render_close_zoom as rcz
import render_b_rich_world_states as rbw

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT_DIR = os.path.join(ROOT, "..", "..", "site", "poc", "2p5d-options")

WINDOW = rcz.WINDOW           # 6.90, 44.60, 7.25, 44.82
R1 = rcz.R1                   # ("R1", "Col de la Traversette", lon, lat)
STYLE = rbw.STATES["autumn-crossing"]

# Terrain color ramp domain, shared by both panels so the two are directly
# comparable. Styling only; never displayed as a scale (conventions section 4).
RAMP_MIN, RAMP_MAX = 0.0, 4400.0

# Oblique camera. Baked at render time: this is what "prerendered per scene"
# means in practice.
VIEW_ELEV = 28.0              # degrees above the horizontal
VIEW_AZIM = -145.0            # camera to the southwest, looking northeast
VIEW_ZOOM = 2.7               # framing only; fills the panel, clips nothing
VERT_EXAG_3D = 2.5            # styling multiplier on the vertical axis

MEAN_LAT = (WINDOW[1] + WINDOW[3]) / 2
M_PER_DEG_LAT = 110_574.0
M_PER_DEG_LON = 111_320.0 * np.cos(np.radians(MEAN_LAT))

CMAP = LinearSegmentedColormap.from_list("close", STYLE["terrain_stops"])
LS = LightSource(azdeg=STYLE["shade"]["azdeg"], altdeg=STYLE["shade"]["altdeg"])

RC = {
    "font.family": STYLE["font_family"],
    "font.sans-serif": STYLE["font_names"],
    "text.color": STYLE["text"],
    "axes.edgecolor": STYLE["tick"],
    "axes.labelcolor": STYLE["tick"],
    "xtick.color": STYLE["tick"],
    "ytick.color": STYLE["tick"],
}


def shade(elev, cell):
    """Hillshade the window with the register's light, in real-world metres."""
    return LS.shade(
        elev,
        cmap=CMAP,
        blend_mode="soft",
        vmin=RAMP_MIN,
        vmax=RAMP_MAX,
        dx=cell * M_PER_DEG_LON,
        dy=cell * M_PER_DEG_LAT,
        vert_exag=STYLE["shade"]["vert_exag"],
    )


def marker_z(elev, cell):
    """Surface height at R1, used to seat the 3D marker. Never displayed."""
    _, _, lon, lat = R1
    col = int(round((lon - WINDOW[0]) / cell))
    row = int(round((WINDOW[3] - lat) / cell))
    row = min(max(row, 0), elev.shape[0] - 1)
    col = min(max(col, 0), elev.shape[1] - 1)
    return float(elev[row, col])


def render_flat(elev, cell, out_path):
    """Option 1: the current pipeline, one panel, full resolution."""
    with plt.rc_context(RC):
        fig, ax = plt.subplots(figsize=(10.6, 10.0), dpi=150)
        fig.patch.set_facecolor(STYLE["face"])
        fig.subplots_adjust(left=0.085, right=0.985, top=0.925, bottom=0.10)
        ax.imshow(
            shade(elev, cell),
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
        ax.set_aspect(M_PER_DEG_LAT / M_PER_DEG_LON)
        ax.set_title(
            "Option 1 · flat shaded relief, full resolution (current pipeline)",
            fontsize=13, color=STYLE["text"],
        )
        ax.set_xlabel("longitude (°E)")
        ax.set_ylabel("latitude (°N)")
        fig.savefig(out_path, facecolor=STYLE["face"], dpi=150)
        plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def render_oblique(elev, cell, out_path):
    """Option 2: oblique 2.5D surface, same window, same data, baked camera."""
    rows, cols = elev.shape
    lons = WINDOW[0] + np.arange(cols) * cell
    lats = WINDOW[3] - np.arange(rows) * cell
    # Work in kilometres east/north of the window's southwest corner so the
    # box aspect is honest about ground proportions.
    x_km = (lons - WINDOW[0]) * M_PER_DEG_LON / 1000.0
    y_km = (lats - WINDOW[1]) * M_PER_DEG_LAT / 1000.0
    X, Y = np.meshgrid(x_km, y_km)
    Z_km = elev / 1000.0

    rgb = shade(elev, cell)

    with plt.rc_context(RC):
        # The 3D axes box is kept at the aspect the projected scene wants
        # (11.5 x 8.6 in); the figure is taller only to hold title and notes
        # outside it, so the terrain fills its panel instead of floating.
        fig = plt.figure(figsize=(11.5, 9.8), dpi=150)
        fig.patch.set_facecolor(STYLE["face"])
        ax = fig.add_axes((0.0, 0.075, 1.0, 0.878), projection="3d",
                          computed_zorder=False)
        ax.set_facecolor(STYLE["face"])
        ax.plot_surface(
            X, Y, Z_km,
            facecolors=rgb,
            rstride=1, cstride=1,
            linewidth=0, antialiased=False, shade=False,
        )

        key, name, lon, lat = R1
        mx = (lon - WINDOW[0]) * M_PER_DEG_LON / 1000.0
        my = (lat - WINDOW[1]) * M_PER_DEG_LAT / 1000.0
        mz = marker_z(elev, cell) / 1000.0
        ax.scatter([mx], [my], [mz], s=110, marker="D", facecolors="none",
                   edgecolors=STYLE["route"], lw=2.0, zorder=10,
                   depthshade=False)
        ax.text(
            mx, my, mz + 0.30, f"{key} {name}",
            fontsize=11, fontweight="bold", color=STYLE["route"], zorder=11,
            path_effects=[patheffects.withStroke(
                linewidth=3.0, foreground=STYLE["halo"] + "ee")],
        )

        span_x = float(x_km[-1] - x_km[0])
        span_y = float(y_km[0] - y_km[-1])
        span_z = float(Z_km.max() - Z_km.min())
        ax.set_box_aspect((span_x, span_y, span_z * VERT_EXAG_3D),
                          zoom=VIEW_ZOOM)
        ax.view_init(elev=VIEW_ELEV, azim=VIEW_AZIM)
        ax.set_xlim(x_km[0], x_km[-1])
        ax.set_ylim(y_km[-1], y_km[0])
        ax.set_zlim(Z_km.min(), Z_km.max())

        # No axes, and above all no z scale of any kind: conventions section 4.
        # The window is stated in words below instead, so the panel stays
        # locatable without a projected coordinate cage.
        ax.set_axis_off()
        ax.grid(False)

        fig.text(
            0.5, 0.972,
            "Option 2 · oblique 2.5D from the same full-resolution data "
            "(prerendered per scene)",
            ha="center", fontsize=13, color=STYLE["text"],
        )
        fig.text(
            0.5, 0.042,
            f"same window as option 1 ({WINDOW[0]:.2f}–{WINDOW[2]:.2f} °E, "
            f"{WINDOW[1]:.2f}–{WINDOW[3]:.2f} °N), camera to the southwest "
            "looking northeast.",
            ha="center", fontsize=10, color=STYLE["text"],
        )
        fig.text(
            0.5, 0.013,
            f"Camera baked at render time: elevation {VIEW_ELEV:.0f}°, azimuth "
            f"{VIEW_AZIM:.0f}°, vertical exaggeration x{VERT_EXAG_3D:g} "
            "(styling, not a scale). A different angle is a different render.",
            ha="center", fontsize=9.5, color=STYLE["tick"],
        )
        fig.savefig(out_path, facecolor=STYLE["face"], dpi=150)
        plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


CAPTION = (
    "Option 3, client-side 3D terrain, is not built here and nothing is "
    "adopted this session. What it would need: the DEM cut into a tiled "
    "height mesh (or terrain-RGB tiles) served as web assets, a JS terrain "
    "library to draw and stream them, and a site-framework decision first, "
    "because the choice of library largely follows the framework the site "
    "ends up being built in. What it buys: the reader moves the camera, so "
    "one scene answers \"what did this look like from the other side\" "
    "without a new render, and route lines drape on the surface as the view "
    "turns. What it costs: a real build, not a script run. Effort class is "
    "weeks, not the hours the two panels above took, plus a permanent "
    "maintenance surface (asset pipeline, mobile GPU and bandwidth budgets, "
    "and provenance chips that have to keep working on a moving camera). "
    "The two options above are the same pipeline the repo already runs; "
    "option 3 is a new dependency and a new deliverable."
)


def sheet(flat_path, oblique_path, out_path):
    import textwrap

    from PIL import Image

    with plt.rc_context(RC):
        fig = plt.figure(figsize=(24, 12.6), dpi=150)
        fig.patch.set_facecolor(STYLE["face"])
        gs = fig.add_gridspec(
            2, 2, height_ratios=[1, 0.26], width_ratios=[1.0, 1.10],
            left=0.012, right=0.988, top=0.905, bottom=0.015,
            wspace=0.02, hspace=0.04,
        )
        for col, path in enumerate((flat_path, oblique_path)):
            ax = fig.add_subplot(gs[0, col])
            ax.imshow(np.asarray(Image.open(path)))
            ax.set_xticks([])
            ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor(STYLE["tick"])
                s.set_linewidth(0.8)

        cap = fig.add_subplot(gs[1, :])
        cap.axis("off")
        cap.text(
            0.5, 0.95, "Option 3 · client-side 3D terrain (written bound, "
            "nothing built, no framework adopted)",
            ha="center", va="top", fontsize=13, fontweight="bold",
            color=STYLE["text"],
        )
        cap.text(
            0.5, 0.70, textwrap.fill(CAPTION, 168), ha="center", va="top",
            fontsize=11.5, color=STYLE["text"], linespacing=1.35,
            transform=cap.transAxes,
        )
        fig.suptitle(
            "The March: 2.5D options at Col de la Traversette (R1, route "
            "candidate, contested) — one scene, one register, choose "
            "dimensionality\n"
            "Direction B · autumn-crossing state · both panels from the "
            "full-resolution 1-arc-second tiles · terrain: SRTM (modern) via "
            "Terrain Tiles on AWS · R1 placement: Wikidata (SOURCES §5) · "
            "visualization-only, no elevation figures displayed (conventions "
            "§4)",
            fontsize=14, color=STYLE["text"], y=0.985,
        )
        fig.savefig(out_path, facecolor=STYLE["face"], dpi=150)
        plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    elev, cell = rcz.full_res_window()
    print(f"full-res window: {elev.shape[0]} x {elev.shape[1]} samples "
          f"at {cell:.8f} deg")

    flat_path = os.path.join(OUT_DIR, "flat-full-res.png")
    oblique_path = os.path.join(OUT_DIR, "oblique-2p5d.png")
    render_flat(elev, cell, flat_path)
    render_oblique(elev, cell, oblique_path)
    sheet(flat_path, oblique_path, os.path.join(OUT_DIR, "2p5d-options.png"))


if __name__ == "__main__":
    main()
