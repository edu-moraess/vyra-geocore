"""Unit tests for GATE 1 semantic fingerprint determinism."""

from vyra_geocore.datasets import (
    CANONICAL_COLUMNS,
    row_fingerprint,
    semantic_fingerprint,
)


def _rec(**kwargs):
    base = {c: "" for c in CANONICAL_COLUMNS}
    base.update(kwargs)
    return base


def test_row_fingerprint_stable():
    r = _rec(class_id="1", class_short_name="BarrenLands__", image_id="42",
             latitude="-10.0", longitude="20.0")
    assert row_fingerprint(r) == row_fingerprint(r)
    assert len(row_fingerprint(r)) == 64


def test_row_fingerprint_sensitive_to_content():
    a = _rec(class_id="1", image_id="1")
    b = _rec(class_id="1", image_id="2")
    assert row_fingerprint(a) != row_fingerprint(b)


def test_semantic_fingerprint_order_independent():
    rows = [
        _rec(class_id="1", image_id="a"),
        _rec(class_id="2", image_id="b"),
        _rec(class_id="3", image_id="c"),
    ]
    assert semantic_fingerprint(rows) == semantic_fingerprint(list(reversed(rows)))


def test_semantic_fingerprint_deterministic():
    rows = [_rec(class_id=str(i), image_id=str(i)) for i in range(10)]
    assert semantic_fingerprint(rows) == semantic_fingerprint(rows)
