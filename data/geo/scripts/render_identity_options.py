#!/usr/bin/env python3
"""Identity / brand OPTIONS in the ancient-map (A) register. Nothing here is final.

Three option artifacts for Tony to react to, all rendered from the committed
processed data through the existing Direction A style dict in
`render_art_direction.py` (imported, never copied):

  1  site/poc/identity-options/1-title-card/title-card.png
     Title-card treatment: "The March", subtitle "Hannibal and the war that
     nearly ended Rome", set in a cartouche over the A-register corridor
     render (the committed corridor-full bbox).
     Plus title-card-typography.png, the same card in three type settings.

  2  site/poc/identity-options/2-frontispiece-the-crossing/
     frontispiece-the-crossing.png
     Chapter frontispiece for chapter one, The Crossing, over the A-register
     Alps detail view: a plate in a ruled frame with chapter number, title,
     an attested standfirst with its anchor, and the open route gap named.

  3  site/poc/identity-options/3-route-debate/route-debate.png
     The route debate staged as an A-register artifact: R1-R7 drawn as seven
     competing corridors with keyed labels, a backer key, and the uncertainty
     kept explicit rather than resolved.

  contact sheet: site/poc/identity-options/contact-sheet.png

Colour rule for this build
-------------------------
Every colour traces to a declared palette (PALETTE below). Each entry is
either pulled straight from the committed A style dict, or a declared
deterministic mix of two such pulls with the mix stated. `verify_palette()`
runs on import and raises if any "A:<key>" entry has drifted from
`render_art_direction.STYLES["a-ancient-map"]`, so this file cannot silently
disagree with the register it claims to be in. Typography is the one thing
explored freely here; the brief allows it.

Geography rule for the route plate (conventions v1.0 sections 3, 4 and 6)
------------------------------------------------------------------------
No route line is freehand and none is attested. Each drawn corridor is built
from two visually distinguished parts:

  solid   the AWMC river polyline itself (Druentia or Isara on the west, the
          named descent river on the east), drawn as committed geometry;
  dashed  a least-cost traverse computed over the corridor DEM between the
          river and the candidate pass, using Tobler's hiking function as the
          cost. Computed on the visualization render grid, coarsened 3x, so
          it is indicative of a corridor and nothing finer.

Neither part is an attested itinerary. Polybius names no pass; Livy 21.38
rules out the Poenine Pass and Caelius Antipater's "heights of Cremo"; Nepos
3.4 says only "the Graian pass" (claims ledger TC-19, gap G-1). The plate
says this on its face. No elevation figure is displayed anywhere in these
plates, per the section 4 amendment.

Run with the project venv:
  .venv/bin/python data/geo/scripts/render_identity_options.py
"""

import heapq
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as patheffects
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LightSource, LinearSegmentedColormap
from matplotlib.font_manager import FontProperties
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon as MplPolygon, Rectangle

import render_art_direction as rad

A = rad.STYLES["a-ancient-map"]
OUT_DIR = os.path.join(rad.OUT_DIR, "..", "identity-options")
DPI = 150


# ---------------------------------------------------------------------------
# Declared palette. Nothing in this file may use a colour that is not here.
# ---------------------------------------------------------------------------
def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _hex(rgb):
    return "#%02x%02x%02x" % tuple(int(round(c)) for c in rgb)


