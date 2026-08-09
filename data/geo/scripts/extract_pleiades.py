#!/usr/bin/env python3
"""Extract Pleiades places inside the Rhone-to-Alps corridor bounding box.

Input : data/geo/raw/pleiades-places-latest.json.gz
        (Pleiades gazetteer daily JSON dump, see data/geo/SOURCES.md)
Output: data/geo/processed/pleiades-places-corridor.geojson

The dump is ~1.9 GB uncompressed, so this streams the top-level "@graph"
array with json.JSONDecoder.raw_decode instead of loading the whole file.

A place is kept when its representative point (reprPoint, [lon, lat]) falls
inside BBOX. Places with no reprPoint are counted and reported but not kept;
they are locations Pleiades itself does not place on the map, and inventing
coordinates for them is out of bounds.

Usage: python3 data/geo/scripts/extract_pleiades.py
"""

import gzip
import json
import os

BBOX = (4.0, 43.5, 8.0, 46.0)  # min lon, min lat, max lon, max lat

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "raw", "pleiades-places-latest.json.gz")
OUT = os.path.join(ROOT, "processed", "pleiades-places-corridor.geojson")

CHUNK = 1 << 20  # 1 MiB of decompressed text per read


def stream_graph_objects(path):
    """Yield each object of the top-level "@graph" array in the dump."""
    decoder = json.JSONDecoder()
    with gzip.open(path, "rt", encoding="utf-8") as f:
        buf = f.read(CHUNK)
        # Find the start of the @graph array.
        while '"@graph"' not in buf:
            more = f.read(CHUNK)
            if not more:
                raise ValueError('"@graph" key not found in dump')
            buf += more
        idx = buf.index('"@graph"')
        idx = buf.index("[", idx) + 1
        buf = buf[idx:]
        while True:
            buf = buf.lstrip(" \t\r\n,")
            if buf.startswith("]"):
                return  # end of array
            try:
                obj, end = decoder.raw_decode(buf)
            except json.JSONDecodeError:
                more = f.read(CHUNK)
                if not more:
                    raise
                buf += more
                continue
            yield obj
            buf = buf[end:]


def in_bbox(pt):
    lon, lat = pt
    return BBOX[0] <= lon <= BBOX[2] and BBOX[1] <= lat <= BBOX[3]


# Worst-first ranking for Pleiades associationCertainty values: a place is
# only as located as its least certain location record.
CERTAINTY_RANK = ["uncertain", "less-certain", "certain"]


def location_certainty(place):
    certs = {
        loc.get("associationCertainty")
        for loc in place.get("locations", [])
        if loc.get("associationCertainty")
    }
    for level in CERTAINTY_RANK:
        if level in certs:
            return level
    return None


def to_feature(place):
    names = [
        {
            "attested": n.get("attested"),
            "romanized": n.get("romanized"),
            "language": n.get("language"),
        }
        for n in place.get("names", [])
    ]
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": place["reprPoint"]},
        "properties": {
            "pid": place.get("id"),
            "uri": place.get("uri"),
            "title": place.get("title"),
            "description": place.get("description"),
            "placeTypes": place.get("placeTypes", []),
            "names": names,
            "locationCertainty": location_certainty(place),
        },
    }


def main():
    kept, total, no_point = 0, 0, 0
    features = []
    for place in stream_graph_objects(RAW):
        total += 1
        pt = place.get("reprPoint")
        if not pt:
            no_point += 1
            continue
        if in_bbox(pt):
            features.append(to_feature(place))
            kept += 1
    features.sort(key=lambda f: f["properties"]["pid"] or "")
    out = {
        "type": "FeatureCollection",
        "bbox": list(BBOX),
        "features": features,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"places in dump: {total}")
    print(f"  without reprPoint (skipped, unplaceable): {no_point}")
    print(f"  inside bbox {BBOX}: {kept}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
