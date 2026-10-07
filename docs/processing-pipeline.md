# PROCESSING PIPELINE — Gate Definitions

| Gate | Name | Mandatory inputs | Mandatory outputs | PASS criterion |
|------|------|------------------|-------------------|----------------|
| 0 | Official Source Recovery | Zenodo URL + expected hashes | ZIP + provenance | Hashes match & file exists |
| 1 | Dataset Universe Identity | Validated ZIP | Canonical CSV + semantic FP + schema validation | 194877 rows, 29 classes, schema OK |
| 2 | Deterministic B7 | Universe + seed 17082026 | 600-sample set + FP | Correct distribution + reproducible FP |
| 3 | STAC Reconciliation | B7 coordinates | Ranked STAC items | Deterministic item per point |
| 4 | Raster Materialization | STAC items | Patches + provenance | Bands + CRS + nodata preserved |
| 5 | Dataset Integrity | Patches | Integrity report | Zero corruption, completeness |
| 6 | Split Preflight | Dataset + coordinates | Leakage analysis | Geographic/temporal groups identified |
| 7 | Dataset Split | Preflight OK | train/val/test manifests | No detectable leakage |
| 8 | Training | Split PASS | Model checkpoint + metrics | All prior gates PASS |

Any `FAIL` or `BLOCKED` stops the pipeline.  
`NOT_EXECUTED` is an explicit status, never an implicit assumption.
