"""Unit tests for GATE 0 source identity (no network required)."""

from vyra_geocore.ingestion import (
    EXPECTED_MD5,
    EXPECTED_SHA256,
    OFFICIAL_SOURCE_URL,
    SourceIdentity,
    official_source_identity,
    verify_hashes,
)
from vyra_geocore.pipeline import Status


def test_expected_hashes_are_immutable_constants():
    assert EXPECTED_SHA256 == "5db1246d778eb0be9671ec8f452da806dfdb112edc5eb73fa381a8d042fc10ed"
    assert EXPECTED_MD5 == "e94db2bbd67eaca888aa21b17680b9e1"
    assert OFFICIAL_SOURCE_URL.startswith("https://zenodo.org/")


def test_verify_hashes_match():
    result = verify_hashes(EXPECTED_SHA256, EXPECTED_MD5)
    assert result["sha256_match"] is True
    assert result["md5_match"] is True
    assert result["identity_valid"] is True


def test_verify_hashes_mismatch_sha256():
    result = verify_hashes("0" * 64, EXPECTED_MD5)
    assert result["sha256_match"] is False
    assert result["md5_match"] is True
    assert result["identity_valid"] is False


def test_verify_hashes_mismatch_md5():
    result = verify_hashes(EXPECTED_SHA256, "0" * 32)
    assert result["sha256_match"] is True
    assert result["md5_match"] is False
    assert result["identity_valid"] is False


def test_source_identity_valid_when_hashes_match():
    ident = official_source_identity(
        computed_sha256=EXPECTED_SHA256,
        computed_md5=EXPECTED_MD5,
        file_size_bytes=64542330,
    )
    assert ident.sha256_match is True
    assert ident.md5_match is True
    assert ident.identity_valid is True
    d = ident.to_dict()
    assert d["identity_valid"] is True
    assert d["file_size_bytes"] == 64542330


def test_source_identity_invalid_when_hashes_missing():
    ident = official_source_identity()
    assert ident.sha256_match is False
    assert ident.md5_match is False
    assert ident.identity_valid is False


def test_status_vocabulary_still_intact():
    assert Status.PASS.value == "PASS"
    assert Status.FAIL.value == "FAIL"
    assert Status.BLOCKED.value == "BLOCKED"
