from __future__ import annotations

import json
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[2] / "app" / "streamlit"
sys.path.insert(0, str(APP_ROOT))

from services.artifact_loader import training_summary
from services.geospatial_loader import class_distribution, filter_points, validate_coords


def test_training_summary_reads_gate8_audit(tmp_path: Path) -> None:
    audit_dir = tmp_path / "audits"
    audit_dir.mkdir()
    (audit_dir / "gate8_training.json").write_text(
        json.dumps(
            {
                "hardware": {"device": "cpu", "gpu": None},
                "model": {"architecture": "SmallCNN", "n_params": 25181, "input": "64x64x1", "classes": 29},
                "training": {"actual_epochs": 40, "best_epoch": 25, "early_stopped": True},
                "validation_metrics": {"accuracy": 0.2247},
                "test_metrics": {"accuracy": 0.2174, "macro_f1": 0.1368},
                "experiment_fingerprint": "exp",
                "checkpoints": {"best_sha256": "sha"},
                "warnings": ["LOW_BASELINE_ACCURACY"],
            }
        ),
        encoding="utf-8",
    )

    result = training_summary(tmp_path)

    assert result["available"] is True
    assert result["model"] == "SmallCNN"
    assert result["best_epoch"] == 25
    assert result["test"]["accuracy"] == 0.2174
    assert result["warning"] == "LOW_BASELINE_ACCURACY"


def test_geoint_filters_preserve_real_records() -> None:
    rows = [
        {"class_id": "1", "class_name": "A", "split": "train", "status": "VALID", "latitude": 1.0, "longitude": 2.0},
        {"class_id": "2", "class_name": "B", "split": "test", "status": "BLOCKED", "latitude": 3.0, "longitude": 4.0},
    ]

    assert len(filter_points(rows, class_id="1", splits=["train"], status="VALID")) == 1
    assert len(filter_points(rows, status="BLOCKED")) == 1
    assert validate_coords(rows)["invalid"] == 0
    assert class_distribution(rows)[0]["records"] == 1
