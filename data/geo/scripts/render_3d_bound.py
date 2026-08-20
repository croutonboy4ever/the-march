#!/usr/bin/env python3
"""Visual evidence for the scoped-3D measurements: mesh levels and zoom range.

Companion to export_scene_3d.py, which produces the numbers. Arithmetic alone
understates a textured mesh, because it counts geometry and ignores the baked
texture that carries most of what the eye reads as detail. These two figures
show the real thing.

Both figures simulate what a web viewer does with a baked scene: the geometry
is decimated to a given mesh density, then put back on the full grid so the
surface carries only the coarse shape, while the shading texture stays at full
source resolution throughout. That is a low-poly mesh under a high-resolution
baked texture, which is exactly the shape of a scoped 3D scene.

  mesh-levels.png  one stressed view (low camera, ridgelines on the skyline)
                   at four mesh densities, full-resolution texture on each
  zoom-ladder.png  the representative mesh density at four view widths, from
                   the whole window down to the col, showing where the source
                   data gives out

Window, register and lighting match render_2p5d_options.py. Conventions v1.0
section 4 holds: no elevation figure appears on any panel.

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_3d_bound.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import numpy as np

import export_scene_3d as ex
import render_2p5d_options as opt

OUT_DIR = os.path.join(opt.OUT_DIR, "scene-3d")
STYLE = opt.STYLE

# Mesh densities shown side by side. The decision-relevant band; strides 6 and
# 8 are reported numerically in MEASUREMENTS.json and are plainly too coarse.
LEVEL_STRIDES = [1, 2, 3, 4]

# Stressed camera for the mesh comparison: low enough that ridgelines sit on
# the skyline, where decimation shows first.
LEVEL_VIEW = {"elev": 14.0, "azim": -145.0, "width_km": 8.0, "zoom": 2.5}

# Zoom ladder, widest to narrowest, centred on R1.
LADDER_WIDTHS_KM = [27.7, 14.0, 7.0, 3.5]
LADDER_VIEW = {"elev": 22.0, "azim": -145.0, "zoom": 2.5}

# Panel geometry for the 2x2 sheets, chosen so each cell is close to the
# proportions the projected scene actually wants; otherwise matplotlib shrinks
# the terrain to fit and leaves the panel half empty.
FIGSIZE = (17, 15)
CELL_W, CELL_H = 0.45, 0.375
CELL_X = (0.03, 0.52)
CELL_Y = (0.50, 0.055)
LADDER_STRIDE = ex.REPRESENTATIVE_STRIDE

VERT_EXAG = opt.VERT_EXAG_3D


def crop(elev, rgb, cell, width_km):
    """Crop grid and texture to a ground window of the given width around R1."""
    _, _, lon, lat = opt.R1
    half_lon = (width_km * 1000.0 / opt.M_PER_DEG_LON) / 2.0
    # Keep the panel's ground proportions the same as the source window.
    aspect = (opt.WINDOW[3] - opt.WINDOW[1]) / (opt.WINDOW[2] - opt.WINDOW[0])
    half_lat = half_lon * aspect

    c0 = int(round((lon - half_lon - opt.WINDOW[0]) / cell))
    c1 = int(round((lon + half_lon - opt.WINDOW[0]) / cell))
    r0 = int(round((opt.WINDOW[3] - (lat + half_lat)) / cell))
    r1 = int(round((opt.WINDOW[3] - (lat - half_lat)) / cell))
    c0, r0 = max(c0, 0), max(r0, 0)
    c1, r1 = min(c1, elev.shape[1]), min(r1, elev.shape[0])

    west = opt.WINDOW[0] + c0 * cell
    north = opt.WINDOW[3] - r0 * cell
    return elev[r0:r1, c0:c1], rgb[r0:r1, c0:c1], west, north


def draw(ax, elev, rgb, cell, west, north, view, marker_label=None):
    """One textured oblique panel. Geometry from elev, colour from rgb."""
    rows, cols = elev.shape
    x_km = np.arange(cols) * cell * opt.M_PER_DEG_LON / 1000.0
    y_km = (rows - 1 - np.arange(rows)) * cell * opt.M_PER_DEG_LAT / 1000.0
    X, Y = np.meshgrid(x_km, y_km)
    Z = elev / 1000.0

    ax.set_facecolor(STYLE["face"])
    ax.plot_surface(X, Y, Z, facecolors=rgb, rstride=1, cstride=1,
                    linewidth=0, antialiased=False, shade=False)

    span_x = float(x_km[-1] - x_km[0])
    span_y = float(y_km[0] - y_km[-1])
    span_z = max(float(Z.max() - Z.min()), 1e-6)
    ax.set_box_aspect((span_x, span_y, span_z * VERT_EXAG), zoom=view["zoom"])
    ax.view_init(elev=view["elev"], azim=view["azim"])
    ax.set_xlim(x_km[0], x_km[-1])
    ax.set_ylim(y_km[-1], y_km[0])
    ax.set_zlim(Z.min(), Z.max())
    ax.set_axis_off()
    ax.grid(False)

    _, name, lon, lat = opt.R1
    mx = (lon - west) * opt.M_PER_DEG_LON / 1000.0
    my = (lat - (north - (rows - 1) * cell)) * opt.M_PER_DEG_LAT / 1000.0
    if 0 <= mx <= span_x and 0 <= my <= span_y:
        col = int(round((lon - west) / cell))
        row = int(round((north - lat) / cell))
        row = min(max(row, 0), rows - 1)
        col = min(max(col, 0), cols - 1)
        mz = float(elev[row, col]) / 1000.0
        ax.scatter([mx], [my], [mz], s=90, marker="D", facecolors="none",
                   edgecolors=STYLE["route"], lw=2.0, zorder=10,
                   depthshade=False)
        if marker_label:
            ax.text(mx, my, mz + span_z * 0.10, marker_label, fontsize=10,
                    fontweight="bold", color=STYLE["route"], zorder=11,
                    path_effects=[patheffects.withStroke(
                        linewidth=3.0, foreground=STYLE["halo"] + "ee")])


def panel(fig, i):
    """Axes rect and title anchor for cell i of the 2x2 sheet."""
    x = CELL_X[i % 2]
    y = CELL_Y[i // 2]
    ax = fig.add_axes((x, y, CELL_W, CELL_H), projection="3d",
                      computed_zorder=False)
    return ax, x + CELL_W / 2, y + CELL_H


def panel_title(fig, cx, top, line1, line2=None):
    fig.text(cx, top + 0.030, line1, ha="center", fontsize=12.5,
             color=STYLE["text"])
    if line2:
        fig.text(cx, top + 0.012, line2, ha="center", fontsize=11,
                 color=STYLE["tick"])


def mesh_levels(elev, rgb, cell, results, out_path):
    """Same stressed view at four mesh densities, one texture throughout."""
    rows, cols = elev.shape
    by_stride = {r["stride"]: r for r in results}

    with plt.rc_context(opt.RC):
        fig = plt.figure(figsize=FIGSIZE, dpi=150)
        fig.patch.set_facecolor(STYLE["face"])
        for i, stride in enumerate(LEVEL_STRIDES):
            ri = ex.sample_indices(rows, stride)
            ci = ex.sample_indices(cols, stride)
            surf = elev if stride == 1 else ex.reconstruct(elev, ri, ci)
            sub_e, sub_rgb, west, north = crop(
                surf, rgb, cell, LEVEL_VIEW["width_km"])
            ax, cx, top = panel(fig, i)
            draw(ax, sub_e, sub_rgb, cell, west, north, LEVEL_VIEW)
            m = by_stride[stride]
            head = ("every source sample" if stride == 1
                    else f"one sample in {stride}")
            panel_title(
                fig, cx, top,
                f"{head}   ·   {m['triangles']:,} triangles   ·   "
                f"{m['glb_bytes']/1e6:.1f} MB",
                f"surface departs from source by {m['rms_deviation_m']:.1f} m "
                f"typical, {m['max_deviation_m']:.0f} m at the worst ridge",
            )
        fig.text(
            0.5, 0.975,
            "How much mesh a scene actually needs: one view, four mesh "
            "densities, the same full-resolution baked texture on all four",
            ha="center", fontsize=15.5, color=STYLE["text"],
        )
        fig.text(
            0.5, 0.955,
            f"Col de la Traversette (R1), {LEVEL_VIEW['width_km']:.0f} km view, "
            "camera low so ridgelines sit on the skyline, where thinning the "
            "mesh shows first",
            ha="center", fontsize=12.5, color=STYLE["text"],
        )
        fig.text(
            0.5, 0.014,
            "Deviation figures describe how far each mesh departs from the "
            "source surface. They are mesh fidelity metrics, not elevations of "
            "any place, and none is displayed to a reader (conventions §4).",
            ha="center", fontsize=10, color=STYLE["tick"],
        )
        fig.savefig(out_path, facecolor=STYLE["face"], dpi=150)
        plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def zoom_ladder(elev, rgb, cell, out_path):
    """One mesh density, four view widths, from whole window down to the col."""
    rows, cols = elev.shape
    ri = ex.sample_indices(rows, LADDER_STRIDE)
    ci = ex.sample_indices(cols, LADDER_STRIDE)
    surf = ex.reconstruct(elev, ri, ci)
    sample_m = cell * opt.M_PER_DEG_LAT * LADDER_STRIDE

    verdicts = ["comfortable", "still holding", "thinning", "past the data"]

    with plt.rc_context(opt.RC):
        fig = plt.figure(figsize=FIGSIZE, dpi=150)
        fig.patch.set_facecolor(STYLE["face"])
        for i, width in enumerate(LADDER_WIDTHS_KM):
            sub_e, sub_rgb, west, north = crop(surf, rgb, cell, width)
            ax, cx, top = panel(fig, i)
            draw(ax, sub_e, sub_rgb, cell, west, north, LADDER_VIEW,
                 marker_label="R1 Col de la Traversette" if i == 0 else None)
            px_per_sample = 1600.0 * sample_m / (width * 1000.0)
            panel_title(
                fig, cx, top,
                f"view about {width:.0f} km wide   ·   {verdicts[i]}",
                f"one elevation sample per {px_per_sample:.1f} screen pixels",
            )
        fig.text(
            0.5, 0.975,
            "How far a reader can zoom before the source data runs out: one "
            f"baked mesh (one sample in {LADDER_STRIDE}), four view widths",
            ha="center", fontsize=15.5, color=STYLE["text"],
        )
        fig.text(
            0.5, 0.955,
            "The limit is set by the elevation data itself, not by the "
            "delivery method. Streaming terrain would reach the same wall in "
            "the same place.",
            ha="center", fontsize=12.5, color=STYLE["text"],
        )
        fig.text(
            0.5, 0.014,
            "Screen-pixel figures assume a 1600 px wide viewport. Past roughly "
            "8 pixels per sample the surface reads as soft and the shading "
            "stops resolving new detail, because there is none left in the "
            "source.",
            ha="center", fontsize=10, color=STYLE["tick"],
        )
        fig.savefig(out_path, facecolor=STYLE["face"], dpi=150)
        plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    elev, cell = opt.rcz.full_res_window()
    rgb = opt.shade(elev, cell)

    rows, cols = elev.shape
    results = []
    for stride in LEVEL_STRIDES:
        ri = ex.sample_indices(rows, stride)
        ci = ex.sample_indices(cols, stride)
        positions, uvs, tris, _, _ = ex.build_mesh(elev, cell, stride)
        err = np.abs(ex.reconstruct(elev, ri, ci) - elev)
        # Size is recomputed here rather than read back, so the figure and the
        # exporter cannot silently disagree about what a level costs.
        import io as _io

        from PIL import Image as _Image
        buf = _io.BytesIO()
        _Image.fromarray((rgb[:, :, :3] * 255).astype(np.uint8)).save(
            buf, format="JPEG", quality=ex.TEXTURE_QUALITY, optimize=True)
        probe = os.path.join(OUT_DIR, f"_size-s{stride}.glb")
        size = ex.write_glb(probe, positions, uvs, tris, buf.getvalue())
        os.remove(probe)
        results.append({
            "stride": stride, "triangles": int(tris.shape[0]),
            "glb_bytes": size, "rms_deviation_m": float(np.sqrt((err ** 2).mean())),
            "max_deviation_m": float(err.max()),
        })

    mesh_levels(elev, rgb, cell, results,
                os.path.join(OUT_DIR, "mesh-levels.png"))
    zoom_ladder(elev, rgb, cell, os.path.join(OUT_DIR, "zoom-ladder.png"))


if __name__ == "__main__":
    main()
