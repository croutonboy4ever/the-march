# The March

An interactive web experience on the Second Punic War. The core of the experience is
Hannibal's march from Iberia across the Rhone and the Alps into Italy, told through
real geography, sourced narrative, and explicit provenance for every claim.

Accuracy conventions are canonical in [docs/conventions-v0.2.md](docs/conventions-v0.2.md):
three provenance markers (attested / inferred / imagined), source disagreement shown as
content, real coordinates and real topography only. Nothing on a map is freehand; every
feature traces to source data.

## Repository structure

```
/site           Static site root. The proof-of-concept map page lives here.
/data/geo       Geographic source data and processing scripts.
  raw/          Raw downloads as pulled (large files kept on disk, gitignored;
                provenance and checksums recorded in SOURCES.md).
  processed/    Extracted / clipped / derived data, committed.
  scripts/      Processing scripts. Every processed file is reproducible by
                running a script against a raw file.
  SOURCES.md    Provenance for every data file: origin URL, date pulled, license.
/data/content   Chapter content, one folder per chapter 00-11. Empty for now.
/docs           Project docs, including the conventions doc.
```

## Site technology choice: plain HTML/CSS/JS

The spike uses a plain static site, no framework and no build step. Reasons:

- The project explicitly wants no framework lock-in yet. Plain files lock nothing in;
  Astro (the other candidate) is easy to adopt later precisely because it consumes
  plain HTML/CSS/JS content, so starting plain keeps that door fully open.
- The proof-of-concept needs exactly one page showing one rendered map. A build
  toolchain adds moving parts and versions to maintain with zero payoff at this stage.
- The heavy lifting (terrain rendering, data clipping) happens in the Python data
  pipeline, not in the browser. The site layer is currently presentation only.

Revisit when chapters exist: at that point content collections, routing, and scroll
orchestration are real needs and Astro (or similar) earns its place. That decision
routes through the decision log per the conventions doc.

## How to run

The site is static; serve the `site/` directory with any file server:

```
python3 -m http.server --directory site 8000
```

then open http://localhost:8000/.

To reproduce the data pipeline (raw downloads onward), see the script headers in
`data/geo/scripts/` and the per-source entries in `data/geo/SOURCES.md`. Python
dependencies for processing: `python3 -m venv .venv && .venv/bin/pip install numpy matplotlib tifffile`
(`tifffile` reads the ESA WorldCover GeoTIFF tiles in `extract_landcover.py`).

## Provenance rule for data

Every file under `data/geo` is either a raw download recorded in SOURCES.md or the
output of a committed script over such a download. No hand-drawn geography, no
hand-edited coordinates. Gaps in the data are recorded in SOURCES.md as gaps, not
papered over.
