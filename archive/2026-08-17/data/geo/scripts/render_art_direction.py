#!/usr/bin/env python3
"""Art-direction exploration: three styled renders of the SAME corridor data.

Inputs : data/geo/processed/dem-corridor.npz          (terrain, see SOURCES.md)
         data/geo/processed/pleiades-places-corridor.geojson
         data/geo/processed/awmc-roads-corridor.geojson
         data/geo/processed/awmc-shoreline-corridor.geojson
         data/geo/processed/awmc-rivers-corridor.geojson
         data/geo/processed/awmc-inland-water-corridor.geojson
Output : site/poc/art-direction/<direction>/corridor-full.png
         site/poc/art-direction/<direction>/alps-detail.png
         site/poc/art-direction/contact-sheet.png

Directions (styling only; the data pipeline and every marker rule are shared):
  a-paper-map          the POC register refined: parchment ground, warm
                       hypsometric tints, serif labels
  b-dark-atmospheric   night-march register: dark ground, terrain-forward
                       relief under restrained low light, sans labels
  c-modern-cartographic  clean editorial mapping: near-white ground, neutral
                       relief, high-contrast linework, sans labels

Every geographic feature comes straight from the processed data files, exactly
as in render_poc.py; nothing is drawn freehand and no data file is touched.
The marker encoding (solid dots, grey uncertain rings, red C1-C6 candidate
rings, violet R1-R7 route diamonds), the legend entries, the attribution line,
and the visualization-only terrain scale are identical across the three
directions; only colors, typography, and relief treatment differ.

Legend rule carried over from the POC: every visual distinction the legend
claims must be verifiably visible in the render. The Alps detail view contains
no sea and no ancient shoreline, so those legend entries are presence-filtered
per VIEW (computed from the data, applied identically across all three
directions). Nothing is filtered per direction.

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_art_direction.py
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

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PROC = os.path.join(ROOT, "processed")
OUT_DIR = os.path.join(ROOT, "..", "..", "site", "poc", "art-direction")

# Views. Full corridor matches the POC bbox; the Alps detail crop covers all
# six C candidates and all seven R candidates (presentational choice only).
VIEWS = [
    ("corridor-full", "full corridor", (4.0, 43.5, 8.0, 46.0)),
    ("alps-detail", "Alps detail", (6.0, 44.3, 8.0, 45.95)),
]

# Marker areas in points^2, identical across directions (same as POC).
S_SETTLEMENT = 20
S_OTHER = 5
S_RING = 46
S_RING_CANDIDATE = 60
S_ROUTE = 70

# Canvas: fixed size so all six renders are pixel-identical in dimensions.
FIGSIZE = (16, 12)
DPI = 150

# ---------------------------------------------------------------------------
# The three style directions. Styling only: colors, fonts, relief treatment.
# ---------------------------------------------------------------------------
STYLES = {
    "a-paper-map": {
        "label": "Direction A · paper-map register",
        "font_family": "serif",
        "font_names": ["Iowan Old Style", "Palatino", "Georgia", "DejaVu Serif"],
        "face": "#f4efe4",
        "terrain_stops": [
            (0.00, "#667953"),
            (0.18, "#8b935f"),
            (0.38, "#c0aa74"),
            (0.58, "#a98a63"),
            (0.78, "#95806f"),
            (0.92, "#e2dbcd"),
            (1.00, "#f8f5ee"),
        ],
        "shade": {"azdeg": 315, "altdeg": 45, "vert_exag": 1.4},
        "sea": "#c2d2d4",
        "lake": "#9dbfd2",
        "river": "#37648f",
        "shore": "#4a6b7a",
        "road": "#7a2e2e",
        "road_alpha": 0.85,
        "dot": "#241d13",
        "dot_small": "#5a5145",
        "ring_uncertain": "#3a342c",
        "ring_candidate": "#a02c2c",
        "route": "#6a3d9a",
        "halo": "#f5f2e8",
        "text": "#241d13",
        "tick": "#5a5145",
        "legend_face": "#f8f5ec",
        "legend_edge": "#6b6257",
    },
    "b-dark-atmospheric": {
        "label": "Direction B · dark atmospheric",
        "font_family": "sans-serif",
        "font_names": ["Avenir Next", "Avenir", "Gill Sans", "DejaVu Sans"],
        "face": "#0e1319",
        "terrain_stops": [
            (0.00, "#151c23"),
            (0.20, "#1e2830"),
            (0.42, "#2e3a42"),
            (0.62, "#4a545c"),
            (0.80, "#6f787f"),
            (0.93, "#a6adb2"),
            (1.00, "#d9dde0"),
        ],
        "shade": {"azdeg": 315, "altdeg": 30, "vert_exag": 1.9},
        "sea": "#0a0e13",
        "lake": "#1c3550",
        "river": "#48769e",
        "shore": "#3f5a6d",
        "road": "#9c6644",
        "road_alpha": 0.8,
        "dot": "#ecdfc8",
        "dot_small": "#a89e8d",
        "ring_uncertain": "#8f877b",
        "ring_candidate": "#e0524d",
        "route": "#c39bef",
        "halo": "#0e1319",
        "text": "#d9d2c2",
        "tick": "#8a8577",
        "legend_face": "#151b22",
        "legend_edge": "#3a444d",
    },
    "c-modern-cartographic": {
        "label": "Direction C · modern cartographic",
        "font_family": "sans-serif",
        "font_names": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "face": "#fbfbf9",
        "terrain_stops": [
            (0.00, "#eeede7"),
            (0.30, "#dddbd0"),
            (0.55, "#c9c6b8"),
            (0.75, "#b3b0a2"),
            (0.90, "#a09d92"),
            (1.00, "#8f8d85"),
        ],
        "shade": {"azdeg": 315, "altdeg": 45, "vert_exag": 1.2},
        "sea": "#dce8ee",
        "lake": "#b5d3e6",
        "river": "#2f7bb8",
        "shore": "#6a8494",
        "road": "#b03a2e",
        "road_alpha": 0.9,
        "dot": "#111111",
        "dot_small": "#666666",
        "ring_uncertain": "#444444",
        "ring_candidate": "#d62828",
        "route": "#7048b6",
        "halo": "#ffffff",
        "text": "#1a1a1a",
        "tick": "#777777",
        "legend_face": "#ffffff",
        "legend_edge": "#cccccc",
    },
}

# ---------------------------------------------------------------------------
# Data-keyed constants, copied verbatim from render_poc.py (no data changes).
# ---------------------------------------------------------------------------
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

PASS_CANDIDATES = [
    "264120821",
    "963101021",
    "963101022",
    "963101023",
    "963101024",
    "963101025",
]
CANDIDATE_LABEL_OFFSETS = {
    "264120821": (0.03, 0.025),   # C1
    "963101021": (0.03, 0.025),   # C2
    "963101022": (0.03, 0.025),   # C3
    "963101023": (0.025, -0.05),  # C4: below-right
    "963101024": (0.03, 0.03),    # C5: above-right
    "963101025": (-0.075, 0.0),   # C6: left
}

ROUTE_CANDIDATES = [
    ("R1", "Col de la Traversette", None, (7.066361, 44.710500)),
    ("R2", "Col de Clapier", None, (6.922778, 45.167500)),
    ("R3", "Col du Montgenevre", "167826", None),
    ("R4", "Little St Bernard (Alpis Graia)", "167639", None),
    ("R5", "Great St Bernard (Alpis Poenina)", "167932", None),
    ("R6", "Col de la Larche", None, (6.898611, 44.421667)),
    ("R7", "Mont Cenis / Petit Mont-Cenis", None, (6.9054, 45.2595)),
]
ROUTE_LABEL_OFFSETS = {
    "R1": (0.03, 0.025),
    "R2": (-0.045, -0.035),
    "R3": (0.02, -0.05),
    "R4": (0.03, 0.0),
    "R5": (0.03, 0.025),
    "R6": (0.03, 0.025),
    "R7": (-0.03, -0.04),
}

RIVER_LABELS = [
    ("Rhodanus (Rhône)", 4.72, 44.70, 83),
    ("Druentia (Durance)", 5.42, 43.93, 15),
    ("Isara (Isère)", 5.35, 45.12, 20),
]

TITLE_ATTRIBUTION = (
    "Terrain: SRTM via Terrain Tiles on AWS · Places: Pleiades · "
    "Roads, shoreline, rivers, inland water: AWMC (Barrington)"
)
CBAR_LABEL = (
    "terrain color scale (m); visualization-only render grid.\n"
    "Displayed elevations come from full-res tiles (conventions §4)"
)


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
    t = geom["type"]
    if t == "Polygon":
        return [geom["coordinates"][0]]
    if t == "MultiPolygon":
        return [poly[0] for poly in geom["coordinates"]]
    return []


def any_point_in_bbox(parts, bbox):
    for part in parts:
        for p in part:
            if bbox[0] <= p[0] <= bbox[2] and bbox[1] <= p[1] <= bbox[3]:
                return True
    return False


def load_data():
    d = np.load(os.path.join(PROC, "dem-corridor.npz"))
    return {
        "dem": d,
        "lakes": load_geojson("awmc-inland-water-corridor.geojson"),
        "rivers": load_geojson("awmc-rivers-corridor.geojson"),
        "shore": load_geojson("awmc-shoreline-corridor.geojson"),
        "roads": load_geojson("awmc-roads-corridor.geojson"),
        "places": load_geojson("pleiades-places-corridor.geojson"),
    }


def render(style_key, view_key, view_label, bbox, data, out_path):
    style = STYLES[style_key]
    d = data["dem"]
    elev = d["elev"].astype(np.float64)
    west, north, cell = float(d["west"]), float(d["north"]), float(d["cell_deg"])
    rows, cols = elev.shape
    east = west + cols * cell
    south = north - rows * cell
    sea = elev <= 0

    mean_lat = (bbox[1] + bbox[3]) / 2
    m_per_deg_lat = 110_574.0
    m_per_deg_lon = 111_320.0 * np.cos(np.radians(mean_lat))

    # Per-view presence flags for the legend rule (data-driven, identical
    # across directions): sea and shoreline do not appear in the Alps crop.
    c0 = max(0, int((bbox[0] - west) / cell))
    c1 = min(cols, int(np.ceil((bbox[2] - west) / cell)))
    r0 = max(0, int((north - bbox[3]) / cell))
    r1 = min(rows, int(np.ceil((north - bbox[1]) / cell)))
    sea_in_view = bool(sea[r0:r1, c0:c1].any())
    shore_in_view = any(
        any_point_in_bbox(line_parts(ft["geometry"]), bbox)
        for ft in data["shore"]["features"]
    )
    lakes_in_view = any(
        any_point_in_bbox(polygon_rings(ft["geometry"]), bbox)
        for ft in data["lakes"]["features"]
    )

    terrain_cmap = LinearSegmentedColormap.from_list(
        style_key, style["terrain_stops"]
    )
    ls = LightSource(azdeg=style["shade"]["azdeg"], altdeg=style["shade"]["altdeg"])
    shaded = ls.shade(
        np.where(sea, 0.0, elev),
        cmap=terrain_cmap,
        blend_mode="soft",
        vmin=0,
        vmax=4400,
        dx=cell * m_per_deg_lon,
        dy=cell * m_per_deg_lat,
        vert_exag=style["shade"]["vert_exag"],
    )
    shaded[sea] = matplotlib.colors.to_rgba(style["sea"])

    rc = {
        "font.family": style["font_family"],
        "font.serif": style["font_names"],
        "font.sans-serif": style["font_names"],
        "text.color": style["text"],
        "axes.edgecolor": style["tick"],
        "axes.labelcolor": style["tick"],
        "xtick.color": style["tick"],
        "ytick.color": style["tick"],
    }
    with plt.rc_context(rc):
        fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
        fig.patch.set_facecolor(style["face"])
        ax.set_facecolor(style["face"])
        fig.subplots_adjust(left=0.055, right=0.99, top=0.915, bottom=0.16)

        ax.imshow(shaded, extent=(west, east, south, north), origin="upper", zorder=1)

        n_lakes = 0
        for ft in data["lakes"]["features"]:
            for ring in polygon_rings(ft["geometry"]):
                ax.add_patch(
                    MplPolygon(
                        [(p[0], p[1]) for p in ring],
                        closed=True,
                        facecolor=style["lake"],
                        edgecolor="none",
                        zorder=2,
                    )
                )
            n_lakes += 1

        n_river_feats = 0
        for ft in data["rivers"]["features"]:
            named = ft["properties"]["pid"] is not None
            for part in line_parts(ft["geometry"]):
                xs, ys = zip(*[(p[0], p[1]) for p in part])
                ax.plot(
                    xs,
                    ys,
                    color=style["river"],
                    lw=1.6 if named else 1.0,
                    alpha=0.9,
                    zorder=2.5,
                    solid_capstyle="round",
                )
            n_river_feats += 1

        for ft in data["shore"]["features"]:
            for part in line_parts(ft["geometry"]):
                xs, ys = zip(*[(p[0], p[1]) for p in part])
                ax.plot(xs, ys, color=style["shore"], lw=1.1, zorder=3)

        for ft in data["roads"]["features"]:
            for part in line_parts(ft["geometry"]):
                xs, ys = zip(*[(p[0], p[1]) for p in part])
                ax.plot(
                    xs, ys, color=style["road"], lw=0.9,
                    alpha=style["road_alpha"], zorder=4,
                    solid_capstyle="round",
                )

        # Pleiades places, same four mutually exclusive classes as the POC.
        # Classified over the full corridor bbox (not the view bbox) so the
        # class counts match the POC; the view crop just clips the draw.
        full_bbox = VIEWS[0][2]
        places = data["places"]["features"]
        by_pid = {ft["properties"]["pid"]: ft for ft in places}
        setts, others, uncertain, candidates = [], [], [], []
        for ft in places:
            lon, lat = ft["geometry"]["coordinates"][:2]
            if not (full_bbox[0] <= lon <= full_bbox[2]
                    and full_bbox[1] <= lat <= full_bbox[3]):
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
            ax.scatter(xs, ys, s=S_OTHER, c=style["dot_small"], alpha=0.55,
                       lw=0, zorder=5)
        if setts:
            xs, ys = zip(*setts)
            ax.scatter(xs, ys, s=S_SETTLEMENT, c=style["dot"],
                       edgecolors=style["halo"], lw=0.4, zorder=6)
        if uncertain:
            xs, ys = zip(*uncertain)
            ax.scatter(xs, ys, s=S_RING, facecolors="none",
                       edgecolors=style["ring_uncertain"], lw=1.1, zorder=6)
        for i, (pid, lon, lat) in enumerate(sorted(candidates), start=1):
            ax.scatter([lon], [lat], s=S_RING_CANDIDATE, facecolors="none",
                       edgecolors=style["ring_candidate"], lw=1.6, zorder=7)
            dx, dy = CANDIDATE_LABEL_OFFSETS.get(pid, (0.03, 0.025))
            ax.annotate(
                f"C{i}",
                (lon, lat),
                xytext=(lon + dx, lat + dy),
                ha="left" if dx >= 0 else "right",
                fontsize=8,
                fontweight="bold",
                color=style["ring_candidate"],
                zorder=8,
                path_effects=[patheffects.withStroke(
                    linewidth=2.0, foreground=style["halo"] + "cc")],
            )

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
            ax.scatter(xs, ys, s=S_ROUTE, marker="D", facecolors="none",
                       edgecolors=style["route"], lw=1.6, zorder=7)
            for key, name, lon, lat in route_points:
                dx, dy = ROUTE_LABEL_OFFSETS.get(key, (0.03, 0.025))
                ax.annotate(
                    key,
                    (lon, lat),
                    xytext=(lon + dx, lat + dy),
                    ha="left" if dx >= 0 else "right",
                    fontsize=8,
                    fontweight="bold",
                    color=style["route"],
                    zorder=8,
                    path_effects=[patheffects.withStroke(
                        linewidth=2.0, foreground=style["halo"] + "cc")],
                )

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
                color=style["text"],
                zorder=8,
                path_effects=[patheffects.withStroke(
                    linewidth=2.2, foreground=style["halo"] + "aa")],
            )

        for text, lon, lat, rot in RIVER_LABELS:
            ax.annotate(
                text,
                (lon, lat),
                fontsize=8.5,
                fontstyle="italic",
                color=style["river"],
                rotation=rot,
                rotation_mode="anchor",
                ha="center",
                va="center",
                zorder=8,
                path_effects=[patheffects.withStroke(
                    linewidth=2.0, foreground=style["halo"] + "aa")],
            )

        ax.set_xlim(bbox[0], bbox[2])
        ax.set_ylim(bbox[1], bbox[3])
        ax.set_aspect(m_per_deg_lat / m_per_deg_lon)
        ax.set_xlabel("longitude (°E)")
        ax.set_ylabel("latitude (°N)")
        ax.set_title(
            f"The March: Rhone-to-Alps corridor ({view_label})\n"
            + TITLE_ATTRIBUTION,
            fontsize=11,
            color=style["text"],
        )
        fig.text(
            0.01, 0.985, style["label"], ha="left", va="top",
            fontsize=10, fontweight="bold", color=style["text"],
        )

        handles = [
            Line2D([], [], marker="o", ls="none", color=style["dot"],
                   markeredgecolor=style["halo"],
                   markersize=np.sqrt(S_SETTLEMENT),
                   label="settlement (Pleiades, location certain)"),
            Line2D([], [], marker="o", ls="none", color=style["dot_small"],
                   markersize=np.sqrt(S_OTHER), alpha=0.8,
                   label="other place, representative point (4x smaller area)"),
            Line2D([], [], marker="o", ls="none", markerfacecolor="none",
                   markeredgecolor=style["ring_uncertain"],
                   markeredgewidth=1.1, markersize=np.sqrt(S_RING),
                   label="location not certain in Pleiades (hollow ring)"),
            Line2D([], [], marker="o", ls="none", markerfacecolor="none",
                   markeredgecolor=style["ring_candidate"],
                   markeredgewidth=1.6, markersize=np.sqrt(S_RING_CANDIDATE),
                   label="Graian pass candidate C1–C6 (contested; key in caption)"),
            Line2D([], [], marker="D", ls="none", markerfacecolor="none",
                   markeredgecolor=style["route"], markeredgewidth=1.6,
                   markersize=np.sqrt(S_ROUTE),
                   label="Hannibal route candidate R1–R7 (contested; key on page)"),
            Line2D([], [], color=style["road"], lw=1.4,
                   label="Roman road (AWMC)"),
            Line2D([], [], color=style["river"], lw=1.8,
                   label="river: Rhodanus, Druentia, Isara + delta arms (AWMC)"),
        ]
        if shore_in_view:
            handles.insert(6, Line2D([], [], color=style["shore"], lw=1.4,
                                     label="ancient shoreline (AWMC)"))
        if lakes_in_view:
            handles.append(Patch(facecolor=style["lake"],
                                 label="inland water (AWMC)"))
        if sea_in_view:
            handles.append(Patch(facecolor=style["sea"],
                                 label="sea (render grid elevation ≤ 0)"))

        leg = ax.legend(
            handles=handles,
            loc="upper left",
            bbox_to_anchor=(0.0, -0.055),
            ncol=3,
            fontsize=8,
            framealpha=1.0,
            facecolor=style["legend_face"],
            edgecolor=style["legend_edge"],
            title="Legend",
            title_fontsize=9,
            labelcolor=style["text"],
        )
        leg.get_title().set_color(style["text"])
        leg.set_zorder(10)

        sm = plt.cm.ScalarMappable(cmap=terrain_cmap, norm=Normalize(0, 4400))
        cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.01, aspect=30)
        cbar.set_label(CBAR_LABEL, fontsize=8, color=style["tick"])
        cbar.ax.tick_params(labelsize=7, colors=style["tick"])
        cbar.outline.set_edgecolor(style["tick"])

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        fig.savefig(out_path, facecolor=style["face"], dpi=DPI)
        plt.close(fig)

    print(
        f"wrote {os.path.relpath(out_path)} "
        f"[{style_key}/{view_key}] "
        f"places: {len(setts)} settlements, {len(others)} other, "
        f"{len(uncertain)} uncertain, {len(candidates)} C-candidates, "
        f"{len(route_points)} R-candidates; "
        f"rivers {n_river_feats}, lakes {n_lakes}; "
        f"legend: sea={sea_in_view} shore={shore_in_view} lakes={lakes_in_view}"
    )


def contact_sheet(out_path):
    """3 columns (directions) x 2 rows (full, Alps detail), from the PNGs."""
    from PIL import Image

    fig, axes = plt.subplots(2, 3, figsize=(24, 13.5), dpi=150)
    fig.patch.set_facecolor("#ffffff")
    row_labels = ["Full corridor", "Alps detail"]
    for col, (style_key, style) in enumerate(STYLES.items()):
        for row, (view_key, _, _) in enumerate(VIEWS):
            img = Image.open(
                os.path.join(OUT_DIR, style_key, f"{view_key}.png")
            )
            ax = axes[row][col]
            ax.imshow(np.asarray(img))
            ax.set_xticks([])
            ax.set_yticks([])
            for s in ax.spines.values():
                s.set_edgecolor("#999999")
            if row == 0:
                ax.set_title(style["label"], fontsize=13, color="#111111")
            if col == 0:
                ax.set_ylabel(row_labels[row], fontsize=12, color="#111111")
    fig.suptitle(
        "The March: art-direction exploration, same corridor data, "
        "styling only",
        fontsize=15,
        color="#111111",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.97))
    fig.savefig(out_path, facecolor="#ffffff", dpi=150)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def main():
    data = load_data()
    for style_key in STYLES:
        for view_key, view_label, bbox in VIEWS:
            render(
                style_key, view_key, view_label, bbox, data,
                os.path.join(OUT_DIR, style_key, f"{view_key}.png"),
            )
    contact_sheet(os.path.join(OUT_DIR, "contact-sheet.png"))


if __name__ == "__main__":
    main()
