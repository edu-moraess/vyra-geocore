"""Geospatial presentation loaders. Read-only. Never fabricates coordinates."""
from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Any

SEED = 17082026


def load_geoint_points(root: Path) -> list[dict[str, Any]]:
    path = root / "datasets" / "b7" / "v1" / "geo" / "geoint_points.csv"
    if not path.exists():
        return []
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            try:
                r["latitude"] = float(r["latitude"])
                r["longitude"] = float(r["longitude"])
            except (TypeError, ValueError):
                continue
            rows.append(r)
    return rows


def filter_points(
    rows: list[dict[str, Any]],
    class_id: str | None = None,
    splits: list[str] | None = None,
    status: str | None = None,
) -> list[dict[str, Any]]:
    out = rows
    if class_id and class_id != "ALL":
        out = [r for r in out if str(r.get("class_id")) == str(class_id)]
    if splits:
        allowed = set(splits)
        out = [r for r in out if r.get("split") in allowed]
    if status and status != "ALL":
        out = [r for r in out if r.get("status") == status]
    return out


def class_distribution(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    from collections import defaultdict
    d: dict[str, dict] = defaultdict(lambda: {
        "class_id": "", "class_name": "", "records": 0, "train": 0, "val": 0, "test": 0,
        "valid": 0, "blocked": 0,
    })
    for r in rows:
        cid = str(r["class_id"])
        e = d[cid]
        e["class_id"] = cid
        e["class_name"] = r.get("class_name", "")
        e["records"] += 1
        sp = r.get("split", "")
        if sp in e:
            e[sp] += 1
        if r.get("status") == "VALID":
            e["valid"] += 1
        else:
            e["blocked"] += 1
    return sorted(d.values(), key=lambda x: int(x["class_id"]))


def deterministic_sample(rows: list[dict[str, Any]], n: int = 12, seed: int = SEED) -> list[dict[str, Any]]:
    if not rows:
        return []
    rng = random.Random(seed)
    idx = list(range(len(rows)))
    rng.shuffle(idx)
    return [rows[i] for i in idx[: min(n, len(rows))]]


def validate_coords(rows: list[dict[str, Any]]) -> dict[str, Any]:
    n = len(rows)
    invalid = 0
    for r in rows:
        lat, lon = r.get("latitude"), r.get("longitude")
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            invalid += 1
        elif not (-90 <= lat <= 90 and -180 <= lon <= 180):
            invalid += 1
    return {"n": n, "invalid": invalid, "ok": invalid == 0}
