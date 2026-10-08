"""GATE 9 Mission Control contract tests."""
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "app" / "streamlit"))

from services.artifact_loader import (
    EXPECTED,
    resolve_root,
    list_gate_checkpoints,
    load_checkpoint,
    load_training_history,
    load_metrics,
    load_patch_manifest,
)
from services.gate_status import pipeline_overview, validate_frozen_identities


def test_resolve_root():
    root = resolve_root(str(REPO))
    assert (root / "checkpoints").is_dir()


def test_gate_checkpoints_discoverable():
    items = list_gate_checkpoints(REPO)
    assert len(items) >= 8
    names = {i["gate"] for i in items}
    assert "GATE_7" in names
    assert "GATE_8R" in names


def test_gate8_training_checkpoint():
    data = load_checkpoint(REPO, "GATE_8_TRAINING_PASS.json")
    assert data is not None
    assert data.get("status") == "PASS"
    assert data.get("experiment_fingerprint") == EXPECTED["exp_fp"]


def test_gate8r_patch_fingerprint():
    data = load_checkpoint(REPO, "GATE_8R_PATCH_EXTRACTION_PASS.json")
    assert data is not None
    assert data.get("patch_semantic_fingerprint") == EXPECTED["patch_fp"]


def test_gate7_split_fingerprint():
    data = load_checkpoint(REPO, "GATE_7_DATASET_SPLIT_PASS.json")
    assert data is not None
    fp = data.get("final_split_semantic_fingerprint")
    assert fp == EXPECTED["split_fp"]


def test_patch_manifest_hash_if_present():
    rows, sha, match = load_patch_manifest(REPO, limit=5)
    if sha is not None:
        assert match is True
        assert len(rows) <= 5


def test_training_history_numeric():
    hist = load_training_history(REPO)
    if hist is None:
        return
    for row in hist:
        float(row["train_loss"])
        float(row["val_loss"])


def test_metrics_no_nan_keys():
    tm = load_metrics(REPO, "test_metrics")
    if tm is None:
        return
    for k in ["loss", "accuracy", "macro_f1"]:
        assert k in tm
        assert tm[k] == tm[k]


def test_pipeline_overview_statuses():
    rows = pipeline_overview(REPO)
    assert any(r["gate"] == "GATE_8" for r in rows)


def test_frozen_identity_validation():
    res = validate_frozen_identities(REPO)
    assert "exp_fp" in res
    assert "patch_fp" in res


def test_no_mutation_of_expected_constants():
    assert EXPECTED["best_sha"].startswith("ef56a68a")
    assert len(EXPECTED["patch_fp"]) == 64
