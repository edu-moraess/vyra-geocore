# ARCHITECTURE — VYRA GEOCORE

## 1. Design Goals

- Infrastructure, not notebook.
- Strict layered dependency rule.
- Full auditability and recoverability.
- Prepared for GeoAI evolution without rewriting the foundation.

## 2. Layer Diagram

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

**Rule:** a layer may only import from layers below it.

## 3. Package Map (`src/vyra_geocore/`)

| Package | Responsibility |
|---------|----------------|
| `ingestion` | Official source recovery (GATE 0) |
| `catalog` | Artifact catalog & indexing |
| `stac` | STAC client & deterministic ranking (GATE 3) |
| `raster` | Raster materialization, windows, COGs (GATE 4) |
| `geospatial` | CRS, transforms, coordinates |
| `datasets` | Identity, B7, splits |
| `validation` | Schema, integrity, leakage checks |
| `provenance` | Provenance records |
| `fingerprints` | File SHA256 + semantic fingerprints |
| `geoai` | Future model training & inference |
| `pipeline` | Gate orchestration, checkpoints, status |
| `cli` | Progressive command-line interface |

## 4. Dependency Rule

```
cli  →  pipeline  →  (geoai | datasets | validation)
                         ↓
              (raster | stac | geospatial)
                         ↓
              (catalog | provenance | fingerprints)
                         ↓
                      ingestion
```

No upward imports. No circular imports.

## 5. Configuration

All runtime configuration lives under `configs/` (versioned YAML).
Code must never hard-code seeds, expected hashes, class lists or STAC parameters.

## 6. Persistence Boundary

- **GitHub** = logical state (code, manifests, audits, checkpoints, hashes, docs).
- **Object Storage / Drive** = heavy artifacts (rasters, ZIPs, models, shards).

Every heavy artifact must have a corresponding entry in a versioned manifest that records its SHA256 and storage location.

## 7. Checkpoint Contract

Each completed gate (or phase) writes an immutable JSON under `checkpoints/`.
If a name collision would occur, a timestamped sibling is created instead of overwriting.

## 8. Evolution Path

```
Earth Observation
    → Representation Learning
    → Scene Understanding
    → Classification / Segmentation
    → Change Detection
    → Temporal Reasoning
    → Geospatial Intelligence
```

The foundation (provenance, fingerprints, gates, recovery) remains stable across all future capabilities.
