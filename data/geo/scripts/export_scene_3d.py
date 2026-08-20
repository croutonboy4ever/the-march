#!/usr/bin/env python3
"""Export one pass scene as a 3D model and measure what it costs.

Measurement spike for the scoped-3D question: if client-side 3D exists only at
a short list of named scenes, each scene is a baked model shipped as a static
file, not terrain streamed from a tile service. This script builds that model
for R1 (Col de la Traversette) and reports the real numbers instead of
estimates: triangle counts, file sizes, how much surface shape each mesh
density loses against the source, and how far a reader could zoom before the
model runs out.

Window and register match render_2p5d_options.py exactly: 6.90-7.25 E,
44.60-44.82 N, direction B autumn-crossing, read from the full-resolution
1-arc-second tiles (SOURCES.md section 3). Nothing here uses the 4x corridor
render grid.

Output format is GLB (binary glTF 2.0), written by hand rather than by adding
a dependency for a spike. One mesh + one baked JPEG texture per file, which is
what a scoped scene actually ships: the fine detail rides in the texture, the
geometry only has to carry shape.

Metric note, so a later session does not misread these numbers: the deviation
figures below are mesh-versus-source fidelity metrics in metres, describing how
far a decimated surface departs from the source surface. They are not elevation
figures about any place, and none of them is ever displayed to a reader.
Conventions v1.0 section 4 governs displayed elevations and is untouched here.

Outputs, under site/poc/2p5d-options/scene-3d/:
  traversette-r1.glb    the representative export (stride chosen below)
  MEASUREMENTS.json     every level measured, machine-readable

Run with the project venv:
  .venv/bin/python data/geo/scripts/export_scene_3d.py
"""

import io
import json
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib

matplotlib.use("Agg")
import numpy as np
from PIL import Image

import render_2p5d_options as opt

OUT_DIR = os.path.join(opt.OUT_DIR, "scene-3d")

# Mesh densities to measure. Stride 1 keeps every source sample; stride 8 keeps
# one in eight along each axis.
STRIDES = [1, 2, 3, 4, 6, 8]

# The level committed as the representative export.
REPRESENTATIVE_STRIDE = 3

# Assumed viewport width in CSS pixels for the zoom-floor arithmetic. A desktop
# reader at roughly this width is the case that stresses the mesh hardest.
VIEWPORT_PX = 1600

# Screen pixels per mesh sample at which the surface stops reading as smooth.
# Two thresholds, because degradation is gradual rather than a cliff.
PX_PER_SAMPLE_SOFT = 4.0    # detail visibly thinning
PX_PER_SAMPLE_HARD = 8.0    # faceting / softness obvious

TEXTURE_QUALITY = 88


def sample_indices(n, stride):
    """Kept indices along one axis, always including the last sample.

    Including the last index guarantees the mesh covers the whole window even
    when the stride does not divide the axis evenly, which matters because the
    texture is mapped by true grid position.
    """
    idx = np.arange(0, n, stride)
    if idx[-1] != n - 1:
        idx = np.append(idx, n - 1)
    return idx


def reconstruct(elev, ri, ci):
    """Put a decimated surface back on the full grid by bilinear interpolation.

    This is what the coarse mesh actually represents between its vertices, so
    comparing it against the source is the honest fidelity measure, and
    rendering it with the full-resolution texture is the honest picture of a
    low-poly mesh under a baked texture.
    """
    kept = elev[np.ix_(ri, ci)]
    rows_full = np.arange(elev.shape[0])
    cols_full = np.arange(elev.shape[1])
    along_cols = np.empty((len(ri), elev.shape[1]))
    for k in range(len(ri)):
        along_cols[k] = np.interp(cols_full, ci, kept[k])
    out = np.empty(elev.shape)
    for j in range(elev.shape[1]):
        out[:, j] = np.interp(rows_full, ri, along_cols[:, j])
    return out


