# REPRODUCIBILITY & RECOVERY — VYRA GEOCORE

## 1. Goals

- Survive loss of Colab session, local disk or Python environment.
- Reconstruct any prior valid state from GitHub + object storage alone.
- Never treat an old artifact as valid merely because it once existed.

## 2. Recovery Sequence

```
1. git clone https://github.com/edu-moraess/vyra-geocore.git
2. cd vyra-geocore
3. pip install -e ".[dev]"
4. python scripts/recover_from_checkpoint.py
5. Inspect checkpoints/ and manifests/
6. Locate heavy artifacts via manifest paths
7. Verify SHA256
8. Resume at next_gate
```

## 3. Checkpoint Rules

- Written under `checkpoints/`.
- Immutable: never silently overwritten.
- Name collision → timestamped sibling is created.
- Must contain at minimum: `name`, `status`, `timestamp_utc`, `processing_version`.
- Should contain: `git_commit`, `config_hash`, `artifacts`, `next_gate`, provenance.

## 4. Determinism Requirements

| Element | Requirement |
|---------|-------------|
| Sampling (B7) | Explicit seed (`17082026`) |
| STAC ranking | Lexicographic stable order |
| Fingerprints | Order-independent semantic algorithm |
| Configs | Versioned YAML, hashed |

## 5. Hash Verification

Before any artifact is accepted as input to a later gate:

```
expected_sha256 (from manifest/checkpoint)
    ==
actual_sha256 (computed on the recovered file)
```

Mismatch → `FAIL` or `BLOCKED`. Never proceed.

## 6. Clean-Environment Test

After every phase commit the following must succeed:

```bash
rm -rf /tmp/vyra-geocore-clean
git clone https://github.com/edu-moraess/vyra-geocore.git /tmp/vyra-geocore-clean
cd /tmp/vyra-geocore-clean
pip install -e ".[dev]"
pytest
python scripts/recover_from_checkpoint.py
```
