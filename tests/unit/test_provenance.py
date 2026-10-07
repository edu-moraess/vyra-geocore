"""Unit tests for provenance models."""

from vyra_geocore.provenance import ProvenanceRecord, utc_now_iso


def test_provenance_roundtrip():
    rec = ProvenanceRecord(
        source="zenodo:6941662",
        source_url="https://zenodo.org/records/6941662/files/Sentinel2LULC_CSV.zip",
        sha256="5db1246d778eb0be9671ec8f452da806dfdb112edc5eb73fa381a8d042fc10ed",
        md5="e94db2bbd67eaca888aa21b17680b9e1",
        gate="GATE_0",
        processing_version="0.1.0",
    )
    d = rec.to_dict()
    restored = ProvenanceRecord.from_dict(d)
    assert restored.source == rec.source
    assert restored.sha256 == rec.sha256
    assert restored.gate == "GATE_0"


def test_utc_now_iso_format():
    ts = utc_now_iso()
    assert ts.endswith("Z")
    assert "T" in ts
    assert len(ts) == 20