def build_mesh(elev, cell, stride):
    """Vertices, texcoords and triangles for one mesh density.

    glTF is Y-up and right-handed, so the mapping is x=east, y=elevation,
    z=south. Metres throughout, measured from the window's northwest corner.
    """
    rows_full, cols_full = elev.shape
    ri = sample_indices(rows_full, stride)
    ci = sample_indices(cols_full, stride)
    rows, cols = len(ri), len(ci)

    dx = cell * opt.M_PER_DEG_LON
    dz = cell * opt.M_PER_DEG_LAT

    xs = ci.astype(np.float64) * dx
    zs = ri.astype(np.float64) * dz
    X, Z = np.meshgrid(xs, zs)
    Y = elev[np.ix_(ri, ci)]

    positions = np.stack([X, Y, Z], axis=-1).reshape(-1, 3).astype(np.float32)

    u = (ci.astype(np.float64) / (cols_full - 1)).astype(np.float32)
    v = (ri.astype(np.float64) / (rows_full - 1)).astype(np.float32)
    U, V = np.meshgrid(u, v)
    uvs = np.stack([U, V], axis=-1).reshape(-1, 2).astype(np.float32)

    r = np.arange(rows - 1)[:, None]
    c = np.arange(cols - 1)[None, :]
    v00 = (r * cols + c).ravel()
    v01 = (r * cols + c + 1).ravel()
    v10 = ((r + 1) * cols + c).ravel()
    v11 = ((r + 1) * cols + c + 1).ravel()
    tris = np.empty((v00.size * 2, 3), dtype=np.uint32)
    tris[0::2] = np.stack([v00, v10, v11], axis=-1)
    tris[1::2] = np.stack([v00, v11, v01], axis=-1)

    return positions, uvs, tris, ri, ci


def _pad(buf, fill=b"\x00"):
    while len(buf) % 4:
        buf += fill
    return buf


