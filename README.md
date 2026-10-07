# VYRA GEOCORE

**Geospatial Computing & Intelligence**

> Build a geospatial computing infrastructure capable of transforming Earth Observation data into structured, analyzable information that can eventually be consumed by autonomous intelligent systems.

Part of the **VYRA** ecosystem · **ArqTech Labs**

---

## 1. What is GEOCORE?

VYRA GEOCORE is **not** a satellite-image dashboard.

It is an engineering platform for:

- Earth Observation
- Geospatial Processing
- Dataset Engineering
- Remote Sensing
- GeoAI
- Geospatial Intelligence

Long-term evolution path:

```
Satellite Data
    → Geospatial Processing
    → Dataset Engineering
    → GeoAI
    → Intelligence
```

Future integration path:

```
Satellite → GEOCORE → VYRA Intelligence → Perception → Robotics / Autonomous Systems
```

---

## 2. Architecture (layered)

```
CLI / Orchestration
        ↓
Pipeline / Gates
        ↓
GeoAI / Dataset / Validation
        ↓
Raster / STAC / Geospatial
        ↓
Catalog / Provenance / Fingerprints
        ↓
Ingestion
```

Lower layers never depend on upper layers. Circular imports are forbidden.

---

## 3. Data Sources

Primary official source (Phase 1+):

| Field | Value |
|-------|-------|
| Dataset | Sentinel2GlobalLULC |
| URL | https://zenodo.org/records/6941662/files/Sentinel2LULC_CSV.zip |
| Expected MD5 | `e94db2bbd67eaca888aa21b17680b9e1` |
| Expected SHA256 | `5db1246d778eb0be9671ec8f452da806dfdb112edc5eb73fa381a8d042fc10ed` |
| Universe | 194 877 rows · 29 classes |

---

## 4. Core Principles

1. **Never fabricate data** — if a source is unavailable → `BLOCKED`, never synthetic success.
2. **Auditability** — every transformation is traceable.
3. **Reproducibility** — valid datasets must be reproducible.
4. **Provenance** — every artifact carries identity (source, hashes, schema, config, commit).
5. **Audit before execution** — no heavy stage runs before the previous gate passes.
6. **Recovery-first** — survive Colab session loss via GitHub + Drive + checkpoints.

Official statuses: `PASS` · `FAIL` · `BLOCKED` · `NOT_EXECUTED` · `WARNING`

---

## 5. Gate Pipeline

```
GATE 0  Official Source Recovery
GATE 1  Dataset Universe Identity
GATE 2  Deterministic B7
GATE 3  STAC Reconciliation
GATE 4  Raster Materialization
GATE 5  Dataset Integrity
GATE 6  Split Preflight
GATE 7  Dataset Split
GATE 8  Training
```

No gate may be skipped. Training is forbidden until all prior data gates pass.

---

## 6. Persistence Model

| Artifact type | Source of truth |
|---------------|-----------------|
| Code, schemas, configs, manifests, audits, checkpoints, hashes, docs | **GitHub** |
| Large datasets, rasters, COGs, models, shards | **Object Storage / Google Drive** |

---

## 7. Recovery Protocol

If the Colab session dies:

```
1. git clone https://github.com/edu-moraess/vyra-geocore.git
2. mount Drive / locate object storage
3. read latest checkpoint + manifest
4. verify SHA256 of referenced artifacts
5. resume from next_gate
```

See `scripts/recover_from_checkpoint.py` and `docs/REPRODUCIBILITY.md`.

---

## 8. Current Phase

**PHASE 0 — FOUNDATION** (this repository bootstrap)

No dataset download, STAC, raster or training has been executed yet.

Next gate: **GATE 0 — Official Source Recovery**

---

## 9. How to install (development)

```bash
git clone https://github.com/edu-moraess/vyra-geocore.git
cd vyra-geocore
pip install -e ".[dev]"
pytest
```

---

## 10. Documentation

| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Layered architecture & dependency rules |
| [DATA_GOVERNANCE.md](docs/DATA_GOVERNANCE.md) | Provenance, identity, never-fabricate policy |
| [DATASET_CONTRACT.md](docs/DATASET_CONTRACT.md) | Canonical schema, classes, B7 contract |
| [REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md) | Seeds, fingerprints, recovery |
| [ROADMAP.md](docs/ROADMAP.md) | Phased delivery plan |
| [processing-pipeline.md](docs/processing-pipeline.md) | Gate definitions |

---

## License

Apache-2.0 · Copyright 2026 ArqTech Labs / VYRA
