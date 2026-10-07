"""Unit tests for official status vocabulary."""

from vyra_geocore.pipeline import Status


def test_status_values():
    assert Status.PASS.value == "PASS"
    assert Status.FAIL.value == "FAIL"
    assert Status.BLOCKED.value == "BLOCKED"
    assert Status.NOT_EXECUTED.value == "NOT_EXECUTED"
    assert Status.WARNING.value == "WARNING"


def test_status_str():
    assert str(Status.PASS) == "PASS"
