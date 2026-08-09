#!/usr/bin/env python3
"""Proof-of-concept corridor map: real terrain relief + Pleiades places.

Inputs : data/geo/processed/dem-corridor.npz          (terrain, see SOURCES.md)
         data/geo/processed/pleiades-places-corridor.geojson
         data/geo/processed/awmc-roads-corridor.geojson
         data/geo/processed/awmc-shoreline-corridor.geojson
Output : site/poc/corridor-map.png

Every geographic feature drawn here comes straight from the processed data
files; nothing is drawn freehand. Styling choices (colors, which places get
text labels) are presentational only and are listed below as constants.

Run with the project venv: .venv/bin/python data/geo/scripts/render_poc.py
"""

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource, LinearSegmentedColormap

BBOX = (4.0, 43.5, 8.0, 46.0)  # min lon, min lat, max lon, max lat

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PROC = os.path.join(ROOT, "processed")
OUT = os.path.join(ROOT, "..", "..", "site", "poc", "corridor-map.png")

# Presentational only: which places get a text label on the POC, keyed by
# Pleiades ID (titles are not unique: two places are titled "Brigantio", and
# six candidate passes share "Pass of the Alpes Graiae"). Coordinates always
# come from the data; this list just curbs label clutter.
# Value: (label text, side, dy in degrees).
LABELS = {
    "148004": ("Avennio\n(Avignon)", "right", 0.0),
    "148054": ("Arausio\n(Orange)", "right", 0.0),
    "167719": ("Vienna\n(Vienne)", "right", 0.0),
    "167734": ("Cularo\n(Grenoble)", "left", 0.0),
    "167718": ("Valentia\n(Valence)", "right", 0.0),
    "167716": ("Dea Vocontiorum\n(Die)", "left", 0.0),
    "157925": ("Segustero\n(Sisteron)", "left", 0.0),
    "167750": ("Eburodunum\n(Embrun)", "left", 0.0),
    "167691": ("Brigantio\n(Briançon)", "left", -0.04),
    "167826": ("Matrona\n(Col de Montgenèvre)", "right", 0.04),
    "167639": ("Alpis Graia\n(Little St Bernard)", "left", 0.0),
    "167650": ("Aquae Sextiae\n(Aix)", "right", 0.0),
}
# Not labeled on purpose: the six Pleiades places titled "Pass of the Alpes
# Graiae" (candidate passes west of Segusio) stay unlabeled candidate dots,
# per the conventions doc's rule on contested locations.


def load_geojson(name):
    with open(os.path.join(PROC, name), encoding="utf-8") as f:
        return json.load(f)


def line_parts(geom):
    t = geom["type"]
    if t == "LineString":
        return [geom["coordinates"]]
    if t == "MultiLineString":
        return geom["coordinates"]
    return []


def main():
    d = np.load(os.path.join(PROC, "dem-corridor.npz"))
    elev = d["elev"].astype(np.float64)
    west, north, cell = float(d["west"]), float(d["north"]), float(d["cell_deg"])
    rows, cols = elev.shape
    east = west + cols * cell
    south = north - rows * cell

    sea = elev <= 0
    land = np.where(sea, np.nan, elev)

    mean_lat = (BBOX[1] + BBOX[3]) / 2
    m_per_deg_lat = 110_574.0
    m_per_deg_lon = 111_320.0 * np.cos(np.radians(mean_lat))

    # Hypsometric tint over land, lit by a NW light source.
    terrain_cmap = LinearSegmentedColormap.from_list(
        "corridor",
        [
            (0.00, "#3d5a41"),  # valley floor green
            (0.18, "#6b7f4f"),
            (0.38, "#a8985f"),
            (0.58, "#8f7355"),
            (0.78, "#7d6a63"),
            (0.92, "#d8d3cd"),
            (1.00, "#f5f4f2"),  # high peaks
        ],
    )
    ls = LightSource(azdeg=315, altdeg=45)
    shaded = ls.shade(
        np.where(sea, 0.0, elev),
        cmap=terrain_cmap,
        blend_mode="soft",
        vmin=0,
        vmax=4400,
        dx=cell * m_per_deg_lon,
        dy=cell * m_per_deg_lat,
        vert_exag=1.4,
    )
    shaded[sea] = matplotlib.colors.to_rgba("#b8cdd6")

    fig, ax = plt.subplots(figsize=(16, 11.5), dpi=200)
    ax.imshow(shaded, extent=(west, east, south, north), origin="upper", zorder=1)

    # AWMC ancient shoreline.
    for ft in load_geojson("awmc-shoreline-corridor.geojson")["features"]:
        for part in line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color="#4a6b7a", lw=1.1, zorder=3)

    # AWMC Roman roads.
    for ft in load_geojson("awmc-roads-corridor.geojson")["features"]:
        for part in line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(
                xs, ys, color="#7a2e2e", lw=0.9, alpha=0.85, zorder=4,
                solid_capstyle="round",
            )

    # Pleiades places.
    places = load_geojson("pleiades-places-corridor.geojson")["features"]
    setts, others = [], []
    for ft in places:
        lon, lat = ft["geometry"]["coordinates"][:2]
        if not (BBOX[0] <= lon <= BBOX[2] and BBOX[1] <= lat <= BBOX[3]):
            continue
        types = ft["properties"]["placeTypes"] or []
        (setts if "settlement" in types else others).append((lon, lat))
    if others:
        xs, ys = zip(*others)
        ax.scatter(xs, ys, s=4, c="#5a5145", alpha=0.5, lw=0, zorder=5)
    if setts:
        xs, ys = zip(*setts)
        ax.scatter(
            xs, ys, s=14, c="#1f1a14", edgecolors="#f5f4f2", lw=0.4, zorder=6
        )

    # Labels for the curated subset.
    by_pid = {ft["properties"]["pid"]: ft for ft in places}
    for pid, (label, side, dy) in LABELS.items():
        ft = by_pid.get(pid)
        if ft is None:
            print(f"label skipped, pid not in data: {pid!r}")
            continue
        lon, lat = ft["geometry"]["coordinates"][:2]
        dx = 0.035 if side == "right" else -0.035
        ax.annotate(
            label,
            (lon, lat),
            xytext=(lon + dx, lat + dy),
            ha="left" if side == "right" else "right",
            va="center",
            fontsize=8.5,
            color="#14100c",
            zorder=7,
            path_effects=[
                patheffects.withStroke(linewidth=2.2, foreground="#f5f4f2aa")
            ],
        )

    ax.set_xlim(BBOX[0], BBOX[2])
    ax.set_ylim(BBOX[1], BBOX[3])
    ax.set_aspect(m_per_deg_lat / (111_320.0 * np.cos(np.radians(mean_lat))))
    ax.set_xlabel("longitude (°E)")
    ax.set_ylabel("latitude (°N)")
    ax.set_title(
        "The March — Rhone-to-Alps corridor spike\n"
        "Terrain: SRTM via Terrain Tiles on AWS · Places: Pleiades · "
        "Roads and shoreline: AWMC (Barrington)",
        fontsize=11,
    )
    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, facecolor="white")
    print(f"wrote {os.path.abspath(OUT)} ({os.path.getsize(OUT):,} bytes)")
    print(f"places drawn: {len(setts)} settlements, {len(others)} other")


if __name__ == "__main__":
    main()
