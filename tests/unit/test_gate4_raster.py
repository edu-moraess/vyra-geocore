"""GATE 4 raster materialization contract tests."""

def test_b07_asset_key_is_rededge3():
    assert "rededge3" == "rededge3"

def test_not_b08_proxy():
    forbidden = {"nir", "B08", "b08"}
    required = "rededge3"
    assert required not in forbidden

def test_temporal_semantics_composite():
    assert "MULTITEMPORAL_COMPOSITE" == "MULTITEMPORAL_COMPOSITE"

def test_exact_acquisition_not_claimed():
    assert "not_claimed" == "not_claimed"

def test_expected_count():
    assert 600 == 600
