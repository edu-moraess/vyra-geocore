# VYRA GEOCORE — Mission Control

Read-only geospatial intelligence interface built from the previous GEOCORE visual language and the frozen VYRA GEOCORE GATE artifacts.

## Views

- **Mission Control** — pipeline state, dataset telemetry and frozen-model metrics.
- **GEOINT Map** — 600 real geographic records with class, split and patch-status filters.
- **Dataset** — class distribution, split composition and patch counts.
- **Training** — validation/test metrics and learning curves when the heavy history artifact is present.
- **Evaluation** — official GATE 8 test metrics and optional confusion matrix.
- **Model Registry** — frozen SmallCNN identity, experiment fingerprint and checkpoint SHA256.
- **Provenance** — GATE chain and immutable experiment identities.

## Model policy

The GATE 8 SmallCNN baseline is a trained, frozen artifact. The UI does not retrain it, change it, or manufacture predictions. The heavy model checkpoint remains in Drive/object storage; GitHub keeps its identity and provenance.

## Geospatial policy

Coordinates come only from the official GEOINT index. Raster previews use windowed reads when the source is available. Prediction maps and error geography remain explicitly unavailable until real georeferenced predictions are persisted.

## Run

Install the application dependencies:

    pip install -r app/streamlit/requirements.txt

Then:

    export GEOCORE_ARTIFACT_ROOT=$(pwd)
    streamlit run app/streamlit/app.py
