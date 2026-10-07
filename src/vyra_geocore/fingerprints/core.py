"""Fingerprint utilities.

Two identity layers:

1. File identity  — SHA256 of the physical bytes.
2. Semantic identity — content fingerprint independent of row order / serialization.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable, Union


def sha256_bytes(data: bytes) -> str:
    """Compute SHA256 hex digest of raw bytes."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Union[str, Path], chunk_size: int = 1 << 20) -> str:
    """Compute SHA256 of a file using streaming (memory-safe)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def md5_file(path: Union[str, Path], chunk_size: int = 1 << 20) -> str:
    """Compute MD5 of a file using streaming (legacy compatibility only)."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def semantic_fingerprint(row_fingerprints: Iterable[str]) -> str:
    """
    Build a semantic (order-independent) fingerprint.

    Algorithm:
        1. Each row already has its own SHA256 fingerprint.
        2. Sort the list of row fingerprints lexicographically.
        3. Concatenate and hash again with SHA256.

    This distinguishes "same content, different physical file"
    from "different content".
    """
    sorted_fps = sorted(row_fingerprints)
    joined = "\n".join(sorted_fps).encode("utf-8")
    return sha256_bytes(joined)


def row_fingerprint(fields: Iterable[str]) -> str:
    """
    Fingerprint a single logical row.

    Fields are joined with a stable separator and hashed.
    Caller is responsible for canonical string representation of each field.
    """
    payload = "|".join(str(f) for f in fields).encode("utf-8")
    return sha256_bytes(payload)
