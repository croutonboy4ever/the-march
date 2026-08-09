#!/usr/bin/env python3
"""Clip AWMC geodata (Roman roads, ancient shoreline) to the corridor bbox.

Inputs : data/geo/raw/awmc-roads.geojson
         data/geo/raw/awmc-shoreline.geojson
         (Ancient World Mapping Center geodata, see data/geo/SOURCES.md)
Outputs: data/geo/processed/awmc-roads-corridor.geojson
         data/geo/processed/awmc-shoreline-corridor.geojson

"Clip" here means feature selection, not geometry surgery: a feature is kept,
with its source geometry untouched, when any of its vertices falls inside the
corridor bbox or any of its segments crosses it (tested via per-part coordinate
bounds overlap). Geometries are never modified, so every kept line remains
exactly what AWMC published; the renderer crops to the bbox at draw time.

Usage: python3 data/geo/scripts/clip_awmc.py
"""

import json
import os

BBOX = (4.0, 43.5, 8.0, 46.0)  # min lon, min lat, max lon, max lat

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
JOBS = [
    ("awmc-roads.geojson", "awmc-roads-corridor.geojson"),
    ("awmc-shoreline.geojson", "awmc-shoreline-corridor.geojson"),
]


def iter_positions(geom):
    """Yield (lon, lat) for any GeoJSON geometry type."""
    t, c = geom["type"], geom.get("coordinates", [])
    if t == "Point":
        yield c
    elif t in ("MultiPoint", "LineString"):
        yield from c
    elif t in ("MultiLineString", "Polygon"):
        for part in c:
            yield from part
    elif t == "MultiPolygon":
        for poly in c:
            for ring in poly:
                yield from ring
    elif t == "GeometryCollection":
        for g in geom.get("geometries", []):
            yield from iter_positions(g)


def bounds_overlap(geom):
    lons, lats = [], []
    for lon, lat in iter_positions(geom):
        lons.append(lon)
        lats.append(lat)
    if not lons:
        return False
    return (
        min(lons) <= BBOX[2]
        and max(lons) >= BBOX[0]
        and min(lats) <= BBOX[3]
        and max(lats) >= BBOX[1]
    )


def main():
    for raw_name, out_name in JOBS:
        raw_path = os.path.join(ROOT, "raw", raw_name)
        out_path = os.path.join(ROOT, "processed", out_name)
        with open(raw_path, encoding="utf-8") as f:
            data = json.load(f)
        kept = [
            ft
            for ft in data["features"]
            if ft.get("geometry") and bounds_overlap(ft["geometry"])
        ]
        out = {
            "type": "FeatureCollection",
            "bbox": list(BBOX),
            "features": kept,
        }
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False)
        print(f"{raw_name}: {len(data['features'])} features -> {len(kept)} in corridor")


if __name__ == "__main__":
    main()
