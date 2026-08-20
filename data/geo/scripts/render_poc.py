#!/usr/bin/env python3
"""Proof-of-concept corridor map: real terrain relief + Pleiades places.

Inputs : data/geo/processed/dem-corridor.npz          (terrain, see SOURCES.md)
         data/geo/processed/pleiades-places-corridor.geojson
         data/geo/processed/awmc-roads-corridor.geojson
         data/geo/processed/awmc-shoreline-corridor.geojson
         data/geo/processed/awmc-rivers-corridor.geojson
         data/geo/processed/awmc-inland-water-corridor.geojson
Output : site/poc/corridor-map.png

Every geographic feature drawn here comes straight from the processed data
files; nothing is drawn freehand. Styling choices (colors, which places get
text labels, where river labels sit) are presentational only and are listed
below as constants.

Marker encoding (all of it appears in the on-map legend; rule: every visual
distinction the legend claims must be verifiably visible in the render):
  - solid large dot ..... settlement, location certain in Pleiades
  - solid small dot ..... other place type, location certain (4x area ratio)
  - grey hollow ring .... place whose Pleiades locationCertainty is not
                          'certain' (less-certain / uncertain)
  - red hollow ring ..... the six candidate locations Pleiades titles
                          "Pass of the Alpes Graiae" (west of Segusio),
                          keyed C1-C6 by Pleiades ID; structurally contested
                          per conventions section 6
  - violet hollow diamond the seven passes proposed by scholars as Hannibal's
                          218 BC crossing, keyed R1-R7; a separate ROUTE
                          debate (which pass did the army cross) from the
                          C-ring LOCATION debate (where is this one candidate
                          place). Backers and arguments are in
                          data/content/02/route-candidates.md.

The terrain color scale in the legend is visualization-only (conventions
v1.0 section 4): its numbers describe the color mapping of the render grid,
not the elevation of any place. Displayed place elevations, when they come,
must come from the full-resolution tiles (scripts/audit_elevation.py).

Run with the project venv: .venv/bin/python data/geo/scripts/render_poc.py
"""

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource, LinearSegmentedColormap, Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon as MplPolygon

BBOX = (4.0, 43.5, 8.0, 46.0)  # min lon, min lat, max lon, max lat

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PROC = os.path.join(ROOT, "processed")
OUT = os.path.join(ROOT, "..", "..", "site", "poc", "corridor-map.png")

# Colors (presentational).
C_SEA = "#b8cdd6"
C_LAKE = "#8fb8d0"
C_RIVER = "#3d6fa5"
C_SHORE = "#4a6b7a"
C_ROAD = "#7a2e2e"
C_DOT = "#1f1a14"
C_DOT_SMALL = "#5a5145"
C_RING_UNCERTAIN = "#3a342c"
C_RING_CANDIDATE = "#a02c2c"
C_ROUTE = "#6a3d9a"
C_HALO = "#f5f4f2"

# Marker areas in points^2. Settlement vs other is a claimed size encoding:
# keep the area ratio at 4x so it stays legible (was 3.5x and too subtle).
S_SETTLEMENT = 20
S_OTHER = 5
S_RING = 46
S_RING_CANDIDATE = 60
S_ROUTE = 70

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
    # Aix-les-Bains in Savoie, not Aix-en-Provence. Pleiades 167650 sits at
    # 5.9155E 45.6891N and its own description reads "Aquae Sextiae (modern
    # Aix-les-Bains) was a vicus of the city of Vienna." The earlier gloss
    # "(Aix)" read as Aix-en-Provence, which is Aquae Sextiae Salluviorum,
    # a different town about 240 km south. Corrected 2026-08-20.
    "167650": ("Aquae Sextiae\n(Aix-les-Bains)", "right", 0.0),
}

# The six Pleiades places titled "Pass of the Alpes Graiae" (candidate pass
# locations west of Segusio; Pleiades description: "A pass west of Segusio").
# Rendered as red hollow rings keyed C1-C6 by Pleiades ID; the key appears in
# the site page caption. Pleiades/DARMC name no modern candidate for any of
# them except 963101022, which Pleiades links to Col du Petit Mont-Cenis via
# a GeoHack reference whose longitude is visibly truncated (6.0), which skews
# that place's representative point west into the Arc valley. Nothing is
# moved: rings sit on the Pleiades representative points as given.
PASS_CANDIDATES = [
    "264120821",
    "963101021",
    "963101022",
    "963101023",
    "963101024",
    "963101025",
]
# Presentational: per-candidate label offsets (dx, dy in degrees) so the
# C4/C5/C6 cluster around 6.6-6.7 E does not collide.
CANDIDATE_LABEL_OFFSETS = {
    "264120821": (0.03, 0.025),   # C1
    "963101021": (0.03, 0.025),   # C2
    "963101022": (0.03, 0.025),   # C3
    "963101023": (0.025, -0.05),  # C4: below-right
    "963101024": (0.03, 0.03),    # C5: above-right
    "963101025": (-0.075, 0.0),   # C6: left
}

