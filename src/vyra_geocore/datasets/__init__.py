"""Dataset identity and universe construction (GATE 1+)."""

from vyra_geocore.datasets.schema import (
    AUXILIARY_MARKER,
    CANONICAL_COLUMNS,
    EXPECTED_CLASSES,
    EXPECTED_CLASS_NAMES,
    EXPECTED_ROWS,
    LEGACY_SEMANTIC_FINGERPRINT,
    SOURCE_TO_CANONICAL,
    classify_csv,
    clean_header,
)
from vyra_geocore.datasets.fingerprint import (
    row_fingerprint,
    semantic_fingerprint,
    semantic_fingerprint_from_row_fps,
)
from vyra_geocore.datasets.b7 import (
    B7_SEED,
    B7_TOTAL,
    sample_b7,
    target_count,
)

__all__ = [
    "CANONICAL_COLUMNS",
    "SOURCE_TO_CANONICAL",
    "EXPECTED_CLASS_NAMES",
    "EXPECTED_ROWS",
    "EXPECTED_CLASSES",
    "AUXILIARY_MARKER",
    "LEGACY_SEMANTIC_FINGERPRINT",
    "classify_csv",
    "clean_header",
    "row_fingerprint",
    "semantic_fingerprint",
    "semantic_fingerprint_from_row_fps",
    "B7_SEED",
    "B7_TOTAL",
    "sample_b7",
    "target_count",
]
