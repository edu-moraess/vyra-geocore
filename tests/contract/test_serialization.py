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
    assert parsed["data"]["detections"][0]["bbox"]["x2"] == 110.0
    assert parsed["data"]["track_states"][0]["bbox_kind"] == "measured"


def test_non_finite_and_foreign_types_are_rejected():
    with pytest.raises(ContractError):
        to_plain(math.nan)
    with pytest.raises(ContractError):
        to_plain({1, 2})