def mix(h1, h2, t):
    """Linear sRGB-space blend, t=0 gives h1 and t=1 gives h2."""
    a, b = _rgb(h1), _rgb(h2)
    return _hex(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


# name -> (value, provenance). "A:<key>" means taken verbatim from the
# committed Direction A style dict; "mix(...)" states the derivation.
PALETTE = {
    "ground":          (A["face"],            "A:face"),
    "ink":             (A["text"],            "A:text"),
    "halo":            (A["halo"],            "A:halo"),
    "panel":           (A["legend_face"],     "A:legend_face"),
    "rule":            (A["legend_edge"],     "A:legend_edge"),
    "tick":            (A["tick"],            "A:tick"),
    "sea":             (A["sea"],             "A:sea"),
    "lake":            (A["lake"],            "A:lake"),
    "river":           (A["river"],           "A:river"),
    "shore":           (A["shore"],           "A:shore"),
    "road":            (A["road"],            "A:road"),
    "dot":             (A["dot"],             "A:dot"),
    "dot_small":       (A["dot_small"],       "A:dot_small"),
    "ring_uncertain":  (A["ring_uncertain"],  "A:ring_uncertain"),
    "ring_candidate":  (A["ring_candidate"],  "A:ring_candidate"),
    "route":           (A["route"],           "A:route"),
    # Declared derivations. Each is a stated mix of two entries above; no
    # colour is chosen by eye.
    "ink_soft":        (mix(A["text"], A["face"], 0.34),
                        "mix(A:text, A:face, 0.34)"),
    "ink_faint":       (mix(A["text"], A["face"], 0.62),
                        "mix(A:text, A:face, 0.62)"),
    "rule_light":      (mix(A["legend_edge"], A["face"], 0.50),
                        "mix(A:legend_edge, A:face, 0.50)"),
    "route_soft":      (mix(A["route"], A["face"], 0.45),
                        "mix(A:route, A:face, 0.45)"),
    "refuted":         (mix(A["ring_uncertain"], A["face"], 0.42),
                        "mix(A:ring_uncertain, A:face, 0.42)"),
    "panel_deep":      (mix(A["legend_face"], A["text"], 0.07),
                        "mix(A:legend_face, A:text, 0.07)"),
}


def verify_palette():
    """Fail loudly if any A: pull has drifted from the committed A style dict."""
    bad = []
    for name, (value, prov) in PALETTE.items():
        if prov.startswith("A:"):
            key = prov[2:]
            if key not in A:
                bad.append(f"{name}: A has no key {key!r}")
            elif A[key] != value:
                bad.append(f"{name}: A[{key!r}]={A[key]} but palette says {value}")
    if bad:
        raise SystemExit(
            "palette drift against render_art_direction.STYLES"
            "['a-ancient-map']:\n  " + "\n  ".join(bad)
        )


verify_palette()


def C(name):
    return PALETTE[name][0]


# ---------------------------------------------------------------------------
# Typography. The one layer this build explores. Every stack ends in a font
# matplotlib always ships, so a machine without the macOS faces still renders.
# ---------------------------------------------------------------------------
TYPE_SETTINGS = {
    "inscriptional": {
        "label": "Inscriptional",
        "note": "Copperplate display over Hoefler Text. Roman lettering on "
                "the monument, book text underneath.",
        "display": ["Copperplate", "Optima", "DejaVu Serif"],
        "display_caps": True,
        "display_track": 0.28,
        "display_scale": 1.00,
        "text": ["Hoefler Text", "Iowan Old Style", "Palatino", "DejaVu Serif"],
        "display_weight": "bold",
    },
    "register": {
        "label": "Register-true",
        "note": "Hoefler Text throughout, letterspaced caps for the display "
                "line. The A register's own lettering, nothing added.",
        "display": ["Hoefler Text", "Iowan Old Style", "Palatino", "DejaVu Serif"],
        "display_caps": True,
        "display_track": 0.30,
        "display_scale": 0.86,
        "text": ["Hoefler Text", "Iowan Old Style", "Palatino", "DejaVu Serif"],
        "display_weight": "normal",
    },
    "engraved": {
        "label": "Engraved plate",
        "note": "Didot display over Cochin. Reads as an eighteenth century "
                "atlas plate rather than an ancient object.",
        "display": ["Didot", "Bodoni 72", "DejaVu Serif"],
        "display_caps": True,
        "display_track": 0.22,
        "display_scale": 0.90,
        "text": ["Cochin", "Baskerville", "Palatino", "DejaVu Serif"],
        "display_weight": "normal",
    },
}
PRIMARY_SETTING = "inscriptional"

# Modern-gloss disambiguation, local to these plates. Pleiades 167650 is
# titled "Aquae Sextiae" but its own description reads "modern Aix-les-Bains",
# and it sits at 5.92E 45.69N in Savoie. The shared renderer's gloss, "(Aix)",
# reads as Aix-en-Provence, a different town. Corrected here from the source
# record; the shared LABELS dict still carries the old gloss and is flagged
# separately rather than edited from a brand session.
LABEL_GLOSS = {
    "167650": "Aquae Sextiae\n(Aix-les-Bains)",
}


def fp(setting, role, size, weight=None, style=None):
    s = TYPE_SETTINGS[setting]
    if role == "display":
        size = size * s["display_scale"]
    return FontProperties(
        family=s["display"] if role == "display" else s["text"],
        size=size,
        weight=weight or ("normal" if role != "display" else s["display_weight"]),
        style=style or "normal",
    )


def track(text, amount):
    """Emulate letterspacing; matplotlib has no tracking control."""
    if amount <= 0:
        return text
    gap = " " * max(1, int(round(amount * 4)))
    return gap.join(list(text))


# ---------------------------------------------------------------------------
# Shared A-register basemap. Same data, same style dict, same draw order as
# render_art_direction.render, with the comparison-sheet chrome (axes, legend,
# colorbar, title) left off because these are designed plates.
# ---------------------------------------------------------------------------
def shaded_terrain(elev, sea, cell, mean_lat, mottle=True):
    m_per_deg_lat = 110_574.0
    m_per_deg_lon = 111_320.0 * np.cos(np.radians(mean_lat))
    cmap = LinearSegmentedColormap.from_list("a-ancient-map", A["terrain_stops"])
    ls = LightSource(azdeg=A["shade"]["azdeg"], altdeg=A["shade"]["altdeg"])
    shaded = ls.shade(
        np.where(sea, 0.0, elev), cmap=cmap, blend_mode="soft",
        vmin=0, vmax=4400,
        dx=cell * m_per_deg_lon, dy=cell * m_per_deg_lat,
        vert_exag=A["shade"]["vert_exag"],
    )
    shaded[sea] = matplotlib.colors.to_rgba(C("sea"))
    if mottle:
        field = rad.parchment_mottle(shaded.shape[:2], A["mottle"])
        shaded[:, :, :3] = np.clip(shaded[:, :, :3] * field[:, :, None], 0, 1)
    return shaded


def basemap(ax, bbox, data, *, roads=True, mottle=True, river_lw=1.0):
    d = data["dem"]
    elev = d["elev"].astype(np.float64)
    west, north, cell = float(d["west"]), float(d["north"]), float(d["cell_deg"])
    rows, cols = elev.shape
    east = west + cols * cell
    south = north - rows * cell
    sea = elev <= 0
    mean_lat = (bbox[1] + bbox[3]) / 2

    ax.imshow(
        shaded_terrain(elev, sea, cell, mean_lat, mottle),
        extent=(west, east, south, north), origin="upper", zorder=1,
    )
    for ft in data["lakes"]["features"]:
        for ring in rad.polygon_rings(ft["geometry"]):
            ax.add_patch(MplPolygon([(p[0], p[1]) for p in ring], closed=True,
                                    facecolor=C("lake"), edgecolor="none", zorder=2))
    for ft in data["river_network"]["features"]:
        for part in rad.line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=C("river"), lw=0.7 * river_lw, alpha=0.65,
                    zorder=2.4, solid_capstyle="round")
    for ft in data["rivers"]["features"]:
        named = ft["properties"]["pid"] is not None
        for part in rad.line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=C("river"), lw=(1.6 if named else 1.0) * river_lw,
                    alpha=0.9, zorder=2.5, solid_capstyle="round")
    for ft in data["shore"]["features"]:
        for part in rad.line_parts(ft["geometry"]):
            xs, ys = zip(*[(p[0], p[1]) for p in part])
            ax.plot(xs, ys, color=C("shore"), lw=1.1, zorder=3)
    if roads:
        for ft in data["roads"]["features"]:
            for part in rad.line_parts(ft["geometry"]):
                xs, ys = zip(*[(p[0], p[1]) for p in part])
                ax.plot(xs, ys, color=C("road"), lw=0.9, alpha=A["road_alpha"],
                        zorder=4, solid_capstyle="round")

    ax.set_xlim(bbox[0], bbox[2])
    ax.set_ylim(bbox[1], bbox[3])
    m_per_deg_lat = 110_574.0
    m_per_deg_lon = 111_320.0 * np.cos(np.radians(mean_lat))
    ax.set_aspect(m_per_deg_lat / m_per_deg_lon)
    ax.set_xticks([])
    ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def classify_places(data):
    """The POC's four mutually exclusive classes, over the full corridor bbox."""
    full = rad.VIEWS[0][2]
    setts, others, uncertain, candidates = [], [], [], []
    by_pid = {}
    for ft in data["places"]["features"]:
        p = ft["properties"]
        by_pid[p["pid"]] = ft
        lon, lat = ft["geometry"]["coordinates"][:2]
        if not (full[0] <= lon <= full[2] and full[1] <= lat <= full[3]):
            continue
        if p["pid"] in rad.PASS_CANDIDATES:
            candidates.append((p["pid"], lon, lat))
        elif p.get("locationCertainty") not in ("certain", None):
            uncertain.append((lon, lat))
        elif "settlement" in (p["placeTypes"] or []):
            setts.append((lon, lat))
        else:
            others.append((lon, lat))
    return setts, others, uncertain, sorted(candidates), by_pid


