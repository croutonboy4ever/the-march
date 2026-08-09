# Data sources and provenance

Every data file under `data/geo` is listed here with origin URL, date pulled, and
license. Raw downloads too large for git live in `data/geo/raw/` on disk only
(gitignored); their checksums here are the fixed reference. Processed files are
committed and each is the output of a named script over a named raw file. Gaps —
sources that were unreachable or data that does not exist — are recorded in the
Gaps section at the bottom, not papered over.

## 1. Pleiades gazetteer (ancient places)

- **What**: Daily JSON dump of all Pleiades places (ancient-world gazetteer).
- **Origin URL**: https://atlantides.org/downloads/pleiades/json/pleiades-places-latest.json.gz
  (public dumps published by the Pleiades project, pleiades.stoa.org).
- **Date pulled**: 2026-08-09. Server Last-Modified: 2026-08-09 11:12 UTC (dump regenerates daily).
- **License**: Creative Commons Attribution 3.0 (CC-BY); Pleiades content requires
  attribution to "Pleiades: A community-built gazetteer and graph of ancient places."
- **Raw file** (on disk, gitignored): `raw/pleiades-places-latest.json.gz`,
  135,529,520 bytes, sha256 `d53814c76d1ff7e43c0091c61b82069f6201565e41029c02f4b9f91b01ee1b7c`.
- **Processed file** (committed): `processed/pleiades-places-corridor.geojson` —
  705 places whose Pleiades representative point falls in the corridor bbox
  4.0–8.0 E, 43.5–46.0 N. Produced by `scripts/extract_pleiades.py`.
  7,576 places in the dump carry no coordinates at all and are excluded as
  unplaceable (Pleiades itself does not locate them; we do not invent coordinates).

## 2. AWMC geodata (Roman roads, ancient shoreline)

- **What**: Roads and coastline/shoreline GeoJSON from the Ancient World Mapping
  Center working data set. Roads derive from the Barrington Atlas of the Greek
  and Roman World; the shoreline derives from VMAP0 with AWMC modifications
  (per the READMEs archived in `raw/awmc-repo-README.md` and
  `raw/awmc-shoreline-README.md`).
- **Origin URLs**:
  - https://raw.githubusercontent.com/AWMC/geodata/master/Cultural-Data/roads/roads.geojson
  - https://raw.githubusercontent.com/AWMC/geodata/master/Physical%20Data/shoreline/shoreline.geojson
  (repo: https://github.com/AWMC/geodata)
- **Date pulled**: 2026-08-09.
- **License**: ODC Open Database License (ODbL) 1.0, per the repo README
  (archived at `raw/awmc-repo-README.md`).
- **Raw files** (committed; small enough for git, force-added past the raw/ ignore):
  - `raw/awmc-roads.geojson`, 5,281,885 bytes,
    sha256 `d28e5a1675a59df0037a84e6a8dc5f6b8efc75dbbd74a76ace59dd8285604516`
  - `raw/awmc-shoreline.geojson`, 19,009,980 bytes,
    sha256 `1497761447e0c11d01f50d3795647494d554b7d492b2f9ca64385d5da2a69212`
- **Processed files** (committed), produced by `scripts/clip_awmc.py`; feature
  selection by bbox overlap, geometries unmodified from source:
  - `processed/awmc-roads-corridor.geojson` — 137 of 3,166 road features.
  - `processed/awmc-shoreline-corridor.geojson` — 8 of 9,901 shoreline features
    (only the southern edge of the corridor touches the Mediterranean).

## Gaps

None recorded yet.