def write_glb(path, positions, uvs, tris, image_bytes):
    """Minimal single-mesh, single-texture binary glTF 2.0."""
    if positions.shape[0] <= 65535:
        indices = tris.astype(np.uint16)
        index_component = 5123
    else:
        indices = tris.astype(np.uint32)
        index_component = 5125

    pos_b = _pad(positions.tobytes())
    uv_b = _pad(uvs.tobytes())
    idx_b = _pad(indices.tobytes())
    img_b = _pad(image_bytes)

    blob = pos_b + uv_b + idx_b + img_b
    off_pos, off_uv = 0, len(pos_b)
    off_idx = off_uv + len(uv_b)
    off_img = off_idx + len(idx_b)

    gltf = {
        "asset": {
            "version": "2.0",
            "generator": "the-march export_scene_3d.py (measurement spike)",
        },
        "scene": 0,
        "scenes": [{"nodes": [0]}],
        "nodes": [{"mesh": 0, "name": "traversette-r1"}],
        "meshes": [{
            "name": "terrain",
            "primitives": [{
                "attributes": {"POSITION": 0, "TEXCOORD_0": 1},
                "indices": 2,
                "material": 0,
            }],
        }],
        "materials": [{
            "name": "baked-relief",
            "doubleSided": True,
            "pbrMetallicRoughness": {
                "baseColorTexture": {"index": 0},
                "metallicFactor": 0.0,
                "roughnessFactor": 1.0,
            },
        }],
        "textures": [{"sampler": 0, "source": 0}],
        "samplers": [{
            "magFilter": 9729, "minFilter": 9987,
            "wrapS": 33071, "wrapT": 33071,
        }],
        "images": [{"bufferView": 3, "mimeType": "image/jpeg"}],
        "accessors": [
            {
                "bufferView": 0, "componentType": 5126, "count": int(positions.shape[0]),
                "type": "VEC3",
                "min": [float(positions[:, i].min()) for i in range(3)],
                "max": [float(positions[:, i].max()) for i in range(3)],
            },
            {
                "bufferView": 1, "componentType": 5126,
                "count": int(uvs.shape[0]), "type": "VEC2",
            },
            {
                "bufferView": 2, "componentType": index_component,
                "count": int(indices.size), "type": "SCALAR",
            },
        ],
        "bufferViews": [
            {"buffer": 0, "byteOffset": off_pos, "byteLength": positions.nbytes,
             "target": 34962},
            {"buffer": 0, "byteOffset": off_uv, "byteLength": uvs.nbytes,
             "target": 34962},
            {"buffer": 0, "byteOffset": off_idx, "byteLength": indices.nbytes,
             "target": 34963},
            {"buffer": 0, "byteOffset": off_img, "byteLength": len(image_bytes)},
        ],
        "buffers": [{"byteLength": len(blob)}],
    }

    json_b = _pad(json.dumps(gltf, separators=(",", ":")).encode("utf-8"), b" ")
    total = 12 + 8 + len(json_b) + 8 + len(blob)
    with open(path, "wb") as f:
        f.write(struct.pack("<III", 0x46546C67, 2, total))
        f.write(struct.pack("<II", len(json_b), 0x4E4F534A))
        f.write(json_b)
        f.write(struct.pack("<II", len(blob), 0x004E4942))
        f.write(blob)
    return total


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    elev, cell = opt.rcz.full_res_window()
    rows, cols = elev.shape
    print(f"source window: {rows} x {cols} samples at {cell:.8f} deg")

    # One baked texture, computed once at source resolution and reused by every
    # mesh density. This is the point of the approach: geometry gets cheaper,
    # the texture does not.
    rgb = opt.shade(elev, cell)
    img = Image.fromarray((rgb[:, :, :3] * 255).astype(np.uint8))
    jpeg_buf = io.BytesIO()
    img.save(jpeg_buf, format="JPEG", quality=TEXTURE_QUALITY, optimize=True)
    jpeg_bytes = jpeg_buf.getvalue()
    png_buf = io.BytesIO()
    img.save(png_buf, format="PNG", optimize=True)
    print(f"baked texture: {img.size[0]}x{img.size[1]}, "
          f"jpeg {len(jpeg_bytes)/1e6:.2f} MB, png {len(png_buf.getvalue())/1e6:.2f} MB")

    # Ground sample spacing of the source, per axis. North-south is the coarser
    # of the two and therefore sets the limit.
    dx_m = cell * opt.M_PER_DEG_LON
    dz_m = cell * opt.M_PER_DEG_LAT
    window_width_m = (cols - 1) * dx_m
    print(f"window ground width: {window_width_m/1000:.1f} km, "
          f"source spacing {dx_m:.1f} m east-west / {dz_m:.1f} m north-south")

    results = []
    for stride in STRIDES:
        positions, uvs, tris, ri, ci = build_mesh(elev, cell, stride)
        recon = reconstruct(elev, ri, ci)
        err = recon - elev
        max_dev = float(np.abs(err).max())
        rms_dev = float(np.sqrt((err ** 2).mean()))

        path = os.path.join(OUT_DIR, f"_probe-s{stride}.glb")
        size = write_glb(path, positions, uvs, tris, jpeg_bytes)

        sample_m = dz_m * stride
        soft_km = VIEWPORT_PX * sample_m / PX_PER_SAMPLE_SOFT / 1000.0
        hard_km = VIEWPORT_PX * sample_m / PX_PER_SAMPLE_HARD / 1000.0

        row = {
            "stride": stride,
            "vertices": int(positions.shape[0]),
            "triangles": int(tris.shape[0]),
            "glb_bytes": int(size),
            "max_deviation_m": round(max_dev, 1),
            "rms_deviation_m": round(rms_dev, 2),
            "sample_spacing_m": round(sample_m, 1),
            "soft_limit_view_km": round(soft_km, 2),
            "hard_limit_view_km": round(hard_km, 2),
        }
        results.append(row)
        print(f"  stride {stride}: {row['triangles']:>9,} tris  "
              f"{size/1e6:>6.2f} MB  dev max {max_dev:>6.1f} m rms {rms_dev:>5.2f} m  "
              f"soft floor {soft_km:.1f} km / hard floor {hard_km:.1f} km")
        if stride != REPRESENTATIVE_STRIDE:
            os.remove(path)
        else:
            os.replace(path, os.path.join(OUT_DIR, "traversette-r1.glb"))

    meta = {
        "scene": "Col de la Traversette (R1) window",
        "window_deg": {"west": opt.WINDOW[0], "south": opt.WINDOW[1],
                       "east": opt.WINDOW[2], "north": opt.WINDOW[3]},
        "source": "1-arc-second tiles, SOURCES.md section 3; no render grid used",
        "source_samples": [rows, cols],
        "source_spacing_m": {"east_west": round(dx_m, 1),
                             "north_south": round(dz_m, 1)},
        "window_ground_width_km": round(window_width_m / 1000.0, 2),
        "texture": {"pixels": [img.size[0], img.size[1]],
                    "jpeg_bytes": len(jpeg_bytes),
                    "png_bytes": len(png_buf.getvalue()),
                    "jpeg_quality": TEXTURE_QUALITY},
        "viewport_px_assumed": VIEWPORT_PX,
        "px_per_sample_thresholds": {"soft": PX_PER_SAMPLE_SOFT,
                                     "hard": PX_PER_SAMPLE_HARD},
        "representative_stride": REPRESENTATIVE_STRIDE,
        "deviation_metric_note": (
            "mesh-versus-source surface fidelity in metres; not an elevation "
            "figure about any place and never displayed to a reader"),
        "levels": results,
    }
    with open(os.path.join(OUT_DIR, "MEASUREMENTS.json"), "w") as f:
        json.dump(meta, f, indent=2)
    print(f"wrote {os.path.relpath(os.path.join(OUT_DIR, 'MEASUREMENTS.json'))}")


if __name__ == "__main__":
    main()