def draw_places(ax, data, *, with_candidates=True, with_routes=True,
                setting=PRIMARY_SETTING, key_size=9.5):
    setts, others, uncertain, candidates, by_pid = classify_places(data)
    if others:
        xs, ys = zip(*others)
        ax.scatter(xs, ys, s=rad.S_OTHER, c=C("dot_small"), alpha=0.55, lw=0, zorder=5)
    if setts:
        xs, ys = zip(*setts)
        ax.scatter(xs, ys, s=rad.S_SETTLEMENT, c=C("dot"), edgecolors=C("halo"),
                   lw=0.4, zorder=6)
    if uncertain:
        xs, ys = zip(*uncertain)
        ax.scatter(xs, ys, s=rad.S_RING, facecolors="none",
                   edgecolors=C("ring_uncertain"), lw=1.1, zorder=6)
    if with_candidates:
        for i, (pid, lon, lat) in enumerate(candidates, start=1):
            ax.scatter([lon], [lat], s=rad.S_RING_CANDIDATE, facecolors="none",
                       edgecolors=C("ring_candidate"), lw=1.6, zorder=7)
            dx, dy = rad.CANDIDATE_LABEL_OFFSETS.get(pid, (0.03, 0.025))
            keyed(ax, f"C{i}", lon, lat, dx, dy, C("ring_candidate"),
                  setting, key_size)
    if with_routes:
        for key, name, lon, lat in route_points(by_pid):
            ax.scatter([lon], [lat], s=rad.S_ROUTE, marker="D", facecolors="none",
                       edgecolors=C("route"), lw=1.6, zorder=7)
            dx, dy = rad.ROUTE_LABEL_OFFSETS.get(key, (0.03, 0.025))
            keyed(ax, key, lon, lat, dx, dy, C("route"), setting, key_size)
    return by_pid


def keyed(ax, text, lon, lat, dx, dy, color, setting, size):
    ax.annotate(
        text, (lon, lat), xytext=(lon + dx, lat + dy),
        ha="left" if dx >= 0 else "right",
        fontproperties=fp(setting, "text", size, weight="bold"),
        color=color, zorder=8,
        path_effects=[patheffects.withStroke(linewidth=3.0, foreground=C("halo"))],
    )


def draw_labels(ax, by_pid, setting, size=10, rivers=True, bbox=None,
                inset=0.0):
    """Place and river labels. `bbox` drops anything outside the view so no
    label bleeds past the plate frame; `inset` keeps edge labels off the rule."""
    def inside(lon, lat):
        if bbox is None:
            return True
        return (bbox[0] + inset <= lon <= bbox[2] - inset
                and bbox[1] + inset <= lat <= bbox[3] - inset)

    for pid, (label, side, dy) in rad.LABELS.items():
        ft = by_pid.get(pid)
        if ft is None:
            continue
        lon, lat = ft["geometry"]["coordinates"][:2]
        if not inside(lon, lat):
            continue
        label = LABEL_GLOSS.get(pid, label)
        dx = 0.035 if side == "right" else -0.035
        ax.annotate(
            label, (lon, lat), xytext=(lon + dx, lat + dy),
            ha="left" if side == "right" else "right", va="center",
            fontproperties=fp(setting, "text", size), color=C("ink"), zorder=8,
            path_effects=[patheffects.withStroke(linewidth=3.2,
                                                 foreground=C("halo"))],
        )
    if rivers:
        for text, lon, lat, rot in rad.RIVER_LABELS:
            if not inside(lon, lat):
                continue
            ax.annotate(
                text, (lon, lat),
                fontproperties=fp(setting, "text", size, style="italic"),
                color=C("river"), rotation=rot, rotation_mode="anchor",
                ha="center", va="center", zorder=8,
                path_effects=[patheffects.withStroke(linewidth=3.0,
                                                     foreground=C("halo"))],
            )


def route_points(by_pid):
    out = []
    for key, name, pid, fallback in rad.ROUTE_CANDIDATES:
        if pid is not None:
            ft = by_pid.get(pid)
            if ft is None:
                print(f"route candidate {key} skipped, pid not in data: {pid!r}")
                continue
            lon, lat = ft["geometry"]["coordinates"][:2]
        else:
            lon, lat = fallback
        out.append((key, name, lon, lat))
    return out


# ---------------------------------------------------------------------------
# Plate furniture: the ruled border an engraved plate carries.
# ---------------------------------------------------------------------------
def double_rule(fig_or_ax, rect, *, outer=1.6, inner=0.7, gap=0.006,
                color=None, fill=None, alpha=1.0, zorder=20, is_fig=True):
    """rect = (x, y, w, h) in figure (or axes) fraction."""
    color = color or C("rule")
    x, y, w, h = rect
    add = fig_or_ax.add_artist if is_fig else fig_or_ax.add_patch
    if fill is not None:
        add(Rectangle((x, y), w, h, facecolor=fill, edgecolor="none",
                      alpha=alpha, zorder=zorder,
                      transform=fig_or_ax.transFigure if is_fig else None))
    for lw, g in ((outer, 0.0), (inner, gap)):
        add(Rectangle((x + g, y + g), w - 2 * g, h - 2 * g, facecolor="none",
                      edgecolor=color, lw=lw, zorder=zorder + 1,
                      transform=fig_or_ax.transFigure if is_fig else None))


def text_block(fig, x, y, text, size, color, setting, lead, style=None,
               weight=None):
    """Draw a wrapped block one line at a time so the caller's leading, not
    matplotlib's font-derived line spacing, governs the layout."""
    for i, line in enumerate(text.split("\n")):
        fig.text(x, y - i * lead, line, ha="left", va="top",
                 fontproperties=fp(setting, "text", size, weight=weight,
                                   style=style),
                 color=color, zorder=30)
    return y - lead * len(text.split("\n"))


def rule_at(fig, x0, x1, y, color, lw):
    fig.add_artist(Line2D([x0, x1], [y, y], color=color, lw=lw,
                          transform=fig.transFigure, zorder=30))


def marker_chip(fig, x, y, letter, size=8.5, setting=PRIMARY_SETTING):
    """The reading-layer provenance chip from conventions section 8."""
    fig.text(x, y, letter, ha="center", va="center",
             fontproperties=fp(setting, "text", size, weight="bold"),
             color=C("panel"), zorder=31,
             bbox=dict(boxstyle="square,pad=0.32", facecolor=C("ink"),
                       edgecolor="none"))


# ---------------------------------------------------------------------------
# Option 1: title card
# ---------------------------------------------------------------------------
TITLE = "The March"
SUBTITLE = "Hannibal and the war that nearly ended Rome"
# Attested, claims ledger TC-16: Polybius 3.56, with Livy 21.38 concurring.
TITLE_STANDFIRST = "Five months from New Carthage. Fifteen days over the Alps."
TITLE_ANCHOR = "Polybius 3.56; Livy 21.38 concurs"

# Full-bleed crop of the committed corridor-full bbox, trimmed in latitude
# only so the plate fills a 4:3 frame without distorting the geometry.
TITLE_BBOX = (4.0, 43.5, 8.0, 45.645)


