#!/usr/bin/env python3
"""Elevation audit per conventions v1.0 section 4 (amendment, 2026-08-09).

Rendered terrain grids are visualization-only. Any elevation figure displayed
in the experience must come from the full-resolution tiles (or an
authoritative reference), never from the downsampled render grid. This script
reads elevations for named benchmark points straight from the raw 1-arc-second
skadi tiles and prints them next to the downsampled-grid values, so the two
are never confused.

Input : data/geo/raw/dem/N{lat}E{lon:03d}.hgt.gz  (1", 3601x3601, int16 BE)
        data/geo/processed/dem-corridor.npz       (render grid, ~120 m)
Usage : .venv/bin/python data/geo/scripts/audit_elevation.py
"""

import gzip
import os
import struct

import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DEM_RAW = os.path.join(ROOT, "raw", "dem")
DEM_GRID = os.path.join(ROOT, "processed", "dem-corridor.npz")

# Benchmark points: (label, lat, lon, reference elevation m, reference source)
BENCHMARKS = [
    ("Mont Ventoux summit", 44.1741, 5.2786, 1909, "IGN"),
    ("Barre des Ecrins summit", 44.9239, 6.3597, 4102, "IGN"),
    ("Col du Mont Cenis", 45.2595, 6.9054, 2081, "IGN"),
    ("Avignon (valley floor)", 43.9493, 4.8055, 21, "IGN, city datum"),
]


def full_res_elevation(lat, lon):
    """Elevation in metres from the raw 1-arc-second tile containing lat/lon."""
    tlat, tlon = int(np.floor(lat)), int(np.floor(lon))
    path = os.path.join(DEM_RAW, f"N{tlat}E{tlon:03d}.hgt.gz")
    with gzip.open(path, "rb") as f:
        data = f.read()
    n = 3601
    assert len(data) == n * n * 2, f"unexpected tile size for {path}"
    row = round((1 - (lat - tlat)) * (n - 1))
    col = round((lon - tlon) * (n - 1))
    (val,) = struct.unpack(">h", data[2 * (row * n + col):2 * (row * n + col) + 2])
    return val


def grid_elevation(lat, lon):
    """Elevation from the downsampled render grid (visualization-only)."""
    d = np.load(DEM_GRID)
    elev = d["elev"]
    west, north, cell = float(d["west"]), float(d["north"]), float(d["cell_deg"])
    r = int((north - lat) / cell)
    c = int((lon - west) / cell)
    return int(elev[r, c])


def main():
    print("Elevation audit (conventions v1.0 s.4): full-res tiles vs render grid")
    print(f"{'point':28s} {'full-res (citable)':>18s} {'render grid':>12s} {'reference':>10s}")
    for label, lat, lon, ref, ref_src in BENCHMARKS:
        fr = full_res_elevation(lat, lon)
        gr = grid_elevation(lat, lon)
        print(f"{label:28s} {fr:>15d} m {gr:>10d} m {ref:>7d} m ({ref_src})")
    print(
        "\nRule: figures shown to the reader come from the full-res column\n"
        "(or the named reference), never the render-grid column."
    )


if __name__ == "__main__":
    main()
