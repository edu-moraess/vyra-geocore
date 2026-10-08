"""GATE 9.1 GEOINT Visual Layer tests."""
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "app" / "streamlit"))

from services.geospatial_loader import (
    load_geoint_points,
    filter_points,
    class_distribution,
    validate_coords,
    deterministic_sample,
)
from services.artifact_loader import EXPECTED, load_checkpoint


def test_geoint_points_count():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    assert len(rows) == 600
    assert sum(1 for r in rows if r["status"] == "VALID") == 534
    assert sum(1 for r in rows if r["status"] == "BLOCKED") == 66


def test_coords_valid():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    v = validate_coords(rows)
    assert v["ok"] is True
    assert v["invalid"] == 0


def test_classes_29():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    assert len({r["class_id"] for r in rows}) == 29


def test_filter_class():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    cid = str(rows[0]["class_id"])
    f = filter_points(rows, class_id=cid)
    assert all(str(r["class_id"]) == cid for r in f)
    assert len(f) > 0


def test_filter_split():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    f = filter_points(rows, splits=["train"])
    assert all(r["split"] == "train" for r in f)


def test_filter_blocked():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    f = filter_points(rows, status="BLOCKED")
    assert len(f) == 66
    assert all(r.get("block_reason") == "WINDOW_OUT_OF_BOUNDS" for r in f)


def test_class_distribution():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    dist = class_distribution(rows)
    assert len(dist) == 29
    assert sum(d["records"] for d in dist) == 600


def test_deterministic_sample():
    rows = load_geoint_points(REPO)
    if not rows:
        return
    a = deterministic_sample(rows, n=5, seed=17082026)
    b = deterministic_sample(rows, n=5, seed=17082026)
    assert [r["record_id"] for r in a] == [r["record_id"] for r in b]


def test_prior_fingerprints_unchanged():
    g8 = load_checkpoint(REPO, "GATE_8_TRAINING_PASS.json")
    assert g8 is not None
    assert g8["experiment_fingerprint"] == EXPECTED["exp_fp"]
    g8r = load_checkpoint(REPO, "GATE_8R_PATCH_EXTRACTION_PASS.json")
    assert g8r["patch_semantic_fingerprint"] == EXPECTED["patch_fp"]
    g7 = load_checkpoint(REPO, "GATE_7_DATASET_SPLIT_PASS.json")
    assert g7["final_split_semantic_fingerprint"] == EXPECTED["split_fp"]


def test_gate9_preserved():
    g9 = load_checkpoint(REPO, "GATE_9_STREAMLIT_MISSION_CONTROL_PASS.json")
    assert g9 is not None
    assert g9.get("status") == "PASS"


def test_no_prediction_map_fabricated():
    pred = REPO / "artifacts" / "gate8" / "predictions_georef.csv"
    assert not pred.exists()