def title_card(data, out_path, setting=PRIMARY_SETTING, figsize=(16, 12),
               chrome=True):
    fig = plt.figure(figsize=figsize, dpi=DPI)
    fig.patch.set_facecolor(C("ground"))
    ax = fig.add_axes([0, 0, 1, 1])
    basemap(ax, TITLE_BBOX, data, roads=True, mottle=True)
    _, _, _, _, by_pid = classify_places(data)
    setts, others, uncertain, _, _ = classify_places(data)
    if others:
        xs, ys = zip(*others)
        ax.scatter(xs, ys, s=rad.S_OTHER, c=C("dot_small"), alpha=0.5, lw=0, zorder=5)
    if setts:
        xs, ys = zip(*setts)
        ax.scatter(xs, ys, s=rad.S_SETTLEMENT, c=C("dot"), edgecolors=C("halo"),
                   lw=0.4, zorder=6)
    draw_labels(ax, by_pid, setting, size=9.5, rivers=True, bbox=TITLE_BBOX,
                inset=0.10)

    if chrome:
        double_rule(fig, (0.018, 0.018, 0.964, 0.964), outer=1.8, inner=0.8,
                    gap=0.007, color=C("rule"), zorder=20)

    # Cartouche, lower left, over the quiet ground west of the Rhone.
    cx, cy, cw, ch = 0.055, 0.075, 0.455, 0.345
    double_rule(fig, (cx, cy, cw, ch), outer=1.7, inner=0.7, gap=0.008,
                color=C("rule"), fill=C("panel"), alpha=0.97, zorder=25)
    tx = cx + 0.035
    s = TYPE_SETTINGS[setting]
    disp = TITLE.upper() if s["display_caps"] else TITLE
    fig.text(tx, cy + ch - 0.075, track(disp, s["display_track"]),
             ha="left", va="center",
             fontproperties=fp(setting, "display", 46), color=C("ink"), zorder=30)
    fig.add_artist(Line2D([tx, cx + cw - 0.035],
                          [cy + ch - 0.135, cy + ch - 0.135],
                          color=C("rule"), lw=1.2, transform=fig.transFigure,
                          zorder=30))
    fig.text(tx, cy + ch - 0.185, SUBTITLE, ha="left", va="center",
             fontproperties=fp(setting, "text", 17), color=C("ink"), zorder=30)
    marker_chip(fig, tx + 0.011, cy + 0.098, "A", setting=setting)
    fig.text(tx + 0.031, cy + 0.098, TITLE_STANDFIRST, ha="left", va="center",
             fontproperties=fp(setting, "text", 12.5, style="italic"),
             color=C("ink_soft"), zorder=30)
    fig.text(tx + 0.031, cy + 0.062, TITLE_ANCHOR, ha="left", va="center",
             fontproperties=fp(setting, "text", 9.5), color=C("ink_faint"),
             zorder=30)

    if chrome:
        # Foot band, so the credit and the option note stay legible over
        # terrain instead of dissolving into it.
        fig.add_artist(Rectangle((0.025, 0.025), 0.950, 0.038,
                                 facecolor=C("panel"), edgecolor="none",
                                 alpha=0.94, zorder=26,
                                 transform=fig.transFigure))
        fig.add_artist(Line2D([0.025, 0.975], [0.063, 0.063], color=C("rule"),
                              lw=0.8, transform=fig.transFigure, zorder=27))
        fig.text(0.040, 0.0435, rad.TITLE_ATTRIBUTION, ha="left", va="center",
                 fontproperties=fp(setting, "text", 8.5), color=C("ink_soft"),
                 zorder=30)
        fig.text(0.960, 0.0435,
                 "Option 1 of 3 · identity option, not a decision",
                 ha="right", va="center",
                 fontproperties=fp(setting, "text", 8.5), color=C("ink_soft"),
                 zorder=30)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, facecolor=C("ground"), dpi=DPI)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)} [title card, {setting}]")


def title_card_variants(data, out_path):
    """The same card in all three type settings, for the typography call."""
    tmp = []
    for key in TYPE_SETTINGS:
        p = os.path.join(OUT_DIR, "1-title-card", f".variant-{key}.png")
        title_card(data, p, setting=key, figsize=(16, 12), chrome=False)
        tmp.append((key, p))

    from PIL import Image

    fig, axes = plt.subplots(1, 3, figsize=(22, 7.4), dpi=DPI)
    fig.patch.set_facecolor(C("ground"))
    for ax, (key, path) in zip(axes, tmp):
        s = TYPE_SETTINGS[key]
        ax.imshow(np.asarray(Image.open(path)))
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor(C("rule_light"))
        ax.set_title(s["label"], fontproperties=fp(key, "text", 14),
                     color=C("ink"), pad=8)
        ax.set_xlabel(_wrap(s["note"], 48), fontproperties=fp(key, "text", 9.5),
                      color=C("ink_soft"), labelpad=8)
    fig.suptitle(
        "Title card, three type settings. Colour identical in all three, "
        "every value from the declared palette.",
        fontproperties=fp(PRIMARY_SETTING, "text", 15), color=C("ink"), y=0.965,
    )
    fig.tight_layout(rect=(0.004, 0.022, 0.996, 0.935))
    fig.savefig(out_path, facecolor=C("ground"), dpi=DPI)
    plt.close(fig)
    for _, p in tmp:
        os.remove(p)
    print(f"wrote {os.path.relpath(out_path)} [title card typography]")


# ---------------------------------------------------------------------------
# Option 2: chapter frontispiece, The Crossing
# ---------------------------------------------------------------------------
FRONT_BBOX = rad.VIEWS[1][2]  # the committed Alps detail view
CHAPTER_NUM = "Chapter One"
CHAPTER_TITLE = "The Crossing"
# Attested, claims ledger TC-12: Polybius 3.53, Livy 21.35 confirmed verbatim.
FRONT_STANDFIRST = ("On the ninth day they reached the head of the pass, "
                    "and encamped there two days.")
FRONT_ANCHOR = "Polybius 3.53; Livy 21.35"
# The open gap, claims ledger G-1. Stated as a gap, not resolved.
FRONT_GAP = ("Which pass, no ancient source says. Polybius names none; Livy "
             "21.38 rules out the Poenine Pass and the heights of Cremo; "
             "Nepos 3.4 says only the Graian pass.")


def bbox_aspect(bbox):
    """Height / width of the bbox in metres, so a plate frame can hug its map."""
    mean_lat = (bbox[1] + bbox[3]) / 2
    h = (bbox[3] - bbox[1]) * 110_574.0
    w = (bbox[2] - bbox[0]) * 111_320.0 * np.cos(np.radians(mean_lat))
    return h / w


