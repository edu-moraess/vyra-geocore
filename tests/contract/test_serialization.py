import json
import math

import pytest

from tests.builders import det, observed, prov, stamp
from vyra.domain.checks import ContractError
from vyra.domain.contracts import SCHEMA_VERSION, SceneSnapshot
from vyra.domain.serialization import to_json_line, to_plain, to_record


def make():
    return SceneSnapshot(stamp(4), (det(0, 4), det(1, 4)), (observed(1, 0, 4),), prov())


def test_record_has_schema_version_and_type():
    rec = to_record(make())
    assert rec["schema_version"] == SCHEMA_VERSION == "0.1.0"
    assert rec["type"] == "SceneSnapshot"


def test_json_line_is_strict_single_line_and_deterministic():
    a, b = to_json_line(make()), to_json_line(make())
    assert a == b and "\n" not in a
    parsed = json.loads(a)
    assert parsed["schema_version"] == "0.1.0"


def test_rejects_nan():
    from vyra.domain.geometry import BBox
    with pytest.raises(ContractError):
        to_plain(BBox(0, 0, math.nan, 1))
