#!/usr/bin/env python3
"""Extract ESA WorldCover land cover to a corridor grid aligned to the DEM grid.

Input : data/geo/raw/landcover/ESA_WorldCover_10m_2021_v200_{N42E003,N42E006,
        N45E003,N45E006}_Map.tif  (4 tiles, 3x3 degrees each, 10 m / 1/12000
        degree pixels, uint8 class codes; see data/geo/SOURCES.md section 6)
Output: data/geo/processed/landcover-corridor.npz
        cls   uint8, the majority WorldCover class per DEM cell (0 = no data)
        frac  uint8, percent of the cell's valid pixels in the majority class
        west/north/cell_deg, matching data/geo/processed/dem-corridor.npz

Grid alignment: the output grid is cell-for-cell the DEM render grid
(2250 x 3600, 1/900 degree cells, west 4.0, north 46.0; see build_dem.py).
Each WorldCover pixel is assigned to the DEM cell containing its center
(40 WC pixels = exactly 3 DEM cells per axis, so ~13-14 pixels per cell per
axis, ~178 per cell); each cell takes its most frequent class. Ties break
toward the lower class code (argmax order); with ~178 pixels per cell ties
are rare and the choice is deterministic. WorldCover nodata (0) is excluded
from the vote; a cell with no valid pixels stays 0.

The full class set is preserved in the output, including cropland (40),
built-up (50), and herbaceous wetland (90). Which classes render, and how,
is a rendering decision made in the render scripts, not here: conventions
say gaps and pending decisions are surfaced, not baked into data. The
natural-classes-only rule (tree/shrub/grass/bare/snow/water as
terrain-texture basis, built-up masked) is applied at render time; the
cropland-class call is Tony's, flagged in the session close-out.

WorldCover is a MODERN (2021) dataset. Everywhere this layer renders it is
captioned as modern-basis texture; ancient vegetation is a separate
inference and out of scope for this layer.

Class codes (WorldCover v200 product manual):
  10 tree cover        20 shrubland        30 grassland
  40 cropland          50 built-up         60 bare / sparse vegetation
  70 snow and ice      80 permanent water  90 herbaceous wetland
  95 mangroves         100 moss and lichen

Run with the project venv (needs tifffile, see README):
  .venv/bin/python data/geo/scripts/extract_landcover.py
"""

import os

import numpy as np
import tifffile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
RAW = os.path.join(ROOT, "raw", "landcover")
DEM = os.path.join(ROOT, "processed", "dem-corridor.npz")
OUT = os.path.join(ROOT, "processed", "landcover-corridor.npz")

BBOX = (4.0, 43.5, 8.0, 46.0)  # min lon, min lat, max lon, max lat
WC_PER_DEG = 12000             # WorldCover pixels per degree (10 m)
CLASSES = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]

# The 4 tiles and their top-left (NW) corner in degrees.
TILES = {
    "N42E003": (3, 45),
    "N42E006": (6, 45),
    "N45E003": (3, 48),
    "N45E006": (6, 48),
}
CHUNK_WC_ROWS = 4000  # multiple of 40, so chunks align to whole DEM rows


def tile_path(key):
    return os.path.join(RAW, f"ESA_WorldCover_10m_2021_v200_{key}_Map.tif")


def check_georef(tif, key, nw_lon, nw_lat):
    """Assert the tile's GeoTIFF tags match the documented grid."""
    page = tif.pages[0]
    tags = page.tags
    scale = tags["ModelPixelScaleTag"].value
    tie = tags["ModelTiepointTag"].value
    assert page.shape == (3 * WC_PER_DEG, 3 * WC_PER_DEG), (key, page.shape)
    assert page.dtype == np.uint8, (key, page.dtype)
    assert abs(scale[0] - 1 / WC_PER_DEG) < 1e-12, (key, scale)
    assert abs(scale[1] - 1 / WC_PER_DEG) < 1e-12, (key, scale)
    # Tiepoint: raster (0,0) -> (lon, lat) of the NW corner.
    assert abs(tie[3] - nw_lon) < 1e-9 and abs(tie[4] - nw_lat) < 1e-9, (key, tie)