def frontispiece(data, out_path, setting=PRIMARY_SETTING):
    figw, figh = 11.0, 14.6
    fig = plt.figure(figsize=(figw, figh), dpi=DPI)
    fig.patch.set_facecolor(C("ground"))
    double_rule(fig, (0.045, 0.032, 0.910, 0.936), outer=1.7, inner=0.7,
                gap=0.005, color=C("rule"), zorder=20)

    # Plate: ruled frame sized from the view's own aspect so the frame hugs
    # the map instead of leaving a slab of parchment on either side. The plate
    # height is set first, from the space the type block below needs.
    py, ph = 0.290, 0.615
    pw = ph / ((figw / figh) * bbox_aspect(FRONT_BBOX))
    px = (1.0 - pw) / 2
    double_rule(fig, (px - 0.016, py - 0.016, pw + 0.032, ph + 0.032),
                outer=1.4, inner=0.6, gap=0.005, color=C("rule"), zorder=20)
    ax = fig.add_axes([px, py, pw, ph])
    basemap(ax, FRONT_BBOX, data, roads=True, mottle=True)
    by_pid = draw_places(ax, data, with_candidates=True, with_routes=True,
                         setting=setting, key_size=9.5)
    draw_labels(ax, by_pid, setting, size=10, rivers=True, bbox=FRONT_BBOX,
                inset=0.06)

    fig.text(0.5, 0.945, track("The March", 0.30), ha="center", va="center",
             fontproperties=fp(setting, "text", 11), color=C("ink_soft"),
             zorder=30)

    fig.text(px, 0.245, CHAPTER_NUM, ha="left", va="center",
             fontproperties=fp(setting, "text", 13, style="italic"),
             color=C("ink_soft"), zorder=30)
    s = TYPE_SETTINGS[setting]
    disp = CHAPTER_TITLE.upper() if s["display_caps"] else CHAPTER_TITLE
    fig.text(px, 0.199, track(disp, s["display_track"]), ha="left", va="center",
             fontproperties=fp(setting, "display", 32), color=C("ink"), zorder=30)
    fig.add_artist(Line2D([px, px + pw], [0.167, 0.167], color=C("rule"),
                          lw=1.2, transform=fig.transFigure, zorder=30))

    marker_chip(fig, px + 0.011, 0.139, "A", setting=setting)
    fig.text(px + 0.034, 0.139, FRONT_STANDFIRST, ha="left", va="center",
             fontproperties=fp(setting, "text", 13.5, style="italic"),
             color=C("ink"), zorder=30)
    fig.text(px + 0.034, 0.114, FRONT_ANCHOR, ha="left", va="center",
             fontproperties=fp(setting, "text", 9.5), color=C("ink_faint"),
             zorder=30)

    # The gap gets its own visually distinct treatment: hollow chip, not a
    # provenance marker, because an open question is not a claim.
    fig.text(px + 0.011, 0.088, "?", ha="center", va="center",
             fontproperties=fp(setting, "text", 8.5, weight="bold"),
             color=C("ink"), zorder=31,
             bbox=dict(boxstyle="square,pad=0.32", facecolor="none",
                       edgecolor=C("ink"), lw=1.0))
    text_block(fig, px + 0.034, 0.097, _wrap(FRONT_GAP, 95), 10.5,
               C("ink_soft"), setting, 0.019)

    fig.text(px, 0.048, rad.TITLE_ATTRIBUTION, ha="left", va="center",
             fontproperties=fp(setting, "text", 7.5), color=C("ink_faint"),
             zorder=30)
    fig.text(px + pw, 0.048, "Option 2 of 3 · identity option, not a decision",
             ha="right", va="center",
             fontproperties=fp(setting, "text", 7.5), color=C("ink_faint"),
             zorder=30)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, facecolor=C("ground"), dpi=DPI)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)} [frontispiece, {setting}]")


# ---------------------------------------------------------------------------
# Option 3: the route debate. Geometry first, then the plate.
# ---------------------------------------------------------------------------
ROUTE_BBOX = (5.3, 44.0, 8.0, 45.95)
COARSEN = 3          # render-grid cells combined per pathfinding cell
GATE_LON = 5.60      # declared western drawing gate: no place claim attaches

# Per candidate: which trunk river carries the western approach, an optional
# declared constraint on where the approach may leave that trunk, and which
# AWMC river feature carries the eastern descent. The constraints are stated,
# not tuned by eye: each names the corridor the published reconstructions use.
ROUTE_CORRIDORS = {
    "R1": {
        "west": ("Druentia", None,
                 "leaves the Durance at the Guil"),
        "east": ("393469", "descends to the Padus"),
    },
    "R2": {
        "west": ("Isara", 6.20,
                 "leaves the Isere below the Arc; the Maurienne is the "
                 "corridor the Clapier reconstructions use, and the Arc "
                 "itself is not in the committed AWMC river set"),
        "east": ("383636", "descends to the Duria Minor"),
    },
    "R3": {
        "west": ("Druentia", None,
                 "the Durance reaches the pass"),
        "east": ("383636", "descends to the Duria Minor"),
    },
    "R4": {
        "west": ("Isara", None,
                 "leaves the Isere in the Tarentaise"),
        "east": ("383635", "descends to the Duria Maior"),
    },
    "R5": {
        "west": None,
        "east": ("383635", "descends to the Duria Maior"),
    },
    "R6": {
        "west": ("Druentia", 6.55,
                 "leaves the Durance below the Ubaye"),
        "east": ("383786", "descends toward the Padus plain"),
    },
    "R7": {
        "west": ("Isara", 6.20,
                 "leaves the Isere below the Arc, as R2"),
        "east": ("383636", "descends to the Duria Minor"),
    },
}

# R5 has no western approach inside the committed corridor: the Valais Rhone
# lies north of the DEM's own northern edge. Shown as a gap, not filled in.
R5_GAP = ("R5 is drawn on its eastern descent only. Its western approach, "
          "the Valais Rhone, lies outside the committed corridor DEM.")

# Backers and arguments, verbatim in substance from
# data/content/02/route-candidates.md.
ROUTE_KEY = [
    ("R1", "Col de la Traversette",
     "Mahaney; MacDonald; Ball", None,
     "Peat-bog cores at c.3000 m: biomarkers, horse tapeworm eggs and "
     "clostridia DNA dated c.218 BC."),
    ("R2", "Col de Clapier",
     "Connolly; Lazenby; Lancel; Kuhle and Kuhle; Hoyte 1960", None,
     "The northern line, matching Polybius's march up the river past the "
     "Island, 800 stadia."),
    ("R3", "Col de Montgenevre",
     "Lancel, followed by Miles", None,
     "A known easy trade pass, and the one route matching Livy's itinerary "
     "up the Durance."),
    ("R4", "Little St Bernard (Alpis Graia)",
     "Mommsen; Capes; Coelius Antipater (ancient)", None,
     "Literal reading of the along-the-river march to Vienne, then Mont du "
     "Chat and the Salassi."),
    ("R5", "Great St Bernard (Alpis Poenina)",
     "no modern backer in the fact base", "refuted in antiquity",
     "Ancient etymology only. Livy 21.38 refutes it: the Poeninus deity, "
     "hostile tribes, arrival among the Libui."),
    ("R6", "Col de la Larche",
     "Lancel", None,
     "A southern alternative bypassing Scipio's coastal scouts, on Livy's "
     "Durance corridor."),
    ("R7", "Mont Cenis / Petit Mont-Cenis",
     "none recorded", "no backer recorded",
     "Named in the fact base as a classic candidate, with no distinct "
     "argument recorded. Displayed as such."),
]
REFUTED = {"R5"}

ROUTE_TITLE = "Which pass?"
ROUTE_SUB = "Seven candidate crossings, none of them attested"
ROUTE_GAP_LINE = (
    "No ancient source names the pass. Polybius names none; Livy 21.38 rules "
    "out the Poenine Pass and Caelius Antipater's heights of Cremo; Nepos 3.4 "
    "says only the Graian pass. The identification is modern, and open."
)
ROUTE_GAP_ANCHOR = "claims ledger TC-19 and gap G-1; candidates per route-candidates.md"


