"""Unit tests for fingerprint subsystem."""

from vyra_geocore.fingerprints import (
    row_fingerprint,
    semantic_fingerprint,
    sha256_bytes,
)


def test_sha256_bytes_deterministic():
    data = b"vyra-geocore"
    assert sha256_bytes(data) == sha256_bytes(data)
    assert len(sha256_bytes(data)) == 64


def test_row_fingerprint_stable():
    fields = ["1", "BarrenLands__", "img_001", "0.95"]
    fp1 = row_fingerprint(fields)
    fp2 = row_fingerprint(fields)
    assert fp1 == fp2
    assert len(fp1) == 64


def test_semantic_fingerprint_order_independent():
    rows_a = ["aaa", "bbb", "ccc"]
    rows_b = ["ccc", "aaa", "bbb"]
    assert semantic_fingerprint(rows_a) == semantic_fingerprint(rows_b)


def test_semantic_fingerprint_different_content():
    rows_a = ["aaa", "bbb"]
    rows_b = ["aaa", "zzz"]
    assert semantic_fingerprint(rows_a) != semantic_fingerprint(rows_b)
