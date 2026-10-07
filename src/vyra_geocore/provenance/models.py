"""Provenance data models.

Every significant artifact must carry a provenance block that answers:
- What was the source?
- Which version?
- Which file?
- Which SHA256?
- Which schema?
- Which configuration?
- Which code version / commit?
- Which fingerprint?
- Which timestamp?
- Which gate produced the artifact?
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional
import json


def utc_now_iso() -> str:
    """Return current UTC timestamp in ISO-8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class ProvenanceRecord:
    """Immutable provenance record for an artifact."""

    source: str
    source_version: Optional[str] = None
    source_url: Optional[str] = None
    retrieval_timestamp: Optional[str] = None
    file_size: Optional[int] = None
    md5: Optional[str] = None
    sha256: Optional[str] = None
    schema: Optional[str] = None
    processing_version: Optional[str] = None
    configuration_hash: Optional[str] = None
    code_commit: Optional[str] = None
    semantic_fingerprint: Optional[str] = None
    gate: Optional[str] = None
    created_at: str = field(default_factory=utc_now_iso)
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        return {k: v for k, v in d.items() if v is not None and v != {}}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, sort_keys=True)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProvenanceRecord":
        known = {f.name for f in cls.__dataclass_fields__.values()}  # type: ignore
        core = {k: v for k, v in data.items() if k in known and k != "extra"}
        extra = {k: v for k, v in data.items() if k not in known}
        if "extra" in data and isinstance(data["extra"], dict):
            extra.update(data["extra"])
        return cls(**core, extra=extra)
