import math

from vyra.domain.checks import ContractError
from vyra.domain.geometry import BBox, ImagePoint

import pytest


def test_bbox_properties():
    b = BBox(0, 0, 10, 20)
    assert (b.width, b.height, b.area) == (10, 20, 200)
    assert b.center == ImagePoint(5, 10)
    assert b.bottom_center == ImagePoint(5, 20)


def test_bbox_rejects_degenerate_and_inverted():
    with pytest.raises(ContractError):
        BBox(5, 5, 5, 10)
    with pytest.raises(ContractError):
        BBox(10, 0, 5, 10)


def test_bbox_rejects_non_finite():
    with pytest.raises(ContractError):
        BBox(0, 0, math.nan, 10)
    with pytest.raises(ContractError):
        BBox(0, 0, math.inf, 10)
