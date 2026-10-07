"""ZIP inspection utilities for GATE 0 (read-only characterization)."""

from __future__ import annotations

import zipfile
from pathlib import Path
from typing import Any


AUXILIARY_MARKER = "_including_non_downloaded_images"


def inspect_zip(path: Path) -> dict[str, Any]:
    """
    Open ZIP, validate integrity, list members.

    Does NOT modify the archive. Classification of canonical vs auxiliary
    is provisional (candidates only) — definitive classification is GATE 1.
    """
    result: dict[str, Any] = {
        "zip_valid": False,
        "testzip_result": None,
        "file_count": 0,
        "csv_count": 0,
        "canonical_csv_candidates": 0,
        "auxiliary_csv_candidates": 0,
        "members": [],
        "canonical_candidates": [],
        "auxiliary_candidates": [],
        "error": None,
    }

    try:
        with zipfile.ZipFile(path, "r") as zf:
            bad = zf.testzip()
            result["testzip_result"] = bad
            result["zip_valid"] = bad is None

            members = []
            for info in zf.infolist():
                members.append(
                    {
                        "filename": info.filename,
                        "file_size": info.file_size,
                        "compress_size": info.compress_size,
                        "is_dir": info.is_dir(),
                    }
                )
            result["members"] = members
            result["file_count"] = len(members)

            csvs = [
                m["filename"]
                for m in members
                if m["filename"].lower().endswith(".csv") and not m["is_dir"]
            ]
            result["csv_count"] = len(csvs)

            auxiliary = [n for n in csvs if AUXILIARY_MARKER in n]
            canonical = [n for n in csvs if AUXILIARY_MARKER not in n]
            result["auxiliary_candidates"] = sorted(auxiliary)
            result["canonical_candidates"] = sorted(canonical)
            result["auxiliary_csv_candidates"] = len(auxiliary)
            result["canonical_csv_candidates"] = len(canonical)
    except Exception as exc:
        result["error"] = str(exc)
        result["zip_valid"] = False

    return result
