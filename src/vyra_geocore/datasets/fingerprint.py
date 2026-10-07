"""Semantic fingerprint for the dataset universe (order-independent)."""

from __future__ import annotations

import hashlib
from typing import Iterable, Mapping, Sequence

from vyra_geocore.datasets.schema import CANONICAL_COLUMNS


def row_fingerprint(record: Mapping[str, str]) -> str:
    """SHA256 of canonical fields joined by '|' in fixed schema order."""
    parts = [str(record.get(c, "")) for c in CANONICAL_COLUMNS]
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()


def semantic_fingerprint_from_row_fps(row_fps: Iterable[str]) -> str:
    """
    Universe semantic fingerprint.

    Algorithm:
      1. Collect row-level SHA256 fingerprints.
      2. Sort lexicographically.
      3. Join with newline.
      4. SHA256 the result.
    """
    sorted_fps = sorted(row_fps)
    joined = "\n".join(sorted_fps).encode("utf-8")
    return hashlib.sha256(joined).hexdigest()


def semantic_fingerprint(records: Sequence[Mapping[str, str]]) -> str:
    """Compute semantic fingerprint from a sequence of canonical records."""
    return semantic_fingerprint_from_row_fps(row_fingerprint(r) for r in records)
