"""STAC matching constants and helpers for GATE 3."""

from __future__ import annotations

STAC_ENDPOINT = "https://earth-search.aws.element84.com/v1/search"
STAC_API_ROOT = "https://earth-search.aws.element84.com/v1"
STAC_COLLECTION = "sentinel-2-l2a"
TEMPORAL_WINDOW = "2015-06-01T00:00:00Z/2020-10-31T23:59:59Z"
CLOUD_COVER_MAX = 20

# Element84 asset names corresponding to B2, B3, B4, B8
REQUIRED_ASSETS = ("blue", "green", "red", "nir")

MATCH_STATUSES = (
    "MATCHED_UNIQUE",
    "MATCHED_WITH_WARNING",
    "AMBIGUOUS",
    "NOT_FOUND",
    "INVALID_INPUT",
)

RANKING = (
    ("properties.eo:cloud_cover", "asc"),
    ("properties.datetime", "asc"),
    ("id", "asc"),
)

WARNING_REASON_COMPOSITE = (
    "source_is_multi_temporal_composite; selected_lowest_cloud_earliest_datetime"
)
