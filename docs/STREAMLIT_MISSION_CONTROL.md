# Streamlit Mission Control

## Purpose

Read-only observability interface for VYRA GEOCORE. Consumes artifacts from GATEs 0–8R and GATE 8 Training. Does **not** process data, train models, or mutate fingerprints.

## Architecture

```
UI (Streamlit)
  → presentation services (artifact_loader, gate_status)
    → official checkpoints / manifests / metrics on disk
```

## Run locally

```bash
git clone https://github.com/edu-moraess/vyra-geocore.git
cd vyra-geocore
pip install streamlit pandas
export GEOCORE_ARTIFACT_ROOT=$(pwd)
streamlit run app/streamlit/app.py
```

## Artifact policy

| Present | Behavior |
|---------|----------|
| Checkpoint / metric file found | Load and display |
| Missing | Show UNAVAILABLE — never fabricate |

## Pages

MISSION CONTROL · DATASET · PATCH ENGINE · TRAINING · EVALUATION · MODEL REGISTRY · PROVENANCE

## Limitations

- Raster gallery requires reachable COGs; otherwise UNAVAILABLE
- Does not download full scenes
- Does not recompute GATE 8 metrics
