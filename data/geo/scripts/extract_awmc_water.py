#!/usr/bin/env python3
"""Extract AWMC water features for the Rhone-to-Alps corridor.

Inputs : data/geo/raw/awmc-rivers/awmc-osm-rivers.{shp,dbf}
           (river linework from the AWMC "Physical Shapefiles Apr 2024" zip;
            the unzipped directories of the AWMC/geodata repo carry no river
            linework, only lake/swamp polygons — see SOURCES.md)
         data/geo/raw/awmc-inland-water-OSM.geojson
           (lake/swamp/dry-lake polygons)
Outputs: data/geo/processed/awmc-rivers-corridor.geojson
         data/geo/processed/awmc-rivers-network-corridor.geojson
         data/geo/processed/awmc-inland-water-corridor.geojson

River selection is keyed by Pleiades ID, never by name string:
  148168 Rhodanus (Rhone), 148069 Druentia (Durance), 167793 Isara (Isere),
plus the five segments the source itself annotates notes="Rhodanus delta"
(Barrington Map 15 delta distributaries; they carry no pid of their own).
Geometries are copied unmodified from the source; no clipping of linework.

Network extension (added 2026-08-17): every remaining river feature whose
bounding box overlaps the corridor bbox goes to the separate network file,
same bbox-overlap rule as the other clipped layers, geometries unmodified.
The primary three-river file is unchanged so the POC render and its script
stay exactly reproducible.

Inland-water features are kept when their bounding box overlaps BBOX,
geometries unmodified, same selection rule as scripts/clip_awmc.py.

Usage: .venv/bin/python data/geo/scripts/extract_awmc_water.py
"""

import json
import os
import struct

BBOX = (4.0, 43.5, 8.0, 46.0)  # min lon, min lat, max lon, max lat

RIVER_PIDS = {
    "148168": ("Rhodanus", "Rhone"),
    "148069": ("Druentia", "Durance"),
    "167793": ("Isara", "Isere"),
}
DELTA_NOTE = "Rhodanus delta"

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW_RIVERS = os.path.join(ROOT, "raw", "awmc-rivers", "awmc-osm-rivers")
RAW_WATER = os.path.join(ROOT, "raw", "awmc-inland-water-OSM.geojson")
OUT_RIVERS = os.path.join(ROOT, "processed", "awmc-rivers-corridor.geojson")
OUT_NETWORK = os.path.join(
    ROOT, "processed", "awmc-rivers-network-corridor.geojson"
)
OUT_WATER = os.path.join(ROOT, "processed", "awmc-inland-water-corridor.geojson")


def read_dbf(path):
    """Minimal dBase III reader: returns list of dicts (None for deleted)."""
    with open(path, "rb") as f:
        data = f.read()
    nrec = struct.unpack("<I", data[4:8])[0]
    hdr_size, rec_size = struct.unpack("<HH", data[8:12])
    fields = []
    off = 32
    while data[off] != 0x0D:
        name = data[off:off + 11].split(b"\x00")[0].decode("ascii", "replace")
        flen = data[off + 16]
        fields.append((name, flen))
        off += 32
    records = []
    for i in range(nrec):
        base = hdr_size + i * rec_size
        rec = data[base:base + rec_size]
        if not rec or rec[0:1] == b"*":
            records.append(None)
            continue
        vals, p = {}, 1
        for name, flen in fields:
            vals[name] = rec[p:p + flen].decode("utf-8", "replace").strip()
            p += flen
        records.append(vals)
    return records


def read_shp_polylines(path):
    """Minimal .shp reader for PolyLine (type 3) records.

    Returns a list parallel to the dbf: each entry is a list of parts,
    each part a list of [lon, lat]; None for non-polyline records.
    """
    out = []
    with open(path, "rb") as f:
        f.seek(0, 2)
        end = f.tell()
        f.seek(100)  # skip main header
        while f.tell() < end:
            hdr = f.read(8)
            if len(hdr) < 8:
                break
            _num, clen = struct.unpack(">ii", hdr)
            content = f.read(clen * 2)
            stype = struct.unpack("<i", content[:4])[0]
            if stype != 3:
                out.append(None)
                continue
            nparts, npoints = struct.unpack("<2i", content[36:44])
            parts = struct.unpack(f"<{nparts}i", content[44:44 + 4 * nparts])
            pts_off = 44 + 4 * nparts
            flat = struct.unpack(
                f"<{2 * npoints}d", content[pts_off:pts_off + 16 * npoints]
            )
            pts = [[flat[2 * i], flat[2 * i + 1]] for i in range(npoints)]
            bounds = list(parts) + [npoints]
            out.append(
                [pts[bounds[i]:bounds[i + 1]] for i in range(nparts)]
            )
    return out


