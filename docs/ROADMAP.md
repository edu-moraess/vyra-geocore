# ROADMAP — VYRA GEOCORE

## Phase 0 — Foundation (current)

- Repository creation
- Layered architecture
- Provenance & fingerprint subsystems
- Checkpoint / manifest / audit scaffolding
- Documentation
- Minimal tests
- Recovery script
- Checkpoint `PHASE_0_INIT_PASS`

## Phase 1 — GATE 0  Official Source Recovery

- Download Zenodo ZIP
- Validate MD5 / SHA256
- Write provenance + checkpoint

## Phase 2 — GATE 1  Dataset Universe Identity

- Extract & identify 29 canonical CSVs
- Enforce canonical schema
- Compute semantic fingerprint
- Validate 194 877 rows × 29 classes

## Phase 3 — GATE 2  Deterministic B7

- Reconstruct 600-sample set with seed 17082026
- Document legacy SHA status
- Establish new deterministic identity if needed

## Phase 4 — GATE 3  STAC Reconciliation

- Query earth-search for each B7 coordinate
- Deterministic ranking
- Persist STAC items + provenance

## Phase 5 — GATE 4  Raster Materialization

- Download B2/B3/B4/B8 assets
- Extract 224×224 patches
- Preserve CRS / transform / nodata / dtype

## Phase 6 — GATE 5–7  Integrity · Split Preflight · Split

- Integrity checks
- Geographic / temporal leakage analysis
- Deterministic train/val/test split

## Phase 7 — GATE 8  Training

- Baseline model only after all prior gates PASS
- Architecture open to CNN / ViT / foundation models later

## Phase 8+ — GeoAI Evolution

- Representation learning
- Scene understanding
- Change detection
- Temporal reasoning
- Geospatial intelligence products
