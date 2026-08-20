#!/usr/bin/env python3
"""Variations within the ancient-map register, for evaluation beside the current A.

Four plates of the SAME committed Alps-detail data, differing in what an
"ancient map" is taken to mean. The current Peutinger-inspired direction is
rendered here too, through this same code path rather than reused from the
art-direction sheet, so the comparison is fair: identical framing, identical
marker grammar, no legend or colorbar chrome on any of them.

  a-peutinger   ink wash on parchment. The committed Direction A treatment:
                hillshaded relief darkening with height, green water, red
                roads, antique serif. What already exists.
  d-copperplate hachured engraving. Relief is drawn as a field of downslope
                strokes generated from the terrain gradient, the way relief
                was actually drawn before hillshading existed. Steeper ground
                gets longer, heavier, denser strokes (the Lehmann rule);
                ground below the slope threshold stays blank paper.
  e-ptolemaic   woodcut cosmography. Relief is posterized into cut bands with
                inked band edges, under a graduated graticule border. Ptolemy
                is a coordinate map, so the graticule is native to the form
                rather than decoration laid on top.
  f-incised     incised stone. Monochrome marble, relief as unlabelled cut
                contours with a lit and a shadowed edge, one ochre accent
                standing in for the pigment traces on the Forma Urbis.

Nothing here is a decision. These are options to react to.

Colour rule
-----------
Every register declares a closed palette: a handful of named base colours with
a stated reason, and every other colour a declared mix of two of those bases.
`verify_palettes()` runs on import, recomputes every derived value from its
bases, and raises on mismatch; for the Peutinger register it additionally
checks the bases still equal the committed
`render_art_direction.STYLES["a-ancient-map"]`. No colour in this file is
picked by eye.

What these treatments do and do not claim (conventions v1.0 sections 4 and 6)
-----------------------------------------------------------------------------
Every relief treatment is generated from the same committed corridor DEM. No
place moves, no road is invented, nothing is drawn freehand.

- Hachures are a rendering of the terrain gradient. They carry direction and
  steepness, not magnitude, and no figure is displayed.
- Woodcut bands are a posterization of real elevation. The band edges are
  isolines of the render grid and are deliberately left unlabelled.
- Incised contours are likewise unlabelled. An unlabelled contour is a relief
  treatment, not an elevation readout, so the section 4 amendment holds: no
  elevation figure is displayed on any plate here.
- The broken edge on the incised plate is material costume and nothing more.
  It is applied to the plate's outer boundary only and never punches a hole
  through the map, because a gap in the stone placed over real ground would
  assert an absence of evidence that does not exist there. Using breakage to
  signal actual evidence gaps is a different and far more careful design, and
  it is not attempted here.

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_register_variants.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import LightSource, LinearSegmentedColormap
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch, Polygon as MplPolygon, Rectangle
from matplotlib.path import Path

import render_art_direction as rad
import render_identity_options as rio

A = rad.STYLES["a-ancient-map"]
OUT_DIR = os.path.join(rio.OUT_DIR, "4-register-variants")
BBOX = rad.VIEWS[1][2]          # the committed Alps detail view
DPI = 150
FIGW, FIGH = 11.0, 14.2

M_PER_DEG_LAT = 110_574.0


def m_per_deg_lon(lat):
    return 111_320.0 * np.cos(np.radians(lat))


# ---------------------------------------------------------------------------
# Registers. Each declares closed bases plus derived mixes of those bases.
# ---------------------------------------------------------------------------
REGISTERS = {
    "a-peutinger": {
        "label": "A · Peutinger ink wash",
        "relief_note": "Hillshaded wash darkening with height, the committed "
                       "Direction A treatment.",
        "note": "What exists now. Parchment ground with a deterministic "
                "mottle, ink-wash relief, green water, Peutinger-red roads, "
                "antique serif lettering.",
        "relief": "wash",
        "border": "double_rule",
        "caps_labels": False,
        "display": ["Hoefler Text", "Iowan Old Style", "Palatino", "DejaVu Serif"],
        "text": ["Hoefler Text", "Iowan Old Style", "Palatino", "DejaVu Serif"],
        "track": 0.30,
        # Bases pulled verbatim from the committed A style dict. Checked on
        # import, so this register cannot drift away from what it claims.
        "bases": {
            "ground": ("A:face", A["face"]),
            "ink": ("A:text", A["text"]),
            "water": ("A:river", A["river"]),
            "road": ("A:road", A["road"]),
            "route": ("A:route", A["route"]),
            "accent": ("A:ring_candidate", A["ring_candidate"]),
        },
        "derived": {
            "halo": ("ground", "ground", 0.0),
            "ink_soft": ("ink", "ground", 0.34),
            "ink_faint": ("ink", "ground", 0.62),
            "rule": ("ink", "ground", 0.55),
            "panel": ("ground", "ink", 0.04),
            "dot": ("ink", "ground", 0.0),
            "dot_small": ("ink", "ground", 0.45),
            "ring_uncertain": ("ink", "ground", 0.25),
            "sea": ("water", "ground", 0.55),
            "lake": ("water", "ground", 0.40),
            "shore": ("water", "ink", 0.25),
        },
    },
    "d-copperplate": {
        "label": "D · Copperplate hachure",
        "relief_note": "Downslope strokes generated from the terrain "
                       "gradient. Steeper ground, heavier strokes. Below the "
                       "slope threshold the paper stays blank.",
        "note": "Blaeu and Cassini register. The most period-honest relief of "
                "the set: hachures are how relief was drawn before "
                "hillshading existed, so the technique is not a modern one in "
                "antique costume.",
        "relief": "hachure",
        "border": "double_rule",
        "caps_labels": False,
        "display": ["Didot", "Bodoni 72", "DejaVu Serif"],
        "text": ["Cochin", "Baskerville", "Palatino", "DejaVu Serif"],
        "track": 0.22,
        "bases": {
            # Laid paper of an eighteenth century atlas sheet, warm and light,
            # nothing like parchment: these were printed, not written.
            "ground": (None, "#f3ece0"),
            # Engraver's ink, a warm near-black rather than a flat black.
            "ink": (None, "#2b2a26"),
            # The pale blue-green wash hand-colourists laid over water.
            "water": (None, "#8fada6"),
            # The thin red wash used for routes and boundaries.
            "road": (None, "#a8574a"),
            # Route hue held constant across every register so R1-R7 stay
            # recognisable when the plates sit side by side.
            "route": ("A:route", A["route"]),
            "accent": (None, "#b0442c"),
        },
        "derived": {
            "halo": ("ground", "ground", 0.0),
            "ink_soft": ("ink", "ground", 0.36),
            "ink_faint": ("ink", "ground", 0.64),
            "rule": ("ink", "ground", 0.30),
            "panel": ("ground", "ink", 0.03),
            "dot": ("ink", "ground", 0.0),
            "dot_small": ("ink", "ground", 0.48),
            "ring_uncertain": ("ink", "ground", 0.30),
            "hachure": ("ink", "ground", 0.12),
            "sea": ("water", "ground", 0.50),
            "lake": ("water", "ground", 0.30),
            "shore": ("water", "ink", 0.35),
        },
    },
    "e-ptolemaic": {
        "label": "E · Ptolemaic woodcut",
        "relief_note": "Elevation posterized into cut bands with inked edges. "
                       "The band edges are isolines of the render grid, left "
                       "unlabelled.",
        "note": "Ulm Ptolemy 1482 register. Structurally the best fit of the "
                "set, because Ptolemy is a coordinate map: the graduated "
                "border belongs to the form rather than being decoration, and "
                "it is a natural home for provenance chips.",
        "relief": "bands",
        "border": "graduated",
        "caps_labels": False,
        "display": ["Palatino", "Iowan Old Style", "DejaVu Serif"],
        "text": ["Palatino", "Iowan Old Style", "DejaVu Serif"],
        "track": 0.24,
        "bases": {
            # Foxed paper of an early printed book.
            "ground": (None, "#eee2c8"),
            # Woodcut ink, brown-black from the block.
            "ink": (None, "#3a3226"),
            # The flat blue-green a colourist brushed into water on a
            # hand-coloured Ptolemy.
            "water": (None, "#86a9b0"),
            "road": (None, "#9d4b38"),
            "route": ("A:route", A["route"]),
            "accent": (None, "#b5442a"),
            # The tan of the pictorial hill bands.
            "hill": (None, "#cbac7c"),
        },
        "derived": {
            "halo": ("ground", "ground", 0.0),
            "ink_soft": ("ink", "ground", 0.34),
            "ink_faint": ("ink", "ground", 0.60),
            "rule": ("ink", "ground", 0.12),
            "panel": ("ground", "ink", 0.03),
            "dot": ("ink", "ground", 0.0),
            "dot_small": ("ink", "ground", 0.45),
            "ring_uncertain": ("ink", "ground", 0.28),
            "sea": ("water", "ground", 0.35),
            "lake": ("water", "ground", 0.20),
            "shore": ("water", "ink", 0.40),
            # Five cut bands, low to high.
            "band1": ("hill", "ground", 0.62),
            "band2": ("hill", "ground", 0.34),
            "band3": ("hill", "ground", 0.08),
            "band4": ("hill", "ink", 0.22),
            "band5": ("hill", "ink", 0.44),
        },
    },
    "f-incised": {
        "label": "F · Incised stone",
        "relief_note": "Relief cut as unlabelled contours, each with a lit and "
                       "a shadowed edge. No colour carries meaning except the "
                       "single ochre accent.",
        "note": "Forma Urbis Romae register. The strongest conceptual fit and "
                "the biggest risk: monochrome removes colour as a channel, so "
                "the marker system has to be carried by mark shape. The broken "
                "edge is material costume only and never punches a hole "
                "through the map.",
        "relief": "contour",
        "border": "broken_stone",
        "caps_labels": True,
        "display": ["Copperplate", "Optima", "DejaVu Serif"],
        "text": ["Optima", "Copperplate", "DejaVu Sans"],
        "track": 0.30,
        "bases": {
            # Weathered marble, lifted a little so a cut line has somewhere
            # to be dark against.
            "ground": (None, "#d9d2c4"),
            # The shadow inside a cut line.
            "ink": (None, "#3e392f"),
            "water": (None, "#6f6d61"),
            "road": (None, "#5d564a"),
            # The one accent: the red pigment traces that survive on the
            # Forma Urbis fragments. Everything else on this plate is stone.
            "route": (None, "#8a5a34"),
            "accent": (None, "#8a5a34"),
        },
        "derived": {
            # The lit lip of a cut, lighter than the stone around it.
            "halo": ("ground", "ink", 0.0),
            "lit": ("ground", "ink", -0.16),
            "ink_soft": ("ink", "ground", 0.30),
            "ink_faint": ("ink", "ground", 0.55),
            "rule": ("ink", "ground", 0.22),
            "panel": ("ground", "ink", 0.05),
            "dot": ("ink", "ground", 0.0),
            "dot_small": ("ink", "ground", 0.40),
            "ring_uncertain": ("ink", "ground", 0.26),
            "contour": ("ink", "ground", 0.22),
            "sea": ("water", "ground", 0.35),
            "lake": ("water", "ground", 0.25),
            "shore": ("water", "ink", 0.30),
        },
    },
}

ORDER = ["a-peutinger", "d-copperplate", "e-ptolemaic", "f-incised"]

PROVENANCE = (
    "Same committed corridor data in every plate: terrain SRTM via Terrain "
    "Tiles on AWS, places Pleiades, roads and water AWMC (Barrington). "
    "Relief treatment is styling; no place moves and no elevation figure is "
    "displayed (conventions v1.0 sections 4 and 6)."
)


def build_palette(spec):
    pal = {name: value for name, (_, value) in spec["bases"].items()}
    for name, (b1, b2, t) in spec["derived"].items():
        pal[name] = rio.mix(pal[b1], pal[b2], t)
    return pal


def verify_palettes():
    """Recompute every derived colour and re-check every A pull. Raise on drift."""
    bad = []
    for key, spec in REGISTERS.items():
        pal = build_palette(spec)
        for name, (prov, value) in spec["bases"].items():
            if prov and prov.startswith("A:"):
                akey = prov[2:]
                if akey not in A:
                    bad.append(f"{key}.{name}: A has no key {akey!r}")
                elif A[akey] != value:
                    bad.append(f"{key}.{name}: A[{akey!r}]={A[akey]} "
                               f"but base says {value}")
        for name, (b1, b2, t) in spec["derived"].items():
            if b1 not in pal or b2 not in pal:
                bad.append(f"{key}.{name}: mix names a base that does not exist")
                continue
            if pal[name] != rio.mix(pal[b1], pal[b2], t):
                bad.append(f"{key}.{name}: derived value does not recompute")
    if bad:
        raise SystemExit("palette drift:\n  " + "\n  ".join(bad))


verify_palettes()
PALETTES = {k: build_palette(v) for k, v in REGISTERS.items()}


def fpr(key, role, size, weight="normal", style="normal"):
    spec = REGISTERS[key]
    return FontProperties(family=spec[role], size=size, weight=weight,
                          style=style)


# ---------------------------------------------------------------------------
# Terrain, cropped once per plate.
# ---------------------------------------------------------------------------
def crop_dem(data, bbox, factor=1):
    d = data["dem"]
    elev = d["elev"].astype(np.float64)
    west, north, cell = (float(d["west"]), float(d["north"]),
                         float(d["cell_deg"]))
    c0 = max(0, int(round((bbox[0] - west) / cell)))
    c1 = min(elev.shape[1], int(round((bbox[2] - west) / cell)))
    r0 = max(0, int(round((north - bbox[3]) / cell)))
    r1 = min(elev.shape[0], int(round((north - bbox[1]) / cell)))
    z = elev[r0:r1, c0:c1]
    if factor > 1:
        nr = z.shape[0] // factor * factor
        nc = z.shape[1] // factor * factor
        z = z[:nr, :nc].reshape(nr // factor, factor,
                                nc // factor, factor).mean(axis=(1, 3))
        cell = cell * factor
    w0 = west + c0 * cell if factor == 1 else west + c0 * (cell / factor)
    n0 = north - r0 * cell if factor == 1 else north - r0 * (cell / factor)
    extent = (w0, w0 + z.shape[1] * cell, n0 - z.shape[0] * cell, n0)
    return z, cell, extent


def smooth(z, k):
    """Separable box blur, k cells wide. Keeps hachures from chasing noise."""
    if k <= 1:
        return z
    ker = np.ones(k) / k
    out = np.apply_along_axis(lambda r: np.convolve(r, ker, mode="same"), 1, z)
    return np.apply_along_axis(lambda c: np.convolve(c, ker, mode="same"), 0, out)


# ---------------------------------------------------------------------------
# Relief treatments. Each generated from the same DEM; only the drawing differs.
# ---------------------------------------------------------------------------
def relief_wash(ax, data, bbox, pal):
    z, cell, extent = crop_dem(data, bbox)
    sea = z <= 0
    mean_lat = (bbox[1] + bbox[3]) / 2
    cmap = LinearSegmentedColormap.from_list("a", A["terrain_stops"])
    ls = LightSource(azdeg=A["shade"]["azdeg"], altdeg=A["shade"]["altdeg"])
    shaded = ls.shade(np.where(sea, 0.0, z), cmap=cmap, blend_mode="soft",
                      vmin=0, vmax=4400,
                      dx=cell * m_per_deg_lon(mean_lat), dy=cell * M_PER_DEG_LAT,
                      vert_exag=A["shade"]["vert_exag"])
    shaded[sea] = matplotlib.colors.to_rgba(pal["sea"])
    field = rad.parchment_mottle(shaded.shape[:2], A["mottle"])
    shaded[:, :, :3] = np.clip(shaded[:, :, :3] * field[:, :, None], 0, 1)
    ax.imshow(shaded, extent=extent, origin="upper", zorder=1)


def relief_hachure(ax, data, bbox, pal, factor=3, interval=125, spacing=0.0052):
    """Lehmann hachures, built the way an engraver built them.

    Strokes are seeded along isolines at a fixed interval and run straight
    downslope, which is the classic construction: the strokes line up in ranks
    following the form, and because isolines crowd together on steep ground
    the ranks crowd with them. Steepness then also drives stroke length,
    weight and opacity, so steep ground goes dark and gentle ground stays
    near-blank paper, which is the whole point of the technique.

    Everything here comes from the committed DEM. The strokes carry direction
    and steepness only; no magnitude is stated and no figure is displayed.
    """
    z, cell, extent = crop_dem(data, bbox, factor=factor)
    z = smooth(z, 5)
    rows, cols = z.shape
    lons = extent[0] + (np.arange(cols) + 0.5) * cell
    lats = extent[3] - (np.arange(rows) + 0.5) * cell
    mean_lat = (bbox[1] + bbox[3]) / 2
    lon_scale = m_per_deg_lon(mean_lat) / M_PER_DEG_LAT

    # Row 0 is north, so the north-positive derivative is the negated one.
    dzdy = -np.gradient(z, cell * M_PER_DEG_LAT, axis=0)
    dzdx = np.gradient(z, cell * m_per_deg_lon(mean_lat), axis=1)
    slope = np.hypot(dzdx, dzdy)

    # Isolines via a throwaway figure, so this needs no dependency beyond
    # matplotlib itself.
    tmp = plt.figure()
    cs = tmp.add_subplot().contour(
        lons, lats, z, levels=list(range(interval, 4400, interval)))
    lines = []
    for p in cs.get_paths():
        for poly in p.to_polygons(closed_only=False):
            if len(poly) > 2:
                lines.append(np.asarray(poly))
    plt.close(tmp)

    xs0, ys0, tt = [], [], []
    for line in lines:
        x, y = line[:, 0], line[:, 1]
        d = np.hypot(np.diff(x) * lon_scale, np.diff(y))
        c = np.concatenate([[0.0], np.cumsum(d)])
        if c[-1] < spacing:
            continue
        n = int(c[-1] // spacing)
        targets = (np.arange(n) + 0.5) * spacing
        xs0.append(np.interp(targets, c, x))
        ys0.append(np.interp(targets, c, y))
    if not xs0:
        return
    xs0 = np.concatenate(xs0)
    ys0 = np.concatenate(ys0)

    jj = np.clip(((xs0 - extent[0]) / cell - 0.5).round().astype(int), 0, cols - 1)
    ii = np.clip(((extent[3] - ys0) / cell - 0.5).round().astype(int), 0, rows - 1)
    s = slope[ii, jj]
    keep = s > 0.05                       # about 2.9 degrees; below this, paper
    xs0, ys0, ii, jj, s = xs0[keep], ys0[keep], ii[keep], jj[keep], s[keep]

    gx, gy = dzdx[ii, jj], dzdy[ii, jj]
    mag = np.hypot(gx, gy)
    mag[mag == 0] = 1.0
    ux, uy = -gx / mag, -gy / mag         # downslope unit vector

    t = np.clip(s / 0.62, 0.0, 1.0)       # 0.62 is roughly a 32 degree slope
    length = spacing * (0.55 + 0.85 * t)
    xs1 = xs0 + ux * length / lon_scale
    ys1 = ys0 + uy * length

    segs = np.stack([np.column_stack([xs0, ys0]),
                     np.column_stack([xs1, ys1])], axis=1)
    ax.add_collection(LineCollection(
        segs, colors=pal["hachure"], linewidths=0.28 + 0.80 * t,
        alpha=np.clip(0.28 + 0.62 * t, 0, 1), capstyle="butt", zorder=1.5))
    print(f"    hachures: {len(segs)} strokes seeded along "
          f"{len(lines)} isolines at {interval} m")


def relief_bands(ax, data, bbox, pal, factor=3):
    """Posterized cut bands with inked edges, the woodcut answer to relief.

    Smoothed harder than the other treatments on purpose: a block cut by hand
    simplifies, and an unsimplified isoline reads as a machine artefact rather
    than a cut.
    """
    z, cell, extent = crop_dem(data, bbox, factor=factor)
    z = smooth(z, 11)
    lons = extent[0] + (np.arange(z.shape[1]) + 0.5) * cell
    lats = extent[3] - (np.arange(z.shape[0]) + 0.5) * cell
    levels = [-100, 300, 900, 1600, 2400, 6000]
    colors = [pal["band1"], pal["band2"], pal["band3"], pal["band4"],
              pal["band5"]]
    ax.contourf(lons, lats, z, levels=levels, colors=colors, zorder=1,
                extend="neither")
    ax.contour(lons, lats, z, levels=levels[1:-1], colors=pal["ink"],
               linewidths=0.85, zorder=1.4)
    print(f"    bands: {len(levels) - 1} cut bands on a "
          f"{z.shape[0]}x{z.shape[1]} grid")


def relief_contour(ax, data, bbox, pal, factor=2):
    """Cut contours, doubled with a lit lip so the line reads as incised.

    The contours are deliberately unlabelled: this is a relief treatment, not
    an elevation readout (conventions section 4).
    """
    z, cell, extent = crop_dem(data, bbox, factor=factor)
    z = smooth(z, 9)
    lons = extent[0] + (np.arange(z.shape[1]) + 0.5) * cell
    lats = extent[3] - (np.arange(z.shape[0]) + 0.5) * cell
    levels = list(range(300, 4400, 300))
    off = cell * 1.4
    # Lit lip first, offset up and left, then the shadowed cut over it.
    ax.contour(lons + off, lats + off, z, levels=levels, colors=pal["lit"],
               linewidths=1.0, zorder=1.3)
    ax.contour(lons, lats, z, levels=levels, colors=pal["contour"],
               linewidths=0.9, zorder=1.4)
    print(f"    contours: {len(levels)} unlabelled levels on a "
          f"{z.shape[0]}x{z.shape[1]} grid")


RELIEF = {
    "wash": relief_wash,
    "hachure": relief_hachure,
    "bands": relief_bands,
    "contour": relief_contour,
}


# ---------------------------------------------------------------------------
# Shared map furniture, drawn identically in every register.
# ---------------------------------------------------------------------------
def draw_hydrography_and_roads(ax, data, pal, key):
    for ft in data["lakes"]["features"]:
        for ring in rad.polygon_rings(ft["geometry"]):
            ax.add_patch(MplPolygon([(p[0], p[1]) for p in ring], closed=True,
                                    facecolor=pal["lake"], edgecolor="none",
                                    zorder=2))
    for ft in data["river_network"]["features"]:
        for part in rad.line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=pal["water"], lw=0.7, alpha=0.7, zorder=2.4,
                    solid_capstyle="round")
    for ft in data["rivers"]["features"]:
        named = ft["properties"]["pid"] is not None
        for part in rad.line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=pal["water"], lw=1.6 if named else 1.0,
                    alpha=0.92, zorder=2.5, solid_capstyle="round")
    for ft in data["shore"]["features"]:
        for part in rad.line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=pal["shore"], lw=1.1, zorder=3)
    for ft in data["roads"]["features"]:
        for part in rad.line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=pal["road"], lw=0.9, alpha=0.85, zorder=4,
                    solid_capstyle="round")


def keyed(ax, text, lon, lat, dx, dy, color, key, size, halo):
    ax.annotate(text, (lon, lat), xytext=(lon + dx, lat + dy),
                ha="left" if dx >= 0 else "right",
                fontproperties=fpr(key, "text", size, weight="bold"),
                color=color, zorder=8,
                path_effects=[patheffects.withStroke(linewidth=3.0,
                                                     foreground=halo)])


def draw_markers_and_labels(ax, data, pal, key):
    spec = REGISTERS[key]
    setts, others, uncertain, candidates, by_pid = rio.classify_places(data)
    if others:
        xs, ys = zip(*others)
        ax.scatter(xs, ys, s=rad.S_OTHER, c=pal["dot_small"], alpha=0.55, lw=0,
                   zorder=5)
    if setts:
        xs, ys = zip(*setts)
        ax.scatter(xs, ys, s=rad.S_SETTLEMENT, c=pal["dot"],
                   edgecolors=pal["halo"], lw=0.4, zorder=6)
    if uncertain:
        xs, ys = zip(*uncertain)
        ax.scatter(xs, ys, s=rad.S_RING, facecolors="none",
                   edgecolors=pal["ring_uncertain"], lw=1.1, zorder=6)
    for i, (pid, lon, lat) in enumerate(candidates, start=1):
        ax.scatter([lon], [lat], s=rad.S_RING_CANDIDATE, facecolors="none",
                   edgecolors=pal["accent"], lw=1.6, zorder=7)
        dx, dy = rad.CANDIDATE_LABEL_OFFSETS.get(pid, (0.03, 0.025))
        keyed(ax, f"C{i}", lon, lat, dx, dy, pal["accent"], key, 9.5,
              pal["halo"])
    for rk, _name, lon, lat in rio.route_points(by_pid):
        ax.scatter([lon], [lat], s=rad.S_ROUTE, marker="D", facecolors="none",
                   edgecolors=pal["route"], lw=1.6, zorder=7)
        dx, dy = rad.ROUTE_LABEL_OFFSETS.get(rk, (0.03, 0.025))
        keyed(ax, rk, lon, lat, dx, dy, pal["route"], key, 9.5, pal["halo"])

    inset = 0.06
    for pid, (label, side, dy) in rad.LABELS.items():
        ft = by_pid.get(pid)
        if ft is None:
            continue
        lon, lat = ft["geometry"]["coordinates"][:2]
        if not (BBOX[0] + inset <= lon <= BBOX[2] - inset
                and BBOX[1] + inset <= lat <= BBOX[3] - inset):
            continue
        if spec["caps_labels"]:
            label = label.upper()
        dx = 0.035 if side == "right" else -0.035
        ax.annotate(label, (lon, lat), xytext=(lon + dx, lat + dy),
                    ha="left" if side == "right" else "right", va="center",
                    fontproperties=fpr(key, "text", 9.5),
                    color=pal["ink"], zorder=8,
                    path_effects=[patheffects.withStroke(
                        linewidth=3.2, foreground=pal["halo"])])
    for text, lon, lat, rot in rad.RIVER_LABELS:
        if not (BBOX[0] + inset <= lon <= BBOX[2] - inset
                and BBOX[1] + inset <= lat <= BBOX[3] - inset):
            continue
        if spec["caps_labels"]:
            text = text.upper()
        ax.annotate(text, (lon, lat), fontproperties=fpr(key, "text", 9.5,
                                                         style="italic"),
                    color=pal["shore"], rotation=rot, rotation_mode="anchor",
                    ha="center", va="center", zorder=8,
                    path_effects=[patheffects.withStroke(
                        linewidth=3.0, foreground=pal["halo"])])


# ---------------------------------------------------------------------------
# Borders, one per register.
# ---------------------------------------------------------------------------
def border_double_rule(fig, ax, rect, pal, key):
    rio.double_rule(fig, (rect[0] - 0.014, rect[1] - 0.011,
                          rect[2] + 0.028, rect[3] + 0.022),
                    outer=1.5, inner=0.6, gap=0.004, color=pal["rule"],
                    zorder=20)


def border_graduated(fig, ax, rect, pal, key):
    """The graduated frame of a Ptolemaic sheet: degree ticks in cut bands.

    Drawn in axes coordinates so it hugs the map exactly, with alternating
    inked and blank cells at quarter-degree steps and the whole degrees
    labelled. This is native furniture on a coordinate map, not decoration.
    """
    band = 0.018
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, fill=False,
                           edgecolor=pal["ink"], lw=1.0, zorder=12))
    step = 0.25
    for axis in ("x", "y"):
        lo, hi = (BBOX[0], BBOX[2]) if axis == "x" else (BBOX[1], BBOX[3])
        start = np.ceil(lo / step) * step
        vals = np.arange(start, hi + 1e-9, step)
        for n, v in enumerate(vals[:-1]):
            v2 = min(vals[n + 1], hi)
            f0, f1 = (v - lo) / (hi - lo), (v2 - lo) / (hi - lo)
            filled = n % 2 == 0
            face = pal["ink"] if filled else pal["ground"]
            for side in (0, 1):
                if axis == "x":
                    xy = (f0, -band if side == 0 else 1.0)
                    w, h = f1 - f0, band
                else:
                    xy = (-band if side == 0 else 1.0, f0)
                    w, h = band, f1 - f0
                ax.add_patch(Rectangle(xy, w, h, transform=ax.transAxes,
                                       facecolor=face, edgecolor=pal["ink"],
                                       lw=0.6, zorder=12, clip_on=False))
        for v in vals:
            if abs(v - round(v)) > 1e-6:
                continue
            f = (v - lo) / (hi - lo)
            if axis == "x":
                ax.text(f, -band - 0.006, f"{int(round(v))}°",
                        transform=ax.transAxes, ha="center", va="top",
                        fontproperties=fpr(key, "text", 8),
                        color=pal["ink_soft"], zorder=12, clip_on=False)
            else:
                ax.text(-band - 0.005, f, f"{int(round(v))}°",
                        transform=ax.transAxes, ha="right", va="center",
                        fontproperties=fpr(key, "text", 8),
                        color=pal["ink_soft"], zorder=12, clip_on=False)
    # A light graticule, so the border's promise is kept inside the map.
    for v in np.arange(np.ceil(BBOX[0] / 0.5) * 0.5, BBOX[2], 0.5):
        ax.axvline(v, color=pal["ink"], lw=0.4, alpha=0.28, zorder=4.5)
    for v in np.arange(np.ceil(BBOX[1] / 0.5) * 0.5, BBOX[3], 0.5):
        ax.axhline(v, color=pal["ink"], lw=0.4, alpha=0.28, zorder=4.5)


def broken_edge_path(rect, seed=218, teeth=46, chip=0.010):
    """A deterministic chipped rectangle. Material costume, nothing more."""
    rng = np.random.default_rng(seed)
    x, y, w, h = rect
    pts = []

    def edge(x0, y0, x1, y1, nx, ny):
        for t in np.linspace(0, 1, teeth, endpoint=False):
            j = rng.random()
            d = chip * (0.15 + 0.85 * j ** 2)
            if rng.random() < 0.10:
                d *= 2.4                      # occasional larger chip
            pts.append((x0 + (x1 - x0) * t + nx * d,
                        y0 + (y1 - y0) * t + ny * d))

    edge(x, y, x + w, y, 0, 1)
    edge(x + w, y, x + w, y + h, -1, 0)
    edge(x + w, y + h, x, y + h, 0, -1)
    edge(x, y + h, x, y, 1, 0)
    pts.append(pts[0])
    return Path(np.array(pts), closed=True)


def border_broken_stone(fig, ax, rect, pal, key):
    """Mask everything outside a chipped boundary with the page ground.

    Built as a compound path, the figure rectangle with the fragment as a
    hole, so it masks reliably without needing a clip path on every artist.
    Applied to the plate boundary only: it never removes ground from the
    middle of the map, because an absence of stone over real terrain would
    assert an absence of evidence that is not there.
    """
    frag = broken_edge_path(rect)
    outer = Path([(0, 0), (1, 0), (1, 1), (0, 1), (0, 0)], closed=True)
    verts = np.vstack([outer.vertices, frag.vertices[::-1]])
    codes = np.concatenate([outer.codes if outer.codes is not None
                            else [Path.MOVETO] + [Path.LINETO] * 3 + [Path.CLOSEPOLY],
                            [Path.MOVETO] + [Path.LINETO] * (len(frag.vertices) - 2)
                            + [Path.CLOSEPOLY]])
    fig.add_artist(PathPatch(Path(verts, codes), transform=fig.transFigure,
                             facecolor=pal["panel"], edgecolor="none",
                             zorder=15))
    fig.add_artist(PathPatch(frag, transform=fig.transFigure, facecolor="none",
                             edgecolor=pal["ink"], lw=1.1, alpha=0.55,
                             zorder=16))


BORDER = {
    "double_rule": border_double_rule,
    "graduated": border_graduated,
    "broken_stone": border_broken_stone,
}


# ---------------------------------------------------------------------------
# One plate per register.
# ---------------------------------------------------------------------------
def plate(key, data, out_path):
    spec = REGISTERS[key]
    pal = PALETTES[key]
    print(f"  {key}")

    fig = plt.figure(figsize=(FIGW, FIGH), dpi=DPI)
    fig.patch.set_facecolor(pal["panel"])

    pw = 0.760
    ph = pw * (FIGW / FIGH) * rio.bbox_aspect(BBOX)
    px = (1.0 - pw) / 2
    py = 0.958 - ph
    ax = fig.add_axes([px, py, pw, ph])
    ax.set_facecolor(pal["ground"])

    RELIEF[spec["relief"]](ax, data, BBOX, pal)
    draw_hydrography_and_roads(ax, data, pal, key)
    draw_markers_and_labels(ax, data, pal, key)

    ax.set_xlim(BBOX[0], BBOX[2])
    ax.set_ylim(BBOX[1], BBOX[3])
    ax.set_aspect(M_PER_DEG_LAT / m_per_deg_lon((BBOX[1] + BBOX[3]) / 2))
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)

    BORDER[spec["border"]](fig, ax, (px, py, pw, ph), pal, key)

    def block(y, text, width, size, color, lead):
        for line in rio._wrap(text, width).split("\n"):
            fig.text(px, y, line, ha="left", va="top",
                     fontproperties=fpr(key, "text", size), color=color,
                     zorder=30)
            y -= lead
        return y

    top = py - 0.052
    disp = spec["label"].split(" · ", 1)[1].upper()
    fig.text(px, top, rio.track(disp, spec["track"]), ha="left", va="center",
             fontproperties=fpr(key, "display", 22), color=pal["ink"],
             zorder=30)
    fig.text(px + pw, top, "variation, not a decision", ha="right",
             va="center", fontproperties=fpr(key, "text", 9),
             color=pal["ink_faint"], zorder=30)
    fig.add_artist(Line2D([px, px + pw], [top - 0.026, top - 0.026],
                          color=pal["rule"], lw=1.0, transform=fig.transFigure,
                          zorder=30))
    y = block(top - 0.048, spec["relief_note"], 88, 11, pal["ink"], 0.019)
    y = block(y - 0.007, spec["note"], 96, 9.5, pal["ink_soft"], 0.0175)
    y = block(y - 0.007, PROVENANCE, 112, 7.5, pal["ink_faint"], 0.0145)
    if y < 0.010:
        print(f"    WARNING: caption runs off the plate (y={y:.3f})")

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, facecolor=pal["panel"], dpi=DPI)
    plt.close(fig)
    print(f"    wrote {os.path.relpath(out_path)}")


def comparison_sheet(out_path):
    from PIL import Image

    imgs = [(Image.open(os.path.join(OUT_DIR, f"{k}.png")),
             REGISTERS[k]["label"]) for k in ORDER]
    PANEL_H, GAP, SIDE, TOP, BOT = 8.6, 0.5, 0.55, 1.0, 0.6
    widths = [PANEL_H * im.width / im.height for im, _ in imgs]
    figw = sum(widths) + GAP * (len(imgs) - 1) + 2 * SIDE
    figh = PANEL_H + TOP + BOT
    ground = PALETTES["a-peutinger"]["panel"]
    ink = PALETTES["a-peutinger"]["ink"]

    fig = plt.figure(figsize=(figw, figh), dpi=DPI)
    fig.patch.set_facecolor(ground)
    x = SIDE
    for (im, label), w in zip(imgs, widths):
        ax = fig.add_axes([x / figw, BOT / figh, w / figw, PANEL_H / figh])
        ax.imshow(np.asarray(im))
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor(PALETTES["a-peutinger"]["rule"])
        fig.text((x + w / 2) / figw, (BOT + PANEL_H + 0.14) / figh, label,
                 ha="center", va="bottom",
                 fontproperties=fpr("a-peutinger", "text", 13), color=ink)
        x += w + GAP
    fig.text(0.5, 1 - 0.28 / figh,
             "The March · variations within the ancient-map register. "
             "Same Alps-detail data, same marker grammar, four ideas of what "
             "an ancient map is.",
             ha="center", va="top",
             fontproperties=fpr("a-peutinger", "text", 16), color=ink)
    fig.text(0.5, 0.26 / figh,
             "Each register declares a closed palette and every relief "
             "treatment is generated from the committed DEM. None of these is "
             "a decision.",
             ha="center", va="center",
             fontproperties=fpr("a-peutinger", "text", 10),
             color=PALETTES["a-peutinger"]["ink_soft"])
    fig.savefig(out_path, facecolor=ground, dpi=DPI)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def main():
    data = rad.load_data()
    print("rendering register variations")
    for key in ORDER:
        plate(key, data, os.path.join(OUT_DIR, f"{key}.png"))
    comparison_sheet(os.path.join(OUT_DIR, "register-variants.png"))


if __name__ == "__main__":
    main()
