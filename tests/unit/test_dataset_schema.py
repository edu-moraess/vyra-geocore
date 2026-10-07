"""Unit tests for GATE 1 schema and classification."""

from vyra_geocore.datasets import (
    AUXILIARY_MARKER,
    CANONICAL_COLUMNS,
    EXPECTED_CLASSES,
    EXPECTED_CLASS_NAMES,
    EXPECTED_ROWS,
    SOURCE_TO_CANONICAL,
    classify_csv,
    clean_header,
)


def test_canonical_columns_count():
    assert len(CANONICAL_COLUMNS) == 12


def test_expected_universe_constants():
    assert EXPECTED_ROWS == 194877
    assert EXPECTED_CLASSES == 29
    assert len(EXPECTED_CLASS_NAMES) == 29


def test_source_to_canonical_covers_all():
    assert set(SOURCE_TO_CANONICAL.values()) == set(CANONICAL_COLUMNS)


def test_clean_header_strips_bom():
    assert clean_header("\ufeffLand Cover Class ID") == "Land Cover Class ID"
    assert clean_header("  Latitude  ") == "Latitude"
    assert clean_header(None) is None


def test_classify_canonical():
    cols = list(SOURCE_TO_CANONICAL.keys())
    status, reason = classify_csv("1_BarrenLands___CSV.csv", cols)
    assert status == "CANONICAL"


def test_classify_auxiliary():
    cols = list(SOURCE_TO_CANONICAL.keys())
    name = f"1_BarrenLands___CSV{AUXILIARY_MARKER}.csv"
    status, reason = classify_csv(name, cols)
    assert status == "AUXILIARY"


def test_classify_unknown_missing_column():
    cols = ["Land Cover Class ID", "Latitude"]
    status, _ = classify_csv("weird.csv", cols)
    assert status == "UNKNOWN"
