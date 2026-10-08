# Streamlit Mission Control

## Purpose

Read-only observability interface for VYRA GEOCORE. Consumes artifacts from GATEs 0–8R and GATE 8 Training. Does **not** process data, train models, or mutate fingerprints.

## Run locally

```bash
git clone https://github.com/edu-moraess/vyra-geocore.git
cd vyra-geocore
pip install streamlit pandas pydeck
# optional for B07 preview: rasterio
export GEOCORE_ARTIFACT_ROOT=$(pwd)
# Place geoint_points.csv under datasets/b7/v1/geo/ (Drive: 1BN7EfGqNgqHapyIbABFmX7tnXEnV2vG5)
streamlit run app/streamlit/app.py
```

## GEOINT Visual Layer (GATE 9.1)

### Pages

- **GEOINT MAP** — pydeck scatter of 600 B7 points (534 valid + 66 blocked)
- **PATCH EXPLORER** — deterministic sample (seed 17082026); optional windowed B07
- **CLASS DISTRIBUTION** — train/val/test/valid/blocked per class

### Filters

CLASS · SPLIT (multi) · PATCH STATUS · color by split or status

### Data

`datasets/b7/v1/geo/geoint_points.csv` — presentation index from GATE 7 + GATE 4 provenance + GATE 8R. Drive file id `1BN7EfGqNgqHapyIbABFmX7tnXEnV2vG5`.

### Unavailable by design

| View | Reason |
|------|--------|
| Prediction map | GATE 8 did not store georef predictions |
| Error geography | same |
| STAC coverage | bboxes not in index |
| Raster preview | requires network COG + rasterio |

### Performance

No mass raster download on startup. Previews are on-demand windowed reads only.

## Artifact policy

Missing files → UNAVAILABLE (never fabricate).