class CostGrid:
    """Least-cost traverse over the corridor DEM, coarsened for pathfinding.

    Cost is Tobler's hiking function, so the traverse follows valleys the way
    a walking corridor does. This is a computed inference over modern SRTM
    terrain on the visualization render grid, never an attested itinerary, and
    it is drawn dashed so the plate distinguishes it from committed geometry.
    """

    def __init__(self, dem, bbox, factor):
        elev = dem["elev"].astype(np.float64)
        west, north, cell = (float(dem["west"]), float(dem["north"]),
                             float(dem["cell_deg"]))
        c0 = int(round((bbox[0] - west) / cell))
        c1 = int(round((bbox[2] - west) / cell))
        r0 = int(round((north - bbox[3]) / cell))
        r1 = int(round((north - bbox[1]) / cell))
        sub = elev[r0:r1, c0:c1]
        nr = sub.shape[0] // factor * factor
        nc = sub.shape[1] // factor * factor
        self.z = sub[:nr, :nc].reshape(
            nr // factor, factor, nc // factor, factor).mean(axis=(1, 3))
        self.cell = cell * factor
        self.w0 = west + c0 * cell
        self.n0 = north - r0 * cell
        self.h, self.w = self.z.shape
        mean_lat = (bbox[1] + bbox[3]) / 2
        dy = self.cell * 110_574.0
        dx = self.cell * 111_320.0 * np.cos(np.radians(mean_lat))
        self.nb = [(di, dj, float(np.hypot(di * dy, dj * dx)))
                   for di in (-1, 0, 1) for dj in (-1, 0, 1)
                   if (di, dj) != (0, 0)]

    def ij(self, lon, lat):
        j = int(round((lon - self.w0) / self.cell))
        i = int(round((self.n0 - lat) / self.cell))
        return min(max(i, 0), self.h - 1), min(max(j, 0), self.w - 1)

    def field(self, lon, lat):
        z = self.z
        dist = np.full((self.h, self.w), np.inf)
        prev = np.full((self.h, self.w, 2), -1, dtype=np.int32)
        si, sj = self.ij(lon, lat)
        dist[si, sj] = 0.0
        pq = [(0.0, si, sj)]
        while pq:
            dcur, i, j = heapq.heappop(pq)
            if dcur > dist[i, j]:
                continue
            zc = z[i, j]
            for di, dj, dd in self.nb:
                ni, nj = i + di, j + dj
                if ni < 0 or nj < 0 or ni >= self.h or nj >= self.w:
                    continue
                slope = (z[ni, nj] - zc) / dd
                speed = 6.0 * np.exp(-3.5 * abs(slope + 0.05))
                nd = dcur + (dd / 1000.0) / max(speed, 1e-3)
                if nd < dist[ni, nj]:
                    dist[ni, nj] = nd
                    prev[ni, nj, 0] = i
                    prev[ni, nj, 1] = j
                    heapq.heappush(pq, (nd, ni, nj))
        return dist, prev

    def trace(self, prev, lon, lat):
        """Grid path from (lon, lat) back to the field's source point."""
        i, j = self.ij(lon, lat)
        pts = []
        while i >= 0:
            pts.append((self.w0 + j * self.cell, self.n0 - i * self.cell))
            pi, pj = prev[i, j]
            if pi < 0:
                break
            i, j = int(pi), int(pj)
        return pts


def smooth_path(pts, k=7):
    if len(pts) < k:
        return pts
    a = np.array(pts, dtype=float)
    ker = np.ones(k) / k
    xs = np.convolve(a[:, 0], ker, mode="valid")
    ys = np.convolve(a[:, 1], ker, mode="valid")
    return [tuple(a[0])] + list(zip(xs, ys)) + [tuple(a[-1])]


def in_bbox(p, bbox):
    return bbox[0] <= p[0] <= bbox[2] and bbox[1] <= p[1] <= bbox[3]


def longest_part(feature):
    return [tuple(q[:2]) for q in max(rad.line_parts(feature["geometry"]), key=len)]


def named_trunk(data, name):
    for ft in data["rivers"]["features"]:
        if ft["properties"].get("name_ancient") == name:
            return longest_part(ft)
    raise KeyError(name)


def descent_part(data, pid, near):
    """The part of AWMC river feature `pid` closest to the pass."""
    best = None
    for ft in data["river_network"]["features"]:
        if ft["properties"].get("pid") != pid:
            continue
        for part in rad.line_parts(ft["geometry"]):
            pts = [tuple(q[:2]) for q in part]
            inb = [p for p in pts if in_bbox(p, ROUTE_BBOX)]
            if not inb:
                continue
            dmin = min((p[0] - near[0]) ** 2 + (p[1] - near[1]) ** 2 for p in inb)
            if best is None or dmin < best[0]:
                best = (dmin, pts)
    if best is None:
        raise KeyError(pid)
    return best[1]


def build_routes(data):
    """Return {key: {"river": [...], "traverse": [...], "pass": (lon, lat)}}."""
    grid = CostGrid(data["dem"], ROUTE_BBOX, COARSEN)
    _, _, _, _, by_pid = classify_places(data)
    passes = {k: (lon, lat) for k, _, lon, lat in route_points(by_pid)}
    trunks = {"Druentia": named_trunk(data, "Druentia"),
              "Isara": named_trunk(data, "Isara")}
    out = {}
    for key, spec in ROUTE_CORRIDORS.items():
        lon, lat = passes[key]
        dist, prev = grid.field(lon, lat)
        river, traverse = [], []

        if spec["west"]:
            tname, max_lon, _ = spec["west"]
            poly = trunks[tname]
            inb = [(k, p) for k, p in enumerate(poly) if in_bbox(p, ROUTE_BBOX)]
            gate_k = min(inb, key=lambda kp: abs(kp[1][0] - GATE_LON))[0]
            allowed = [(k, p) for k, p in inb
                       if max_lon is None or p[0] <= max_lon]
            branch_k, branch_p = min(
                allowed, key=lambda kp: dist[grid.ij(*kp[1])])
            lo, hi = sorted((gate_k, branch_k))
            leg = poly[lo:hi + 1]
            if branch_k < gate_k:
                leg = list(reversed(leg))
            river.append(leg)
            traverse.append(grid.trace(prev, *branch_p))  # branch -> pass

        epid, _ = spec["east"]
        part = descent_part(data, epid, (lon, lat))
        inb = [(k, p) for k, p in enumerate(part) if in_bbox(p, ROUTE_BBOX)]
        join_k, join_p = min(inb, key=lambda kp: dist[grid.ij(*kp[1])])
        traverse.append(list(reversed(grid.trace(prev, *join_p))))  # pass -> join
        end_k = max(inb, key=lambda kp: kp[1][0])[0]
        lo, hi = sorted((join_k, end_k))
        leg = part[lo:hi + 1]
        if end_k < join_k:
            leg = list(reversed(leg))
        river.append(leg)

        out[key] = {"river": river, "traverse": traverse, "pass": (lon, lat)}
        print(f"  {key}: river legs {[len(l) for l in river]}, "
              f"computed traverse {[len(t) for t in traverse]}")
    return out


def route_debate(data, out_path, setting=PRIMARY_SETTING):
    print("building route corridors")
    routes = build_routes(data)

    fig = plt.figure(figsize=(19, 13.2), dpi=DPI)
    fig.patch.set_facecolor(C("ground"))
    double_rule(fig, (0.014, 0.016, 0.972, 0.968), outer=1.8, inner=0.8,
                gap=0.005, color=C("rule"), zorder=20)

    figw, figh = 19.0, 13.2
    mx, mw = 0.038, 0.560
    mh = mw * (figw / figh) * bbox_aspect(ROUTE_BBOX)
    my = 0.936 - mh
    double_rule(fig, (mx - 0.010, my - 0.012, mw + 0.020, mh + 0.024),
                outer=1.4, inner=0.6, gap=0.004, color=C("rule"), zorder=20)
    ax = fig.add_axes([mx, my, mw, mh])
    basemap(ax, ROUTE_BBOX, data, roads=True, mottle=True, river_lw=0.85)

    _, _, _, _, by_pid = classify_places(data)
    setts, others, uncertain, _, _ = classify_places(data)
    if others:
        xs, ys = zip(*others)
        ax.scatter(xs, ys, s=rad.S_OTHER, c=C("dot_small"), alpha=0.45, lw=0,
                   zorder=5)
    if setts:
        xs, ys = zip(*setts)
        ax.scatter(xs, ys, s=rad.S_SETTLEMENT, c=C("dot"), edgecolors=C("halo"),
                   lw=0.4, zorder=6)

    for idx, (key, _, _, _, _) in enumerate(ROUTE_KEY):
        r = routes[key]
        color = C("refuted") if key in REFUTED else C("route")
        lw = 2.4 if key not in REFUTED else 1.9
        casing = patheffects.withStroke(linewidth=lw + 2.6, foreground=C("halo"))
        for leg in r["river"]:
            if len(leg) < 2:
                continue
            xs, ys = zip(*leg)
            ax.plot(xs, ys, color=color, lw=lw, zorder=6.5,
                    solid_capstyle="round", path_effects=[casing])
        longest = None
        for leg in r["traverse"]:
            if len(leg) < 2:
                continue
            sm = smooth_path(leg)
            xs, ys = zip(*sm)
            ax.plot(xs, ys, color=color, lw=lw, ls=(0, (5.5, 3.0)), zorder=6.6,
                    solid_capstyle="round", path_effects=[casing])
            if longest is None or len(sm) > len(longest):
                longest = sm
        # A second key on the branch itself, so a reader can tell which
        # corridor is which where several share a trunk.
        if longest is not None and len(longest) > 40:
            # Staggered along the branch so candidates sharing a corridor
            # (R2 with R7, R1 with R6) do not stack their keys.
            frac = 0.38 + 0.07 * (idx % 3)
            bx, by = longest[int(len(longest) * frac)]
            ax.annotate(key, (bx, by), xytext=(bx, by + 0.035), ha="center",
                        va="bottom",
                        fontproperties=fp(setting, "text", 9.5, weight="bold"),
                        color=color, zorder=8,
                        path_effects=[patheffects.withStroke(
                            linewidth=3.0, foreground=C("halo"))])
        lon, lat = r["pass"]
        ax.scatter([lon], [lat], s=rad.S_ROUTE + 26, marker="D",
                   facecolors=C("halo"), edgecolors=color, lw=1.8, zorder=7)
        dx, dy = rad.ROUTE_LABEL_OFFSETS.get(key, (0.03, 0.025))
        keyed(ax, key, lon, lat, dx * 1.5, dy * 1.5, color, setting, 12)

    draw_labels(ax, by_pid, setting, size=8.5, rivers=True, bbox=ROUTE_BBOX,
                inset=0.09)

    # The two trunks the debate splits on, named on the plate. Position and
    # rotation both come from the AWMC polyline itself.
    for name, label, at_lon in (
        ("Druentia", "Druentia (Durance)", 6.25),
        ("Isara", "Isara (Isère)", 5.95),
    ):
        poly = named_trunk(data, name)
        inb = [p for p in poly if in_bbox(p, ROUTE_BBOX)]
        k = min(range(len(inb)), key=lambda i: abs(inb[i][0] - at_lon))
        a, b = inb[max(0, k - 6)], inb[min(len(inb) - 1, k + 6)]
        rot = np.degrees(np.arctan2(
            (b[1] - a[1]) * 110_574.0,
            (b[0] - a[0]) * 111_320.0 * np.cos(np.radians(inb[k][1]))))
        # The polylines run head to mouth, so half of them point west and the
        # label would set upside down. Keep every label reading left to right.
        rot = (rot + 90) % 180 - 90
        ax.annotate(label, inb[k],
                    fontproperties=fp(setting, "text", 9.5, style="italic"),
                    color=C("river"), rotation=rot, rotation_mode="anchor",
                    ha="center", va="bottom", zorder=8,
                    path_effects=[patheffects.withStroke(
                        linewidth=3.0, foreground=C("halo"))])

    # ---- right-hand key panel -------------------------------------------
    kx, ky, kw, kh = 0.630, 0.052, 0.340, 0.896
    double_rule(fig, (kx, ky, kw, kh), outer=1.6, inner=0.7, gap=0.005,
                color=C("rule"), fill=C("panel"), alpha=1.0, zorder=25)
    ix = kx + 0.024
    ex = kx + kw - 0.024
    s = TYPE_SETTINGS[setting]
    top = ky + kh - 0.048
    fig.text(ix, top, track(ROUTE_TITLE.upper() if s["display_caps"]
                            else ROUTE_TITLE, s["display_track"]),
             ha="left", va="center",
             fontproperties=fp(setting, "display", 26), color=C("ink"), zorder=30)
    fig.text(ix, top - 0.033, ROUTE_SUB, ha="left", va="center",
             fontproperties=fp(setting, "text", 12.5, style="italic"),
             color=C("ink_soft"), zorder=30)
    rule_at(fig, ix, ex, top - 0.052, C("rule"), 1.1)

    # Two-pass layout: count the wrapped lines first, then solve for the
    # leading that makes the key fill the panel exactly. A key that runs off
    # the plate is a defect, so the layout is derived rather than guessed.
    entries = []
    for key, name, backers, tag, argument in ROUTE_KEY:
        blines = _wrap("Backers: " + backers, 62)
        alines = _wrap(argument, 64)
        entries.append((key, name, blines, tag, alines))
    gap_lines = _wrap(ROUTE_GAP_LINE, 60)
    r5_lines = _wrap(R5_GAP, 62)
    anchor_lines = _wrap(ROUTE_GAP_ANCHOR, 66)

    def nlines(t):
        return len(t.split("\n"))

    NAME_H, ENTRY_PAD, RULE_PAD = 0.019, 0.009, 0.008
    LEGEND_H = 0.014 + 3 * 0.0175
    GAP_PAD = 0.008 + 0.008 + 0.006
    total_lines = sum(nlines(b) + (1 if t else 0) + nlines(a)
                      for _, _, b, t, a in entries)
    total_lines += nlines(gap_lines) + nlines(r5_lines) + nlines(anchor_lines)
    fixed = len(entries) * (NAME_H + ENTRY_PAD + RULE_PAD) + LEGEND_H + GAP_PAD
    start = top - 0.070
    floor = ky + 0.026
    LEAD = min(0.0158, max(0.0108, (start - floor - fixed) / total_lines))
    print(f"  key panel: {total_lines} wrapped lines, leading {LEAD:.4f}")

    row = start
    for key, name, blines, tag, alines in entries:
        color = C("refuted") if key in REFUTED else C("route")
        fig.text(ix, row, key, ha="left", va="top",
                 fontproperties=fp(setting, "text", 11.5, weight="bold"),
                 color=color, zorder=30)
        fig.text(ix + 0.028, row, name, ha="left", va="top",
                 fontproperties=fp(setting, "text", 11.5), color=C("ink"),
                 zorder=30)
        row -= NAME_H
        row = text_block(fig, ix + 0.028, row, blines, 9.4, C("ink_soft"),
                         setting, LEAD)
        if tag:
            fig.text(ix + 0.028, row, tag, ha="left", va="top",
                     fontproperties=fp(setting, "text", 9.4, style="italic"),
                     color=C("ring_candidate"), zorder=30)
            row -= LEAD
        row = text_block(fig, ix + 0.028, row, alines, 9.4, C("ink_faint"),
                         setting, LEAD)
        row -= ENTRY_PAD
        rule_at(fig, ix, ex, row + 0.004, C("rule_light"), 0.6)
        row -= RULE_PAD

    # ---- how the lines are made, and what they do not claim --------------
    rule_at(fig, ix, ex, row + 0.008, C("rule"), 1.1)
    row -= 0.014
    for color, dashed, text in (
        (C("route"), False, "AWMC river geometry, drawn as committed data"),
        (C("route"), True, "least-cost traverse computed over the render DEM"),
        (C("refuted"), False, "candidate refuted in antiquity (R5, Livy 21.38)"),
    ):
        fig.add_artist(Line2D([ix, ix + 0.026], [row, row], color=color, lw=2.2,
                              ls=(0, (4.5, 2.5)) if dashed else "-",
                              transform=fig.transFigure, zorder=30))
        fig.text(ix + 0.034, row, text, ha="left", va="center",
                 fontproperties=fp(setting, "text", 9.2), color=C("ink_soft"),
                 zorder=30)
        row -= 0.0175

    row -= 0.008
    fig.text(ix + 0.007, row - 0.005, "I", ha="center", va="top",
             fontproperties=fp(setting, "text", 8.5, weight="bold"),
             color=C("panel"), zorder=31,
             bbox=dict(boxstyle="square,pad=0.32", facecolor=C("ink"),
                       edgecolor="none"))
    row = text_block(fig, ix + 0.028, row, gap_lines, 9.8, C("ink"), setting,
                     LEAD) - 0.008
    row = text_block(fig, ix + 0.028, row, r5_lines, 9.0, C("ink_soft"),
                     setting, LEAD) - 0.006
    row = text_block(fig, ix + 0.028, row, anchor_lines, 8.4, C("ink_faint"),
                     setting, LEAD)
    if row < ky + 0.004:
        print(f"  WARNING: key panel content runs below the panel "
              f"(row={row:.3f}, panel floor={ky + 0.004:.3f})")

    fig.text(mx, 0.030, rad.TITLE_ATTRIBUTION, ha="left", va="center",
             fontproperties=fp(setting, "text", 8), color=C("ink_faint"),
             zorder=30)
    fig.text(kx + kw, 0.030, "Option 3 of 3 · identity option, not a decision",
             ha="right", va="center",
             fontproperties=fp(setting, "text", 8), color=C("ink_faint"),
             zorder=30)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    fig.savefig(out_path, facecolor=C("ground"), dpi=DPI)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)} [route debate, {setting}]")


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Contact sheet
# ---------------------------------------------------------------------------
SHEET = [
    ("1-title-card/title-card.png", "Option 1 · title card"),
    ("2-frontispiece-the-crossing/frontispiece-the-crossing.png",
     "Option 2 · chapter frontispiece, The Crossing"),
    ("3-route-debate/route-debate.png", "Option 3 · the route debate"),
]


