#!/usr/bin/env python3
"""Mosaic SRTM-derived HGT tiles into one corridor elevation grid.

Input : data/geo/raw/dem/N{43..45}E{004..007}.hgt.gz
        (12 skadi-format 1-arc-second tiles, see data/geo/SOURCES.md)
Output: data/geo/processed/dem-corridor.npz
        containing: elev (int16, meters), and the grid's lon/lat extent
        and cell size as scalar arrays.

HGT format: each tile is 3601 x 3601 big-endian int16 samples, one degree
square, row 0 at the tile's north edge, sample spacing 1 arc-second, void
value -32768. Adjacent tiles share their edge row/column.

Processing, in order:
1. Mosaic the 12 tiles into a 3x4 degree grid (43-46 N, 4-8 E),
   10801 x 14401 samples, dropping each tile's duplicated shared edges.
2. Crop to the corridor bbox 4.0-8.0 E, 43.5-46.0 N.
3. Downsample by block mean over 4x4 sample blocks (~120 m cells), which
   keeps the grid a faithful average of the source samples and keeps the
   committed file small. Voids are excluded from block means; a block that
   is all void stays void.

Usage: python3 data/geo/scripts/build_dem.py
"""

import gzip
import os

import numpy as np

BBOX = (4.0, 43.5, 8.0, 46.0)  # min lon, min lat, max lon, max lat
LATS = [43, 44, 45]
LONS = [4, 5, 6, 7]
N = 3601  # samples per tile side
VOID = -32768
FACTOR = 4  # downsample block size

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "raw", "dem")
OUT = os.path.join(ROOT, "processed", "dem-corridor.npz")


def read_tile(lat, lon):
    path = os.path.join(RAW, f"N{lat:02d}E{lon:03d}.hgt.gz")
    with gzip.open(path, "rb") as f:
        data = np.frombuffer(f.read(), dtype=">i2")
    if data.size != N * N:
        raise ValueError(f"{path}: expected {N*N} samples, got {data.size}")
    return data.reshape(N, N).astype(np.int16)


def main():
    lat_span = LATS[-1] + 1 - LATS[0]  # 3 degrees
    lon_span = LONS[-1] + 1 - LONS[0]  # 4 degrees
    rows = lat_span * (N - 1) + 1
    cols = lon_span * (N - 1) + 1
    mosaic = np.full((rows, cols), VOID, dtype=np.int16)
    for lat in LATS:
        for lon in LONS:
            tile = read_tile(lat, lon)
            # Row 0 of the mosaic is the north edge (lat 46.0).
            r0 = (LATS[-1] - lat) * (N - 1)
            c0 = (lon - LONS[0]) * (N - 1)
            mosaic[r0 : r0 + N, c0 : c0 + N] = tile
            print(f"placed N{lat}E{lon:03d} at row {r0}, col {c0}")

    # Crop: bbox min lat 43.5 cuts the bottom half of the N43 row.
    north, south = LATS[-1] + 1, LATS[0]  # 46.0, 43.0
    cells_per_deg = N - 1  # 3600
    r_end = round((north - BBOX[1]) * cells_per_deg) + 1
    grid = mosaic[:r_end, :]
    print(f"cropped to {grid.shape} (lat {BBOX[1]}-{north}, lon {LONS[0]}-{LONS[-1]+1})")

    # Block-mean downsample, void-aware. Trim the +1 edge row/col so the
    # dimensions divide evenly by FACTOR.
    r, c = grid.shape
    r -= (r - 1) % FACTOR + 1 if (r % FACTOR) == 1 else r % FACTOR
    c -= (c - 1) % FACTOR + 1 if (c % FACTOR) == 1 else c % FACTOR
    g = grid[:r, :c].astype(np.float64)
    void_mask = g == VOID
    g[void_mask] = np.nan
    blocks = g.reshape(r // FACTOR, FACTOR, c // FACTOR, FACTOR)
    with np.errstate(invalid="ignore"):
        mean = np.nanmean(blocks, axis=(1, 3))
    voids = np.isnan(mean)
    mean[voids] = VOID
    elev = np.round(mean).astype(np.int16)
    print(f"downsampled x{FACTOR} to {elev.shape}; void cells: {int(voids.sum())}")
    print(f"elevation range: {elev[elev != VOID].min()} to {elev.max()} m")

    cell = FACTOR / cells_per_deg  # degrees per output cell
    np.savez_compressed(
        OUT,
        elev=elev,
        # Grid registration: cell (0,0) covers the block whose NW corner is
        # (west edge, north edge); extents describe the covered area.
        west=np.float64(BBOX[0]),
        north=np.float64(north),
        cell_deg=np.float64(cell),
        void=np.int16(VOID),
    )
    print(f"wrote {OUT} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
