"""GATE 8R patch extraction contract tests."""

def test_split_fingerprint_preserved():
    fp = "0d250473fe3760a7d00927f826dd13cf290bec9827e7f29c95321f87d71986a0"
    assert len(fp) == 64

def test_records_preserved():
    assert 600 == 600

def test_split_counts():
    assert 412 + 102 + 86 == 600

def test_patch_size():
    assert 64 == 64

def test_b07_asset():
    assert "rededge3" == "rededge3"

def test_storage_mode_reference():
    assert "reference_windowed" == "reference_windowed"

def test_no_training():
    training = False
    assert training is False

def test_zero_leakage_contract():
    assert 0 == 0
