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

## 3. Elevation (DEM): Terrain Tiles on AWS, skadi format

- **What**: 12 one-degree, 1-arc-second elevation tiles (skadi/HGT format)
  covering 43–46 N, 4–8 E. The Terrain Tiles dataset (originally Mapzen, now
  an AWS Open Data public bucket) composites public-domain sources; over
  Europe at this resolution the land data is NASA SRTM (with EU-DEM-derived
  void filling per the dataset docs) and offshore values come from NOAA
  ETOPO1 bathymetry, which is why sea cells carry negative elevations.
- **Origin URL pattern**: https://s3.amazonaws.com/elevation-tiles-prod/skadi/{N##}/{N##E###}.hgt.gz
  (dataset page: https://registry.opendata.aws/terrain-tiles/ ; source/attribution
  docs: https://github.com/tilezen/joerd/blob/master/docs/data-sources.md).
- **Date pulled**: 2026-08-09.
- **License**: The underlying sources are U.S.-government public domain
  (SRTM: NASA/USGS; ETOPO1: NOAA). The Terrain Tiles docs request attribution
  to the data sources; the site will carry "Elevation data: SRTM (NASA) et al.
  via Terrain Tiles on AWS".
- **Raw files** (on disk, gitignored): `raw/dem/N4{3,4,5}E00{4,5,6,7}.hgt.gz`,
  12 tiles, 156.9 MB total. sha256:
  - `N43E004` `b23a118b4711614951d2ccbc09cf82037718090fa9ff30fbe134614501315af9`
  - `N43E005` `acc341b8193ee1d986de2842bdb44478176fc18048c99869d6d24fdd223524eb`
  - `N43E006` `f0d21bc4fb5e8aef25a8acf8b04435a063193000bc3c1285d1a44c144c65ca5f`
  - `N43E007` `b8bb310b4a8494e464c7dc819f9ab73b0b44bee7da3b074d0a59277b635d2d09`
  - `N44E004` `359cfefa878e2a7c4e7374f093eb4012199d4eea42c57fad6dff97695cc0447f`
  - `N44E005` `012a64e7d42097877dadfa3c34068e9fb8a63b5f608570b5772c7ab0838ae146`
  - `N44E006` `92ba59c137e50a864983ee93d7221a332785ec42ced92273cf25d420c65128c8`
  - `N44E007` `21c0e89f601c5decc1d04c920d9fed18d54ec6affbf4fe69baaaf4ee4b452fb2`
  - `N45E004` `a3488cfd9b15851b4391bd9a74566dfcdf2a514dcbe972f90f03e74c9161273e`
  - `N45E005` `e06037ca5809e231132fe9e74539dd94d943f8f27b613e6c6368d6905143b0e6`
  - `N45E006` `6b9699a7d05ad3cf36af7bb1ddbf35f2a465e9236953675afec8552018825651`
  - `N45E007` `8f98a452476e0c0af474649d59ebd3c5c40211b2d189ad1fb748ada01b953e6f`
- **Processed file** (committed): `processed/dem-corridor.npz` — mosaic of the
  12 tiles cropped to the corridor bbox and block-mean downsampled 4x to
  ~120 m cells (2250 x 3600 int16 grid, 11.1 MB). Produced by
  `scripts/build_dem.py`. Verified against known elevations: Mont Ventoux
  1898 (map) vs 1909 (true), Barre des Ecrins 3995 vs 4102 (summit reads low
  under block averaging, as expected), Col du Mont Cenis 2113 vs 2081,
  Avignon valley floor 30 vs ~20.

## 4. AWMC water: rivers and inland water

- **What**: River linework and inland-water (lake/swamp/dry-lake) polygons
  from the AWMC geodata set.
  - **Rivers**: `rivers/awmc-osm-rivers.{shp,dbf,...}` from the repo-root
    archive "Physical Shapefiles Apr 2024.zip". Finding recorded here so the
    next pull does not repeat the search: the repo's unzipped
    `Physical Data/inland_water/` directory contains **no river linework at
    all** (it is lake/swamp polygons, checked 2026-08-09, zero name matches
    for Rhone/Durance/Isere in any spelling); the river linework exists only
    inside the Apr 2024 zip. Attribution fields mark the corridor rivers as
    Barrington-derived (origin BAMap17/BAMap18/BAMap15) with AWMC/OSM
    curation (`awmc_mod=1`), keyed to Pleiades IDs in a `pid` field.
  - **Inland water**: `Physical Data/inland_water/inland-water-OSM.geojson`
    (lake/swamp/dry-lake polygons; OSM-derived per filename, AWMC-modified).
- **Origin URLs**:
  - https://raw.githubusercontent.com/AWMC/geodata/master/Physical%20Shapefiles%20Apr%202024.zip
  - https://raw.githubusercontent.com/AWMC/geodata/master/Physical%20Data/inland_water/inland-water-OSM.geojson
  (repo: https://github.com/AWMC/geodata)
- **Date pulled**: 2026-08-09.
- **License**: ODC Open Database License (ODbL) 1.0, per the repo README
  (archived at `raw/awmc-repo-README.md`).
- **Raw files** (on disk, gitignored; too large for git):
  - `raw/awmc-physical-shapefiles-2024-04.zip`, 20,512,878 bytes,
    sha256 `d64b768e520f61e53b32013c262bb6cfeca7cca92cfacadfc828071d812bf0ec`
  - `raw/awmc-rivers/awmc-osm-rivers.shp`, 10,142,520 bytes,
    sha256 `ad1e1b7ada562d7ed1781e3a87ac5d5be593cf4d29a7a8466f4235198f939d2d`
  - `raw/awmc-rivers/awmc-osm-rivers.dbf`, 19,447,250 bytes,
    sha256 `3aa5f80ed63c37b75687064702a8e253cbd8792981cefc10108c2b055e144d0d`
  - `raw/awmc-inland-water-OSM.geojson`, 15,946,794 bytes,
    sha256 `a6228834c7149277da8619efa6ce0c042ff54d5eb5d14c7e1b79f36d361205e5`
- **Processed files** (committed), produced by `scripts/extract_awmc_water.py`;
  geometries unmodified from source:
  - `processed/awmc-rivers-corridor.geojson` — the Rhone (Rhodanus, Pleiades
    148168), Durance (Druentia, 148069), and Isere (Isara, 167793), selected
    by Pleiades ID, never by name string; plus 5 unnamed segments the source
    itself annotates `notes="Rhodanus delta"` (Barrington Map 15 delta
    distributaries, no pid of their own).
  - `processed/awmc-inland-water-corridor.geojson` — 615 of 6,393 polygons
    whose bounding box overlaps the corridor.
- **Authority note**: AWMC linework is the authority for ancient-period river
  courses; modern hydrology, like modern SRTM terrain, is real but modern;
  the Rhone's course and delta have shifted since 218 BC.

## Gaps

Known gaps as of 2026-08-09. All sources targeted by the spike were reachable;
these are data-shape gaps, not fetch failures.

1. **Resolved 2026-08-09: river linework pulled.** The Rhone, Durance, and
   Isere are now extracted (see section 4) and drawn on the POC render. The
   gap as originally recorded pointed at `Physical Data/inland_water/`; that
   directory turned out to hold no river linework (lakes only) — the rivers
   came from the repo's Apr 2024 physical-shapefiles zip instead, as section 4
   records.
2. **Modern topography, ancient labels.** SRTM is present-day terrain. For this
   corridor that is acceptable (mountain relief is effectively unchanged), but
   the Rhone delta around the Camargue has shifted since 218 BC, which is why
   the AWMC ancient shoreline and the modern SRTM sea edge disagree slightly
   at the coast. The experience should draw the AWMC line, not the SRTM edge,
   wherever the two conflict on ancient-period questions.
3. **7,576 Pleiades places have no coordinates** dump-wide and are excluded as
   unplaceable. Corridor-relevant places among them cannot appear on the map
   until Pleiades locates them; they are not invented.
4. **Uncertain pass identifications are structural, not resolved.** Pleiades
   itself carries six candidate locations titled "Pass of the Alpes Graiae"
   (west of Segusio) plus distinct pass places (Matrona/Montgenèvre, Alpis
   Graia/Little St Bernard, Alpis Cottia). The POC renders candidates as
   unlabeled dots; the real experience must present the Alpine-route debate
   per conventions doc sections 2 and 6.
5. **DEM negative values offshore are ETOPO1 bathymetry**, not errors; the
   renderer masks elevation <= 0 as sea. Any future shoreline-accurate
   rendering must use the AWMC line instead of the 0 m contour (see gap 2).