def main():
    d = np.load(DEM)
    dem_west = float(d["west"])
    dem_north = float(d["north"])
    cell = float(d["cell_deg"])
    rows, cols = d["elev"].shape
    assert dem_west == BBOX[0] and dem_north == BBOX[3], (dem_west, dem_north)
    assert abs(cell - 1 / 900) < 1e-15, cell
    assert (rows, cols) == (2250, 3600), (rows, cols)

    # Class code -> vote index; nodata and anything unexpected -> 11 (dropped).
    lut = np.full(256, 11, dtype=np.uint8)
    for i, c in enumerate(CLASSES):
        lut[c] = i

    cls = np.zeros((rows, cols), dtype=np.uint8)
    frac = np.zeros((rows, cols), dtype=np.uint8)
    totals = np.zeros(12, dtype=np.int64)

    for key, (nw_lon, nw_lat) in TILES.items():
        # Tile overlap with the corridor bbox, in WC pixel indices.
        # Global WC indices: gi = 0 at lat 46.0 N, gj = 0 at lon 4.0 E.
        lon0, lon1 = max(BBOX[0], nw_lon), min(BBOX[2], nw_lon + 3)
        lat1, lat0 = min(BBOX[3], nw_lat), max(BBOX[1], nw_lat - 3)
        tr0 = round((nw_lat - lat1) * WC_PER_DEG)   # tile row range
        tr1 = round((nw_lat - lat0) * WC_PER_DEG)
        tc0 = round((lon0 - nw_lon) * WC_PER_DEG)   # tile col range
        tc1 = round((lon1 - nw_lon) * WC_PER_DEG)
        gi0 = round((BBOX[3] - lat1) * WC_PER_DEG)  # global row of tile row tr0
        gj0 = round((lon0 - BBOX[0]) * WC_PER_DEG)  # global col of tile col tc0

        # DEM columns covered by this tile (tile lon edges land on DEM cell
        # edges: 40 WC pixels = 3 DEM cells, and the overlap width in pixels
        # is a multiple of 40).
        assert gj0 % 40 == 0 and (tc1 - tc0) % 40 == 0 and gi0 % 40 == 0
        c0 = gj0 * 3 // 40
        c1 = (gj0 + (tc1 - tc0)) * 3 // 40
        # WC col (within the read window) -> DEM col offset, by pixel center.
        col_map = ((3 * (gj0 + np.arange(tc1 - tc0)) + 1) // 40 - c0).astype(
            np.int64
        )

        with tifffile.TiffFile(tile_path(key)) as tif:
            check_georef(tif, key, nw_lon, nw_lat)
            # Whole-tile read (1.3 GB uint8, freed after the tile). The
            # chunked loop below keeps the per-step working set small.
            store = tif.pages[0].asarray()
            for r in range(tr0, tr1, CHUNK_WC_ROWS):
                r_end = min(r + CHUNK_WC_ROWS, tr1)
                block = store[r:r_end, tc0:tc1]
                gi = gi0 + (r - tr0)
                assert gi % 40 == 0 and (r_end - r) % 40 == 0
                r0d = gi * 3 // 40
                r1d = (gi + (r_end - r)) * 3 // 40
                row_map = (
                    (3 * (gi + np.arange(r_end - r)) + 1) // 40 - r0d
                ).astype(np.int64)

                votes = lut[block]
                flat = (
                    row_map[:, None] * (c1 - c0) + col_map[None, :]
                ) * 12 + votes
                counts = np.bincount(
                    flat.ravel(), minlength=(r1d - r0d) * (c1 - c0) * 12
                ).reshape(r1d - r0d, c1 - c0, 12)
                totals += counts.sum(axis=(0, 1))
                valid = counts[:, :, :11]
                n_valid = valid.sum(axis=2)
                winner = valid.argmax(axis=2)
                win_count = np.take_along_axis(
                    valid, winner[:, :, None], axis=2
                )[:, :, 0]
                has = n_valid > 0
                block_cls = np.zeros_like(winner, dtype=np.uint8)
                block_cls[has] = np.array(CLASSES, dtype=np.uint8)[winner[has]]
                block_frac = np.zeros_like(block_cls)
                block_frac[has] = np.round(
                    100 * win_count[has] / n_valid[has]
                ).astype(np.uint8)
                cls[r0d:r1d, c0:c1] = block_cls
                frac[r0d:r1d, c0:c1] = block_frac
            del store
            print(f"{key}: rows {tr0}-{tr1}, cols {tc0}-{tc1} -> "
                  f"dem cols {c0}-{c1}")

    total_px = int(totals.sum())
    print(f"pixels voted: {total_px:,} (nodata/unexpected dropped: "
          f"{int(totals[11]):,})")
    for i, c in enumerate(CLASSES):
        print(f"  class {c:3d}: {int(totals[i]):,} px "
              f"({100 * totals[i] / total_px:.2f}%)")
    n_cells, counts = np.unique(cls, return_counts=True)
    print("majority-class cells:",
          {int(k): int(v) for k, v in zip(n_cells, counts)})
    print(f"majority-fraction: median {int(np.median(frac[cls > 0]))}%, "
          f"p10 {int(np.percentile(frac[cls > 0], 10))}%")

    np.savez_compressed(
        OUT,
        cls=cls,
        frac=frac,
        west=np.float64(BBOX[0]),
        north=np.float64(BBOX[3]),
        cell_deg=np.float64(cell),
    )
    print(f"wrote {OUT} ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