# Route-debate layer: which of these seven passes Hannibal crossed in 218 BC
# (distinct from the C-ring layer above, which is about locating one
# Pleiades-named candidate place, not about route choice). Four resolve to
# existing Pleiades points (pid given, coordinate pulled from the loaded
# places data below, never re-typed); three have no Pleiades or AWMC record
# and are placed from the fallback lon/lat, sourced in
# data/geo/SOURCES.md section 5 (Wikidata, pulled 2026-08-11). Backers and
# arguments for each are in data/content/02/route-candidates.md.
# Entry shape: (key, name, Pleiades pid or None, fallback (lon, lat) or None).
ROUTE_CANDIDATES = [
    ("R1", "Col de la Traversette", None, (7.066361, 44.710500)),
    ("R2", "Col de Clapier", None, (6.922778, 45.167500)),
    ("R3", "Col du Montgenevre", "167826", None),
    ("R4", "Little St Bernard (Alpis Graia)", "167639", None),
    ("R5", "Great St Bernard (Alpis Poenina)", "167932", None),
    ("R6", "Col de la Larche", None, (6.898611, 44.421667)),
    ("R7", "Mont Cenis / Petit Mont-Cenis", None, (6.9054, 45.2595)),
]
# Presentational: per-candidate label offsets (dx, dy in degrees). R2 sits
# ~0.001 deg from Pleiades C-candidate 264120821 (C1, see SOURCES.md s.5) so
# its key is pushed the opposite way from C1's default offset to stay legible;
# R3/R4 sit on points that already carry a settlement text label (Matrona /
# Alpis Graia in LABELS) so their keys are pushed clear of that label's side.
ROUTE_LABEL_OFFSETS = {
    "R1": (0.03, 0.025),
    "R2": (-0.045, -0.035),   # away from C1's default upper-right offset
    "R3": (0.02, -0.05),      # below; "Matrona" label sits to the right
    "R4": (0.03, 0.0),        # right; "Alpis Graia" label sits to the left
    "R5": (0.03, 0.025),
    "R6": (0.03, 0.025),
    "R7": (-0.03, -0.04),
}

# Presentational: river name label positions (deg) and rotation. The linework
# itself is AWMC data; only the label placement is chosen here.
RIVER_LABELS = [
    ("Rhodanus (Rhône)", 4.72, 44.70, 83),
    ("Druentia (Durance)", 5.42, 43.93, 15),
    ("Isara (Isère)", 5.35, 45.12, 20),
]


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


def polygon_rings(geom):
    """Outer rings of a Polygon/MultiPolygon (holes ignored: at this map
    scale no corridor lake's island is resolvable)."""
    t = geom["type"]
    if t == "Polygon":
        return [geom["coordinates"][0]]
    if t == "MultiPolygon":
        return [poly[0] for poly in geom["coordinates"]]
    return []


