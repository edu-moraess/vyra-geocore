"""Derive pipeline status from official checkpoints."""
from __future__ import annotations

from typing import Any

from .artifact_loader import list_gate_checkpoints, EXPECTED, load_checkpoint


GATE_LABELS = {
    "GATE_0": "SOURCE",
    "GATE_1": "DATASET IDENTITY",
    "GATE_2": "B7",
    "GATE_3": "STAC",
    "GATE_4": "RASTER",
    "GATE_5": "INTEGRITY",
    "GATE_6": "SPLIT PREFLIGHT",
    "GATE_7": "SPLIT",
    "GATE_8R": "PATCH ENGINE",
    "GATE_8": "TRAINING",
}


def pipeline_overview(root) -> list[dict[str, Any]]:
    rows = []
    for item in list_gate_checkpoints(root):
        data = item.get("data") or {}
        fp = (
            data.get("experiment_fingerprint")
            or data.get("patch_semantic_fingerprint")
            or data.get("final_split_semantic_fingerprint")
            or data.get("plan_fingerprint")
            or data.get("audit_semantic_fingerprint")
            or data.get("b7_fingerprint")
            or ""
        )
        rows.append({
            "gate": item["gate"],
            "label": GATE_LABELS.get(item["gate"], item["gate"]),
            "status": item["status"],
            "checkpoint": data.get("name") or item["file"],
            "fingerprint": fp[:16] + "…" if len(fp) > 16 else fp,
            "fingerprint_full": fp,
        })
    return rows


def validate_frozen_identities(root) -> dict[str, Any]:
    results = {}
    g7 = load_checkpoint(root, "GATE_7_DATASET_SPLIT_PASS.json")
    if g7:
        fp = g7.get("final_split_semantic_fingerprint", "")
        results["split_fp"] = {
            "expected": EXPECTED["split_fp"],
            "found": fp,
            "match": fp == EXPECTED["split_fp"] if fp else False,
        }
    else:
        results["split_fp"] = {"expected": EXPECTED["split_fp"], "found": None, "match": False}

    g8r = load_checkpoint(root, "GATE_8R_PATCH_EXTRACTION_PASS.json")
    if g8r:
        fp = g8r.get("patch_semantic_fingerprint", "")
        results["patch_fp"] = {
            "expected": EXPECTED["patch_fp"],
            "found": fp,
            "match": fp == EXPECTED["patch_fp"],
        }
    else:
        results["patch_fp"] = {"expected": EXPECTED["patch_fp"], "found": None, "match": False}

    g8 = load_checkpoint(root, "GATE_8_TRAINING_PASS.json")
    if g8:
        fp = g8.get("experiment_fingerprint", "")
        results["exp_fp"] = {
            "expected": EXPECTED["exp_fp"],
            "found": fp,
            "match": fp == EXPECTED["exp_fp"],
        }
        results["best_sha"] = {
            "expected": EXPECTED["best_sha"],
            "found": g8.get("best_checkpoint_sha256"),
            "match": g8.get("best_checkpoint_sha256") == EXPECTED["best_sha"],
        }
    else:
        results["exp_fp"] = {"expected": EXPECTED["exp_fp"], "found": None, "match": False}
        results["best_sha"] = {"expected": EXPECTED["best_sha"], "found": None, "match": False}
    return results
