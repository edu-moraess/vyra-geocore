"""Read-only loaders for GEOCORE gate artifacts.

Never mutates artifacts. Missing files → status UNAVAILABLE, not fabricated values.
"""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any

EXPECTED = {
    "split_fp": "0d250473fe3760a7d00927f826dd13cf290bec9827e7f29c95321f87d71986a0",
    "patch_fp": "e5ad2d547726a22a8a069247946f099be293c7d7f6488924551c927b240b2d72",
    "patch_manifest_sha": "ab4bca827ed71ad6a5366f5d0771d1833fd0264183b16ee2f3785ae56ba817be",
    "exp_fp": "beaecb493ad09e6cb60740447053dffa20c4019e904cb5906c335252b7b1332f",
    "best_sha": "ef56a68ad7362d4bb1604b29c5669ac27851284bd15cb56468a036b1c4d90c2a",
    "last_sha": "d55538c0a6f8b64bc91aa5a39d35744c85b63c52e04c91e978508a64d170a233",
}


def resolve_root(explicit: str | None = None) -> Path:
    import os
    if explicit:
        return Path(explicit)
    env = os.environ.get("GEOCORE_ARTIFACT_ROOT") or os.environ.get("ARTIFACT_ROOT")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent, *here.parents]:
        if (p / "checkpoints").is_dir():
            return p
    return Path.cwd()


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def load_checkpoint(root: Path, name: str) -> dict[str, Any] | None:
    return load_json(root / "checkpoints" / name)


def list_gate_checkpoints(root: Path) -> list[dict[str, Any]]:
    order = [
        ("GATE_0", "GATE_0_OFFICIAL_SOURCE_PASS.json"),
        ("GATE_1", "GATE_1_DATASET_UNIVERSE_PASS.json"),
        ("GATE_2", "GATE_2_DETERMINISTIC_B7_PASS.json"),
        ("GATE_3", "GATE_3_STAC_RECONCILIATION_PASS.json"),
        ("GATE_4", "GATE_4_RASTER_MATERIALIZATION_PASS.json"),
        ("GATE_5", "GATE_5_DATASET_INTEGRITY_PASS.json"),
        ("GATE_6", "GATE_6_SPLIT_PREFLIGHT_PASS.json"),
        ("GATE_7", "GATE_7_DATASET_SPLIT_PASS.json"),
        ("GATE_8R", "GATE_8R_PATCH_EXTRACTION_PASS.json"),
        ("GATE_8", "GATE_8_TRAINING_PASS.json"),
    ]
    out = []
    for gate, fname in order:
        data = load_checkpoint(root, fname)
        if data is None:
            out.append({"gate": gate, "status": "UNAVAILABLE", "file": fname, "data": None})
        else:
            out.append({
                "gate": gate,
                "status": data.get("status", "UNKNOWN"),
                "file": fname,
                "name": data.get("name"),
                "data": data,
            })
    return out


def load_training_history(root: Path) -> list[dict[str, Any]] | None:
    candidates = [
        root / "artifacts" / "gate8" / "training_history.csv",
        root / "artifacts" / "gate8" / "baseline_001" / "logs" / "training_history.csv",
    ]
    for p in candidates:
        if p.exists():
            with open(p, newline="", encoding="utf-8") as f:
                return list(csv.DictReader(f))
    return None


def load_metrics(root: Path, kind: str) -> dict[str, Any] | None:
    candidates = [root / "artifacts" / "gate8" / f"{kind}.json"]
    for p in candidates:
        data = load_json(p)
        if data is not None:
            return data
    return None


def load_patch_manifest(root: Path, limit: int | None = None) -> tuple[list[dict], str | None, bool]:
    path = root / "datasets" / "b7" / "v1" / "patches" / "patch_manifest.csv"
    if not path.exists():
        return [], None, False
    sha = sha256_file(path)
    match = sha == EXPECTED["patch_manifest_sha"]
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if limit is not None and i >= limit:
                break
            rows.append(row)
    return rows, sha, match


def load_confusion(root: Path) -> dict[str, Any] | None:
    return load_json(root / "artifacts" / "gate8" / "confusion_matrix.json")
