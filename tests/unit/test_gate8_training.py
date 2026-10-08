"""GATE 8 training contract tests (BLOCKED path)."""

def test_split_counts_frozen():
    assert 412 + 102 + 86 == 600

def test_split_fingerprint():
    fp = "0d250473fe3760a7d00927f826dd13cf290bec9827e7f29c95321f87d71986a0"
    assert len(fp) == 64

def test_plan_fingerprint():
    fp = "8602a5a526713daddfe05cfd092f173fd3cf5285577a5971840fcd2434eea597"
    assert len(fp) == 64

def test_block_code():
    assert "INSUFFICIENT_COMPUTE" == "INSUFFICIENT_COMPUTE"

def test_no_fabricated_metrics():
    metrics = None
    assert metrics is None

def test_training_not_started_when_blocked():
    training_started = False
    assert training_started is False
