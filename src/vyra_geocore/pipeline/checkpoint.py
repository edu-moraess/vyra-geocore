"""Checkpoint management — immutable, versioned, recoverable."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from vyra_geocore.provenance.models import ProvenanceRecord, utc_now_iso
from vyra_geocore.pipeline.status import Status


class CheckpointError(Exception):
    """Raised when checkpoint operations fail."""


def write_checkpoint(
    name: str,
    status: Status,
    *,
    root: Path,
    gate: Optional[str] = None,
    git_commit: Optional[str] = None,
    git_branch: Optional[str] = None,
    processing_version: str = "0.1.0",
    config_hash: Optional[str] = None,
    artifacts: Optional[list[dict[str, Any]]] = None,
    next_gate: Optional[str] = None,
    provenance: Optional[ProvenanceRecord] = None,
    extra: Optional[dict[str, Any]] = None,
) -> Path:
    """
    Write an immutable checkpoint JSON.

    Checkpoints are never overwritten. If a file with the same name exists,
    a timestamped variant is created.
    """
    checkpoints_dir = root / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)

    payload: dict[str, Any] = {
        "name": name,
        "status": str(status),
        "timestamp_utc": utc_now_iso(),
        "processing_version": processing_version,
    }
    if gate:
        payload["gate"] = gate
    if git_commit:
        payload["git_commit"] = git_commit
    if git_branch:
        payload["git_branch"] = git_branch
    if config_hash:
        payload["config_hash"] = config_hash
    if artifacts:
        payload["artifacts"] = artifacts
    if next_gate:
        payload["next_gate"] = next_gate
    if provenance:
        payload["provenance"] = provenance.to_dict()
    if extra:
        payload["extra"] = extra

    target = checkpoints_dir / f"{name}.json"
    if target.exists():
        ts = utc_now_iso().replace(":", "").replace("-", "")
        target = checkpoints_dir / f"{name}_{ts}.json"

    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def read_checkpoint(path: Path) -> dict[str, Any]:
    """Load a checkpoint file."""
    if not path.exists():
        raise CheckpointError(f"Checkpoint not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def latest_checkpoint(root: Path, prefix: str) -> Optional[Path]:
    """Return the most recent checkpoint matching a name prefix."""
    checkpoints_dir = root / "checkpoints"
    if not checkpoints_dir.exists():
        return None
    matches = sorted(checkpoints_dir.glob(f"{prefix}*.json"), reverse=True)
    return matches[0] if matches else None
