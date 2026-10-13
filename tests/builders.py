"""Construtores de dados de teste (determinísticos)."""

from vyra.domain.contracts import (
    ClockDomain,
    Detection,
    Provenance,
    Stamp,
    TrackState,
    TrackStatus,
    ValueKind,
)
from vyra.domain.geometry import BBox


def prov() -> Provenance:
    return Provenance.create("test", "0", {"k": "v"})


def stamp(i: int = 0, source: str = "cam0") -> Stamp:
    return Stamp(source, i, i / 25.0, ClockDomain.FRAME_INDEX_DERIVED)


def bbox() -> BBox:
    return BBox(10.0, 20.0, 110.0, 220.0)


def det(index: int = 0, frame: int = 0, name: str = "CAR", class_id: int = 2) -> Detection:
    return Detection(stamp(frame), index, class_id, name, 0.9, bbox(), prov())


def observed(track_id: int, detection_index: int, frame: int = 0) -> TrackState:
    return TrackState(
        track_id, stamp(frame), TrackStatus.CONFIRMED, bbox(), ValueKind.MEASURED,
        detection_index, hits=3,
    )
