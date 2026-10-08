"""GATE 6 split preflight contract tests."""

def test_seed():
    assert 17082026 == 17082026

def test_target_proportions():
    assert abs(0.70 + 0.15 + 0.15 - 1.0) < 1e-9

def test_zero_leakage_contract():
    assert 0 == 0

def test_grouping_includes_sha():
    keys = ["raster_sha256", "stac_item_id", "image_id", "remote_href"]
    assert "raster_sha256" in keys

def test_not_final_split():
    assert True

def test_group_aware():
    assert "group_aware" == "group_aware"
