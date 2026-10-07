"""Official source identity for GATE 0.

Expected hashes are immutable. Never normalize or substitute them.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Optional


# Immutable expected identity of the official Zenodo artifact
EXPECTED_SHA256 = "5db1246d778eb0be9671ec8f452da806dfdb112edc5eb73fa381a8d042fc10ed"
EXPECTED_MD5 = "e94db2bbd67eaca888aa21b17680b9e1"
OFFICIAL_SOURCE_URL = "https://zenodo.org/records/6941662/files/Sentinel2LULC_CSV.zip"
OFFICIAL_FILENAME = "Sentinel2LULC_CSV.zip"
SOURCE_PROVIDER = "zenodo"
SOURCE_RECORD = "6941662"


@dataclass(frozen=True)
class SourceIdentity:
    """Physical identity of the official source ZIP."""

    source_url: str
    source_provider: str
    source_record: str
    filename: str
    expected_sha256: str
    expected_md5: str
    computed_sha256: Optional[str] = None
    computed_md5: Optional[str] = None
    file_size_bytes: Optional[int] = None

    @property
    def sha256_match(self) -> bool:
        if self.computed_sha256 is None:
            return False
        return self.computed_sha256 == self.expected_sha256

    @property
    def md5_match(self) -> bool:
        if self.computed_md5 is None:
            return False
        return self.computed_md5 == self.expected_md5

    @property
    def identity_valid(self) -> bool:
        return self.sha256_match and self.md5_match

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["sha256_match"] = self.sha256_match
        d["md5_match"] = self.md5_match
        d["identity_valid"] = self.identity_valid
        return d


def official_source_identity(
    computed_sha256: Optional[str] = None,
    computed_md5: Optional[str] = None,
    file_size_bytes: Optional[int] = None,
) -> SourceIdentity:
    """Build SourceIdentity for the official Zenodo artifact."""
    return SourceIdentity(
        source_url=OFFICIAL_SOURCE_URL,
        source_provider=SOURCE_PROVIDER,
        source_record=SOURCE_RECORD,
        filename=OFFICIAL_FILENAME,
        expected_sha256=EXPECTED_SHA256,
        expected_md5=EXPECTED_MD5,
        computed_sha256=computed_sha256,
        computed_md5=computed_md5,
        file_size_bytes=file_size_bytes,
    )


def verify_hashes(computed_sha256: str, computed_md5: str) -> dict[str, bool]:
    """Compare computed hashes against expected official identity."""
    return {
        "sha256_match": computed_sha256 == EXPECTED_SHA256,
        "md5_match": computed_md5 == EXPECTED_MD5,
        "identity_valid": (
            computed_sha256 == EXPECTED_SHA256 and computed_md5 == EXPECTED_MD5
        ),
    }
