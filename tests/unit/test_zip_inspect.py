"""Unit tests for ZIP inspection (uses synthetic in-memory ZIP, not the official source)."""

import zipfile
from pathlib import Path

from vyra_geocore.ingestion.zip_inspect import AUXILIARY_MARKER, inspect_zip


def _make_zip(tmp_path: Path, members: dict[str, bytes]) -> Path:
    path = tmp_path / "test.zip"
    with zipfile.ZipFile(path, "w") as zf:
        for name, data in members.items():
            zf.writestr(name, data)
    return path


def test_inspect_valid_zip_classifies_candidates(tmp_path: Path):
    path = _make_zip(
        tmp_path,
        {
            "1_BarrenLands___CSV.csv": b"a,b\n1,2\n",
            "2_MossAndLichen_CSV.csv": b"a,b\n3,4\n",
            "1_BarrenLands___CSV_including_non_downloaded_images.csv": b"x\n",
        },
    )
    result = inspect_zip(path)
    assert result["zip_valid"] is True
    assert result["csv_count"] == 3
    assert result["canonical_csv_candidates"] == 2
    assert result["auxiliary_csv_candidates"] == 1
    assert any(AUXILIARY_MARKER in n for n in result["auxiliary_candidates"])


def test_inspect_invalid_path():
    result = inspect_zip(Path("/nonexistent/path/file.zip"))
    assert result["zip_valid"] is False
    assert result["error"] is not None