def contact_sheet(out_path, setting=PRIMARY_SETTING):
    """Three plates at a common height, so a portrait page does not swamp two
    landscape ones. The canvas is sized from the images rather than guessed."""
    from PIL import Image

    imgs = [(Image.open(os.path.join(OUT_DIR, rel)), label)
            for rel, label in SHEET]
    PANEL_H, GAP, SIDE, TOP, BOT = 8.0, 0.55, 0.6, 1.05, 0.75
    widths = [PANEL_H * im.width / im.height for im, _ in imgs]
    figw = sum(widths) + GAP * (len(imgs) - 1) + 2 * SIDE
    figh = PANEL_H + TOP + BOT

    fig = plt.figure(figsize=(figw, figh), dpi=DPI)
    fig.patch.set_facecolor(C("ground"))
    x = SIDE
    for (im, label), w in zip(imgs, widths):
        ax = fig.add_axes([x / figw, BOT / figh, w / figw, PANEL_H / figh])
        ax.imshow(np.asarray(im))
        ax.set_xticks([])
        ax.set_yticks([])
        for s in ax.spines.values():
            s.set_edgecolor(C("rule_light"))
        fig.text((x + w / 2) / figw, (BOT + PANEL_H + 0.16) / figh, label,
                 ha="center", va="bottom",
                 fontproperties=fp(setting, "text", 13), color=C("ink"))
        x += w + GAP
    fig.text(0.5, 1 - 0.30 / figh,
             "The March · identity options in the ancient-map (A) register. "
             "Three options to react to, none of them final.",
             ha="center", va="top",
             fontproperties=fp(setting, "text", 16), color=C("ink"))
    fig.text(0.5, 0.30 / figh,
             "Rendered from the committed processed data through the "
             "Direction A style dict. Every colour traces to the declared "
             "palette; typography is the layer under exploration.",
             ha="center", va="center",
             fontproperties=fp(setting, "text", 10), color=C("ink_soft"))
    fig.savefig(out_path, facecolor=C("ground"), dpi=DPI)
    plt.close(fig)
    print(f"wrote {os.path.relpath(out_path)}")


def main():
    data = rad.load_data()
    title_card(data, os.path.join(OUT_DIR, "1-title-card", "title-card.png"))
    title_card_variants(
        data, os.path.join(OUT_DIR, "1-title-card", "title-card-typography.png"))
    frontispiece(data, os.path.join(OUT_DIR, "2-frontispiece-the-crossing",
                                    "frontispiece-the-crossing.png"))
    route_debate(data, os.path.join(OUT_DIR, "3-route-debate", "route-debate.png"))
    contact_sheet(os.path.join(OUT_DIR, "contact-sheet.png"))


if __name__ == "__main__":
    main()
