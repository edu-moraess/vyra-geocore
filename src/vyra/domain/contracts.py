"""Contratos de domínio do VYRA (schema 0.1.0).

Somente biblioteca padrão. Todos os contratos são imutáveis e validam seus invariantes na
construção. Ver CONTRACTS.md para a descrição de cada invariante.

Separação conceitual:
  Detection   = observação instantânea (um frame)
  Track       = identidade temporal atribuída pelo tracker
  TrackState  = estado de um track num instante
  SceneSnapshot = estado completo da cena num Stamp
  Event       = ocorrência temporal com evidências
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from vyra.domain.checks import (
    ContractError,
    check_finite,
    check_instance,
    check_int,
    check_pairs,
    check_str,
    check_tuple,
)
from vyra.domain.geometry import BBox, ImagePoint

SCHEMA_VERSION = "0.1.0"


class ValueKind(str, Enum):
    MEASURED = "MEASURED"
    EXTERNAL = "EXTERNAL"
    INFERRED = "INFERRED"
    DERIVED = "DERIVED"
    PREDICTED = "PREDICTED"
    HYPOTHETICAL = "HYPOTHETICAL"


class ClockDomain(str, Enum):
    SOURCE = "SOURCE"
    SYSTEM = "SYSTEM"
    SYNTHETIC = "SYNTHETIC"


class FrameStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"


class TrackStatus(str, Enum):
    TENTATIVE = "TENTATIVE"
    CONFIRMED = "CONFIRMED"
    LOST = "LOST"
    TERMINATED = "TERMINATED"


class EventKind(str, Enum):
    DETECTED = "DETECTED"
    HYPOTHESIS = "HYPOTHESIS"
    INDETERMINATE = "INDETERMINATE"


@dataclass(frozen=True, slots=True)
class Quantity:
    unit: str
    value: float | None = None
    kind: ValueKind | None = None
    unavailable_reason: str | None = None

    def __post_init__(self) -> None:
        check_str("Quantity.unit", self.unit)
        if self.value is None:
            check_str("Quantity.unavailable_reason", self.unavailable_reason)
            if self.kind is not None:
                raise ContractError("Quantity indisponível não pode ter kind")
        else:
            check_finite("Quantity.value", self.value)
            check_instance("Quantity.kind", self.kind, ValueKind)
            if self.unavailable_reason is not None:
                raise ContractError("Quantity com valor não pode ter unavailable_reason")


@dataclass(frozen=True, slots=True)
class Provenance:
    component: str
    version: str
    parameters: tuple[tuple[str, str], ...] = ()

    def __post_init__(self) -> None:
        check_str("Provenance.component", self.component)
        check_str("Provenance.version", self.version)
        check_pairs("Provenance.parameters", self.parameters)

    @property
    def digest(self) -> str:
        import hashlib

        parts = [self.component, self.version] + [f"{k}={v}" for k, v in sorted(self.parameters)]
        return hashlib.sha256("|".join(parts).encode()).hexdigest()


@dataclass(frozen=True, slots=True)
class Stamp:
    source_id: str
    frame_index: int
    time_s: float
    clock: ClockDomain

    def __post_init__(self) -> None:
        check_str("Stamp.source_id", self.source_id)
        check_int("Stamp.frame_index", self.frame_index, minimum=0)
        check_finite("Stamp.time_s", self.time_s, minimum=0.0)
        check_instance("Stamp.clock", self.clock, ClockDomain)


@dataclass(frozen=True, slots=True)
class Origin:
    source_id: str
    width: int
    height: int
    nominal_fps: float | None = None

    def __post_init__(self) -> None:
        check_str("Origin.source_id", self.source_id)
        check_int("Origin.width", self.width, minimum=1)
        check_int("Origin.height", self.height, minimum=1)
        if self.nominal_fps is not None:
            check_finite("Origin.nominal_fps", self.nominal_fps, minimum=0.0)
            if self.nominal_fps <= 0:
                raise ContractError("Origin.nominal_fps deve ser > 0 quando presente")


@dataclass(frozen=True, slots=True)
class FrameRecord:
    stamp: Stamp
    status: FrameStatus
    note: str | None = None

    def __post_init__(self) -> None:
        check_instance("FrameRecord.stamp", self.stamp, Stamp)
        check_instance("FrameRecord.status", self.status, FrameStatus)
        if self.status is FrameStatus.INVALID:
            check_str("FrameRecord.note", self.note)
        elif self.note is not None:
            check_str("FrameRecord.note", self.note)


@dataclass(frozen=True, slots=True)
class Detection:
    stamp: Stamp
    index: int
    label: str
    score: float
    bbox: BBox
    provenance: Provenance

    def __post_init__(self) -> None:
        check_instance("Detection.stamp", self.stamp, Stamp)
        check_int("Detection.index", self.index, minimum=0)
        check_str("Detection.label", self.label)
        check_finite("Detection.score", self.score, minimum=0.0, maximum=1.0)
        check_instance("Detection.bbox", self.bbox, BBox)
        check_instance("Detection.provenance", self.provenance, Provenance)


@dataclass(frozen=True, slots=True)
class Track:
    track_id: str
    label: str

    def __post_init__(self) -> None:
        check_str("Track.track_id", self.track_id)
        check_str("Track.label", self.label)


@dataclass(frozen=True, slots=True)
class TrackState:
    stamp: Stamp
    track_id: str
    status: TrackStatus
    bbox: BBox | None
    detection_index: int | None
    misses: int
    kind: ValueKind

    def __post_init__(self) -> None:
        check_instance("TrackState.stamp", self.stamp, Stamp)
        check_str("TrackState.track_id", self.track_id)
        check_instance("TrackState.status", self.status, TrackStatus)
        check_int("TrackState.misses", self.misses, minimum=0)
        check_instance("TrackState.kind", self.kind, ValueKind)
        observed = self.detection_index is not None
        if observed:
            check_int("TrackState.detection_index", self.detection_index, minimum=0)
            if self.bbox is None:
                raise ContractError("TrackState observado exige bbox")
            if self.kind is not ValueKind.MEASURED:
                raise ContractError("TrackState observado exige kind=MEASURED")
            if self.misses != 0:
                raise ContractError("TrackState observado exige misses=0")
            if self.status in (TrackStatus.LOST, TrackStatus.TERMINATED):
                raise ContractError("TrackState observado não pode ser LOST/TERMINATED")
        else:
            if self.status is TrackStatus.TERMINATED:
                if self.bbox is not None:
                    raise ContractError("TrackState TERMINATED não deve ter bbox")
            elif self.bbox is not None:
                if self.kind is not ValueKind.PREDICTED:
                    raise ContractError("TrackState com bbox sem detecção exige kind=PREDICTED")


@dataclass(frozen=True, slots=True)
class SceneSnapshot:
    stamp: Stamp
    detections: tuple[Detection, ...]
    tracks: tuple[Track, ...]
    track_states: tuple[TrackState, ...]

    def __post_init__(self) -> None:
        check_instance("SceneSnapshot.stamp", self.stamp, Stamp)
        check_tuple("SceneSnapshot.detections", self.detections, Detection)
        check_tuple("SceneSnapshot.tracks", self.tracks, Track)
        check_tuple("SceneSnapshot.track_states", self.track_states, TrackState)
        for d in self.detections:
            if d.stamp != self.stamp:
                raise ContractError("Detection.stamp deve coincidir com SceneSnapshot.stamp")
        for ts in self.track_states:
            if ts.stamp != self.stamp:
                raise ContractError("TrackState.stamp deve coincidir com SceneSnapshot.stamp")
        idxs = [d.index for d in self.detections]
        if len(idxs) != len(set(idxs)):
            raise ContractError("Detection.index duplicado no SceneSnapshot")
        tids = [t.track_id for t in self.tracks]
        if len(tids) != len(set(tids)):
            raise ContractError("Track.track_id duplicado no SceneSnapshot")
        for ts in self.track_states:
            if ts.track_id not in tids:
                raise ContractError(f"TrackState referencia track_id inexistente: {ts.track_id}")
            if ts.detection_index is not None and ts.detection_index not in idxs:
                raise ContractError(
                    f"TrackState referencia detection_index inexistente: {ts.detection_index}"
                )
        # 1 detecção sustenta no máximo 1 track
        used = [ts.detection_index for ts in self.track_states if ts.detection_index is not None]
        if len(used) != len(set(used)):
            raise ContractError("Uma detecção sustenta no máximo um track")


@dataclass(frozen=True, slots=True)
class EvidenceRef:
    track_id: str | None = None
    detection_index: int | None = None

    def __post_init__(self) -> None:
        if self.track_id is None and self.detection_index is None:
            raise ContractError("EvidenceRef exige track_id e/ou detection_index")
        if self.track_id is not None:
            check_str("EvidenceRef.track_id", self.track_id)
        if self.detection_index is not None:
            check_int("EvidenceRef.detection_index", self.detection_index, minimum=0)


@dataclass(frozen=True, slots=True)
class Event:
    kind: EventKind
    stamp_start: Stamp
    stamp_end: Stamp
    label: str
    evidence: tuple[EvidenceRef, ...]
    limitations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        check_instance("Event.kind", self.kind, EventKind)
        check_instance("Event.stamp_start", self.stamp_start, Stamp)
        check_instance("Event.stamp_end", self.stamp_end, Stamp)
        check_str("Event.label", self.label)
        check_tuple("Event.evidence", self.evidence, EvidenceRef)
        check_tuple("Event.limitations", self.limitations, str)
        if self.stamp_start.source_id != self.stamp_end.source_id:
            raise ContractError("Event stamps devem ter o mesmo source_id")
        if self.stamp_start.clock != self.stamp_end.clock:
            raise ContractError("Event stamps devem ter o mesmo clock")
        if self.stamp_end.time_s < self.stamp_start.time_s:
            raise ContractError("Event intervalo invertido")
        if self.kind in (EventKind.DETECTED, EventKind.HYPOTHESIS) and not self.evidence:
            raise ContractError(f"Event {self.kind} exige evidências")
        if self.kind is EventKind.INDETERMINATE and not self.limitations:
            raise ContractError("Event INDETERMINATE exige limitations")


@dataclass(frozen=True, slots=True)
class PipelineMetrics:
    total: int
    ok: int
    invalid: int
    latency_ms: Quantity
    throughput_fps: Quantity

    def __post_init__(self) -> None:
        check_int("PipelineMetrics.total", self.total, minimum=0)
        check_int("PipelineMetrics.ok", self.ok, minimum=0)
        check_int("PipelineMetrics.invalid", self.invalid, minimum=0)
        if self.ok + self.invalid != self.total:
            raise ContractError("PipelineMetrics: ok + invalid deve igualar total")
        check_instance("PipelineMetrics.latency_ms", self.latency_ms, Quantity)
        check_instance("PipelineMetrics.throughput_fps", self.throughput_fps, Quantity)
        for name, q in (("latency_ms", self.latency_ms), ("throughput_fps", self.throughput_fps)):
            if q.kind is not None and q.kind not in (ValueKind.MEASURED, ValueKind.DERIVED):
                raise ContractError(f"{name} só pode ser MEASURED ou DERIVED")
