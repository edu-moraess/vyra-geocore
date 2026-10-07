"""Unit tests for checkpoint subsystem."""

import json
from pathlib import Path

from vyra_geocore.pipeline import Status, write_checkpoint, read_checkpoint


def test_write_and_read_checkpoint(tmp_path: Path):
    path = write_checkpoint(
        name="TEST_CKPT",
        status=Status.PASS,
        root=tmp_path,
        gate="GATE_TEST",
        processing_version="0.1.0",
        next_gate="GATE_NEXT",
    )
    assert path.exists()
    data = read_checkpoint(path)
    assert data["name"] == "TEST_CKPT"
    assert data["status"] == "PASS"
    assert data["gate"] == "GATE_TEST"
    assert data["next_gate"] == "GATE_NEXT"
    assert "timestamp_utc" in data


def test_checkpoint_is_immutable(tmp_path: Path):
    p1 = write_checkpoint("IMMUTABLE", Status.PASS, root=tmp_path)
    p2 = write_checkpoint("IMMUTABLE", Status.PASS, root=tmp_path)
    assert p1 != p2
    assert p1.exists() and p2.exists()
