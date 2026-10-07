"""Deterministic B7 stratified sampling (GATE 2)."""

from __future__ import annotations

import random
from typing import Mapping, Sequence

B7_SEED = 17082026
B7_TOTAL = 600
B7_DEFAULT_PER_CLASS = 20
B7_SPECIAL_CLASS_ID = 22
B7_SPECIAL_SAMPLES = 40
B7_LEGACY_SHA256 = "bc4dc39cb4fdb891f4cc01db29049d5351040d9c8b78aa0f72dff456d55cdd23"
B7_ORDERING_FIELDS = ("class_id", "image_id", "latitude", "longitude")


def target_count(class_id: int) -> int:
    """Target sample count for a class under the B7 contract."""
    if class_id == B7_SPECIAL_CLASS_ID:
        return B7_SPECIAL_SAMPLES
    return B7_DEFAULT_PER_CLASS


def sample_b7(
    by_class: Mapping[int, Sequence[Mapping[str, str]]],
    seed: int = B7_SEED,
) -> list[dict[str, str]]:
    """
    Stratified sample without replacement.

    Returns records canonically ordered by (class_id, image_id, latitude, longitude).
    """
    rng = random.Random(seed)
    selected: list[dict[str, str]] = []
    for cid in range(1, 30):
        pool = list(by_class[cid])
        target = target_count(cid)
        if len(pool) < target:
            raise ValueError(
                f"class {cid}: available={len(pool)} < target={target}"
            )
        indices = rng.sample(range(len(pool)), target)
        selected.extend(dict(pool[i]) for i in indices)

    selected.sort(
        key=lambda r: (
            int(float(r["class_id"])),
            r["image_id"],
            r["latitude"],
            r["longitude"],
        )
    )
    return selected