def main():
    d = np.load(os.path.join(PROC, "dem-corridor.npz"))
    elev = d["elev"].astype(np.float64)
    west, north, cell = float(d["west"]), float(d["north"]), float(d["cell_deg"])
    rows, cols = elev.shape
    east = west + cols * cell
    south = north - rows * cell

    sea = elev <= 0

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
    shaded[sea] = matplotlib.colors.to_rgba(C_SEA)

    fig, ax = plt.subplots(figsize=(16, 11.5), dpi=200)
    ax.imshow(shaded, extent=(west, east, south, north), origin="upper", zorder=1)

    # AWMC inland water (lake/swamp polygons).
    n_lakes = 0
    for ft in load_geojson("awmc-inland-water-corridor.geojson")["features"]:
        for ring in polygon_rings(ft["geometry"]):
            ax.add_patch(
                MplPolygon(
                    [(p[0], p[1]) for p in ring],
                    closed=True,
                    facecolor=C_LAKE,
                    edgecolor="none",
                    zorder=2,
                )
            )
        n_lakes += 1

    # AWMC rivers (Rhodanus, Druentia, Isara by Pleiades ID, plus the
    # source-annotated Rhodanus-delta segments).
    n_river_feats = 0
    for ft in load_geojson("awmc-rivers-corridor.geojson")["features"]:
        named = ft["properties"]["pid"] is not None
        for part in line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(
                xs,
                ys,
                color=C_RIVER,
                lw=1.6 if named else 1.0,
                alpha=0.9,
                zorder=2.5,
                solid_capstyle="round",
            )
        n_river_feats += 1

    # AWMC ancient shoreline.
    for ft in load_geojson("awmc-shoreline-corridor.geojson")["features"]:
        for part in line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=C_SHORE, lw=1.1, zorder=3)

    # AWMC Roman roads.
    for ft in load_geojson("awmc-roads-corridor.geojson")["features"]:
        for part in line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(
                xs, ys, color=C_ROAD, lw=0.9, alpha=0.85, zorder=4,
                solid_capstyle="round",
            )

    # Pleiades places. Four mutually exclusive marker classes:
    # pass candidates (red rings), non-certain locations (grey rings),
    # certain settlements (large solid), other certain places (small solid).
    places = load_geojson("pleiades-places-corridor.geojson")["features"]
    by_pid = {ft["properties"]["pid"]: ft for ft in places}
    setts, others, uncertain, candidates = [], [], [], []
    for ft in places:
        lon, lat = ft["geometry"]["coordinates"][:2]
        if not (BBOX[0] <= lon <= BBOX[2] and BBOX[1] <= lat <= BBOX[3]):
            continue
        p = ft["properties"]
        if p["pid"] in PASS_CANDIDATES:
            candidates.append((p["pid"], lon, lat))
        elif p.get("locationCertainty") not in ("certain", None):
            uncertain.append((lon, lat))
        elif "settlement" in (p["placeTypes"] or []):
            setts.append((lon, lat))
        else:
            others.append((lon, lat))
    if others:
        xs, ys = zip(*others)
        ax.scatter(xs, ys, s=S_OTHER, c=C_DOT_SMALL, alpha=0.55, lw=0, zorder=5)
    if setts:
        xs, ys = zip(*setts)
        ax.scatter(
            xs, ys, s=S_SETTLEMENT, c=C_DOT, edgecolors=C_HALO, lw=0.4, zorder=6
        )
    if uncertain:
        xs, ys = zip(*uncertain)
        ax.scatter(
            xs,
            ys,
            s=S_RING,
            facecolors="none",
            edgecolors=C_RING_UNCERTAIN,
            lw=1.1,
            zorder=6,
        )
    # Candidate rings, keyed C1-C6 in pid order (key in the page caption).
    for i, (pid, lon, lat) in enumerate(sorted(candidates), start=1):
        ax.scatter(
            [lon],
            [lat],
            s=S_RING_CANDIDATE,
            facecolors="none",
            edgecolors=C_RING_CANDIDATE,
            lw=1.6,
            zorder=7,
        )
        dx, dy = CANDIDATE_LABEL_OFFSETS.get(pid, (0.03, 0.025))
        ax.annotate(
            f"C{i}",
            (lon, lat),
            xytext=(lon + dx, lat + dy),
            ha="left" if dx >= 0 else "right",
            fontsize=8,
            fontweight="bold",
            color=C_RING_CANDIDATE,
            zorder=8,
            path_effects=[patheffects.withStroke(linewidth=2.0, foreground=C_HALO + "cc")],
        )

    # Route candidates: which pass Hannibal crossed (separate ROUTE debate
    # from the C-ring LOCATION debate above). Hollow diamonds, keyed R1-R7.
    # Coordinates: Pleiades pid where one exists, else the fallback recorded
    # in ROUTE_CANDIDATES / SOURCES.md section 5. Nothing drawn freehand.
    route_points = []
    for key, name, pid, fallback in ROUTE_CANDIDATES:
        if pid is not None:
            ft = by_pid.get(pid)
            if ft is None:
                print(f"route candidate {key} skipped, pid not in data: {pid!r}")
                continue
            lon, lat = ft["geometry"]["coordinates"][:2]
        else:
            lon, lat = fallback
        route_points.append((key, name, lon, lat))
    if route_points:
        xs, ys = zip(*[(lon, lat) for _, _, lon, lat in route_points])
        ax.scatter(
            xs,
            ys,
            s=S_ROUTE,
            marker="D",
            facecolors="none",
            edgecolors=C_ROUTE,
            lw=1.6,
            zorder=7,
        )
        for key, name, lon, lat in route_points:
            dx, dy = ROUTE_LABEL_OFFSETS.get(key, (0.03, 0.025))
            ax.annotate(
                key,
                (lon, lat),
                xytext=(lon + dx, lat + dy),
                ha="left" if dx >= 0 else "right",
                fontsize=8,
                fontweight="bold",
                color=C_ROUTE,
                zorder=8,
                path_effects=[patheffects.withStroke(linewidth=2.0, foreground=C_HALO + "cc")],
            )

    # Labels for the curated subset.
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
            zorder=8,
            path_effects=[
                patheffects.withStroke(linewidth=2.2, foreground=C_HALO + "aa")
            ],
        )

    # River name labels (presentational placement; see RIVER_LABELS).
    for text, lon, lat, rot in RIVER_LABELS:
        ax.annotate(
            text,
            (lon, lat),
            fontsize=8.5,
            fontstyle="italic",
            color=C_RIVER,
            rotation=rot,
            rotation_mode="anchor",
            ha="center",
            va="center",
            zorder=8,
            path_effects=[
                patheffects.withStroke(linewidth=2.0, foreground=C_HALO + "aa")
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
        "Roads, shoreline, rivers, inland water: AWMC (Barrington)",
        fontsize=11,
    )

    # Legend: every entry corresponds to a drawn, visible distinction.
    handles = [
        Line2D([], [], marker="o", ls="none", color=C_DOT,
               markeredgecolor=C_HALO, markersize=np.sqrt(S_SETTLEMENT),
               label="settlement (Pleiades, location certain)"),
        Line2D([], [], marker="o", ls="none", color=C_DOT_SMALL,
               markersize=np.sqrt(S_OTHER), alpha=0.8,
               label="other place, representative point (4x smaller area)"),
        Line2D([], [], marker="o", ls="none", markerfacecolor="none",
               markeredgecolor=C_RING_UNCERTAIN, markeredgewidth=1.1,
               markersize=np.sqrt(S_RING),
               label="location not certain in Pleiades (hollow ring)"),
        Line2D([], [], marker="o", ls="none", markerfacecolor="none",
               markeredgecolor=C_RING_CANDIDATE, markeredgewidth=1.6,
               markersize=np.sqrt(S_RING_CANDIDATE),
               label="Graian pass candidate C1–C6 (contested; key in caption)"),
        Line2D([], [], marker="D", ls="none", markerfacecolor="none",
               markeredgecolor=C_ROUTE, markeredgewidth=1.6,
               markersize=np.sqrt(S_ROUTE),
               label="Hannibal route candidate R1–R7 (contested; key on page)"),
        Line2D([], [], color=C_ROAD, lw=1.4,
               label="Roman road (AWMC; network postdates the march)"),
        Line2D([], [], color=C_SHORE, lw=1.4, label="ancient shoreline (AWMC)"),
        Line2D([], [], color=C_RIVER, lw=1.8,
               label="river: Rhodanus, Druentia, Isara + delta arms (AWMC)"),
        Patch(facecolor=C_LAKE, label="inland water (AWMC)"),
        Patch(facecolor=C_SEA, label="sea (render grid elevation ≤ 0)"),
    ]
    # The legend sits below the axes so it covers no map content (the rule:
    # everything the legend claims must be verifiably visible in the render,
    # which an overlapping legend box would defeat -- it hid the Rhone delta
    # in the first draft).
    leg = ax.legend(
        handles=handles,
        loc="upper left",
        bbox_to_anchor=(0.0, -0.055),
        ncol=3,
        fontsize=8,
        framealpha=1.0,
        facecolor=C_HALO,
        edgecolor="#6b6257",
        title="Legend",
        title_fontsize=9,
    )
    leg.set_zorder(10)

    # Terrain color scale: visualization-only (conventions v1.0 s.4).
    sm = plt.cm.ScalarMappable(cmap=terrain_cmap, norm=Normalize(0, 4400))
    cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.01, aspect=30)
    cbar.set_label(
        "terrain color scale (m) — visualization-only render grid;\n"
        "displayed elevations come from full-res tiles (conventions §4)",
        fontsize=8,
    )
    cbar.ax.tick_params(labelsize=7)

    fig.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    # bbox_inches="tight" so the below-axes legend is included in the frame.
    fig.savefig(OUT, facecolor="white", bbox_inches="tight")
    print(f"wrote {os.path.abspath(OUT)} ({os.path.getsize(OUT):,} bytes)")
    print(
        f"places drawn: {len(setts)} settlements, {len(others)} other, "
        f"{len(uncertain)} uncertain rings, {len(candidates)} pass candidates, "
        f"{len(route_points)} route candidates"
    )
    print(f"rivers: {n_river_feats} features; lakes: {n_lakes} polygons")


if __name__ == "__main__":
    main()
