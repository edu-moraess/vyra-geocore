"""Unit tests for GATE 3 STAC matching contracts."""

from vyra_geocore.stac import (
    MATCH_STATUSES,
    REQUIRED_ASSETS,
    STAC_COLLECTION,
    STAC_ENDPOINT,
    TEMPORAL_WINDOW,
)
from vyra_geocore.stac.matching import CLOUD_COVER_MAX, RANKING, WARNING_REASON_COMPOSITE


def test_stac_endpoint():
    assert "earth-search.aws.element84.com" in STAC_ENDPOINT


def test_collection_is_l2a():
    assert STAC_COLLECTION == "sentinel-2-l2a"


def test_temporal_window_matches_dataset():
    assert "2015-06-01" in TEMPORAL_WINDOW
    assert "2020-10-31" in TEMPORAL_WINDOW


def test_required_assets_four_bands():
    assert set(REQUIRED_ASSETS) == {"blue", "green", "red", "nir"}


def test_match_statuses_complete():
    for s in ("MATCHED_UNIQUE", "MATCHED_WITH_WARNING", "AMBIGUOUS", "NOT_FOUND", "INVALID_INPUT"):
        assert s in MATCH_STATUSES


def test_ranking_deterministic():
    assert RANKING[0][0] == "properties.eo:cloud_cover"
    assert RANKING[1][0] == "properties.datetime"
    assert RANKING[2][0] == "id"


def test_cloud_cover_max():
    assert CLOUD_COVER_MAX == 20


def test_composite_warning_documented():
    assert "composite" in WARNING_REASON_COMPOSITE
