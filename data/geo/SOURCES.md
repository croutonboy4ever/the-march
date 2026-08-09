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

## Gaps

None recorded yet.
