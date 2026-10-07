"""Foundation tests — version and package importability."""

from vyra_geocore import __version__, __phase__, __status__


def test_version_is_semver():
    assert __version__ == "0.1.0"


def test_phase_is_phase_0():
    assert __phase__ == "PHASE_0"


def test_status_is_foundation():
    assert __status__ == "FOUNDATION"
