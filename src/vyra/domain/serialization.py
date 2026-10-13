"""Serialização determinística e estrita (JSON, sem NaN/Infinity) dos contratos.

Somente escrita nesta versão: `from_dict` (replay) fica pendente para a Fase 1.
"""

from __future__ import annotations

import json
import math
from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any

from vyra.domain.checks import ContractError
from vyra.domain.contracts import SCHEMA_VERSION


def to_plain(obj: Any) -> Any:
    if is_dataclass(obj) and not isinstance(obj, type):
        return {f.name: to_plain(getattr(obj, f.name)) for f in fields(obj)}
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, (tuple, list)):
        return [to_plain(i) for i in obj]
    if isinstance(obj, float):
        if not math.isfinite(obj):
            raise ContractError("valor não finito não é serializável")
        return obj
    if obj is None or isinstance(obj, (bool, int, str)):
        return obj
    raise ContractError(f"tipo não serializável: {type(obj).__name__}")


def to_record(obj: Any) -> dict[str, Any]:
    return {"schema_version": SCHEMA_VERSION, "type": type(obj).__name__, "data": to_plain(obj)}


def to_json_line(obj: Any) -> str:
    """Uma linha JSONL: chaves ordenadas, separadores compactos, NaN proibido."""
    return json.dumps(to_record(obj), sort_keys=True, separators=(",", ":"), allow_nan=False)