def geom_bbox(geom):
    xs, ys = [], []

    def walk(c):
        if isinstance(c[0], (int, float)):
            xs.append(c[0])
            ys.append(c[1])
        else:
            for cc in c:
                walk(cc)

    walk(geom["coordinates"])
    return min(xs), min(ys), max(xs), max(ys)


def overlaps(bb):
    x0, y0, x1, y1 = bb
    return x1 >= BBOX[0] and x0 <= BBOX[2] and y1 >= BBOX[1] and y0 <= BBOX[3]


def main():
    # --- Rivers ---
    recs = read_dbf(RAW_RIVERS + ".dbf")
    shapes = read_shp_polylines(RAW_RIVERS + ".shp")
    assert len(recs) == len(shapes), "dbf/shp record count mismatch"
    features = []
    network = []
    for rec, shape in zip(recs, shapes):
        if rec is None or shape is None:
            continue
        pid = rec.get("pid", "")
        is_named = pid in RIVER_PIDS
        is_delta = rec.get("notes", "") == DELTA_NOTE
        if not (is_named or is_delta):
            # Network extension: keep every other river feature whose
            # bounding box overlaps the corridor, geometry unmodified.
            xs = [p[0] for part in shape for p in part]
            ys = [p[1] for part in shape for p in part]
            if overlaps((min(xs), min(ys), max(xs), max(ys))):
                network.append(
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "MultiLineString",
                            "coordinates": shape,
                        },
                        "properties": {
                            "pid": pid or None,
                            "origin": rec.get("origin"),
                            "notes": rec.get("notes") or None,
                            "strabo_name": rec.get("Strabo_nam") or None,
                        },
                    }
                )
            continue
        if is_named:
            ancient, modern = RIVER_PIDS[pid]
        else:
            ancient, modern = None, None
        features.append(
            {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString",
                    "coordinates": shape,
                },
                "properties": {
                    "name_ancient": ancient,
                    "name_modern": modern,
                    "pid": pid or None,
                    "origin": rec.get("origin"),
                    "notes": rec.get("notes") or None,
                    "strabo_name": rec.get("Strabo_nam") or None,
                },
            }
        )
    features.sort(key=lambda f: (f["properties"]["pid"] or "zzz", f["properties"]["origin"] or ""))
    named = [f for f in features if f["properties"]["pid"]]
    delta = [f for f in features if not f["properties"]["pid"]]
    assert len(named) == 3, f"expected 3 pid-keyed rivers, got {len(named)}"
    with open(OUT_RIVERS, "w", encoding="utf-8") as f:
        json.dump(
            {"type": "FeatureCollection", "bbox": list(BBOX), "features": features},
            f,
            ensure_ascii=False,
            indent=1,
        )
    print(f"rivers: {len(named)} named (by pid) + {len(delta)} 'Rhodanus delta' segments -> {OUT_RIVERS}")

    network.sort(
        key=lambda f: (
            f["properties"]["pid"] or "zzz",
            f["properties"]["origin"] or "",
            f["properties"]["notes"] or "",
            f["geometry"]["coordinates"][0][0],
        )
    )
    with open(OUT_NETWORK, "w", encoding="utf-8") as f:
        json.dump(
            {"type": "FeatureCollection", "bbox": list(BBOX), "features": network},
            f,
            ensure_ascii=False,
            indent=1,
        )
    n_net_pid = sum(1 for f in network if f["properties"]["pid"])
    print(
        f"river network: {len(network)} additional corridor features "
        f"({n_net_pid} pid-keyed) -> {OUT_NETWORK}"
    )

    # --- Inland water (lakes etc.) ---
    with open(RAW_WATER, encoding="utf-8") as f:
        raw = json.load(f)
    kept = []
    for ft in raw["features"]:
        geom = ft.get("geometry")
        if not geom:
            continue
        if overlaps(geom_bbox(geom)):
            p = ft.get("properties") or {}
            kept.append(
                {
                    "type": "Feature",
                    "geometry": geom,
                    "properties": {
                        "type": p.get("TYPE"),
                        "awmc_id": p.get("AWMC_ID"),
                        "title": (p.get("TITLE") or None)
                        if p.get("TITLE") not in ("", "Untitled")
                        else None,
                    },
                }
            )
    with open(OUT_WATER, "w", encoding="utf-8") as f:
        json.dump(
            {"type": "FeatureCollection", "bbox": list(BBOX), "features": kept},
            f,
            ensure_ascii=False,
            indent=1,
        )
    print(f"inland water: {len(kept)} of {len(raw['features'])} features -> {OUT_WATER}")


if __name__ == "__main__":
    main()
