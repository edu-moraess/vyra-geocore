# DATA GOVERNANCE — VYRA GEOCORE

## 1. Never Fabricate

The following are strictly forbidden:

- Inventing images, labels, coordinates, STAC items, bands, API results, metrics or availability.
- Using synthetic fallbacks to mask missing real data.
- Marking a gate `PASS` when a mandatory condition was not executed.

If an external source is unavailable → status = `BLOCKED`.

## 2. Provenance Requirements

Every significant artifact must answer:

| Question | Field |
|----------|-------|
| What was the source? | `source` |
| Which version? | `source_version` |
| Which URL? | `source_url` |
| When retrieved? | `retrieval_timestamp` |
| File size? | `file_size` |
| MD5? | `md5` |
| SHA256? | `sha256` |
| Schema? | `schema` |
| Processing version? | `processing_version` |
| Configuration hash? | `configuration_hash` |
| Code commit? | `code_commit` |
| Semantic fingerprint? | `semantic_fingerprint` |
| Which gate? | `gate` |
| When created? | `created_at` |

See `vyra_geocore.provenance.ProvenanceRecord`.

## 3. Identity Layers

| Layer | Definition |
|-------|------------|
| **File identity** | SHA256 of the physical bytes on disk |
| **Semantic identity** | Order-independent fingerprint of logical content |

Semantic algorithm:

1. Compute a row-level SHA256 for every record.
2. Sort the list of row fingerprints lexicographically.
3. Concatenate and SHA256 again.

This distinguishes “same content, different serialization” from “different content”.

## 4. Legacy References

Historical hashes (B7 SHA, previous physical SHA, previous semantic fingerprint) are stored as `legacy_reference` only.

They **must never** be used as automatic PASS criteria.
If a new implementation does not reproduce a legacy hash → record `legacy_sha_status = UNRESOLVED` and establish a new deterministic identity.

## 5. Canonical vs Auxiliary

The official ZIP historically contains 36 CSVs:

- **29 canonical** CSVs → form the dataset universe.
- **7 auxiliary** CSVs (filename contains `_including_non_downloaded_images`) → must not enter the canonical universe automatically.

## 6. Status Vocabulary

| Status | Meaning |
|--------|---------|
| `PASS` | All mandatory conditions executed and satisfied |
| `FAIL` | Executed but failed validation |
| `BLOCKED` | External dependency unavailable or precondition missing |
| `NOT_EXECUTED` | Stage has not run |
| `WARNING` | Non-fatal anomaly; does not block by itself |

## 7. Audit Before Execution

No heavy stage may run before the previous gate has status `PASS`.
The pipeline stops on `FAIL` or `BLOCKED`.
