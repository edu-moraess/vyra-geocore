"""Validadores mínimos usados pelos contratos. Somente biblioteca padrão."""

from __future__ import annotations

import math
from typing import Any


class ContractError(ValueError):
    """Violação de invariante de um contrato de domínio."""


def check_str(name: str, value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{name} deve ser uma string não vazia (recebido: {value!r})")


def check_int(name: str, value: Any, minimum: int = 0) -> None:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ContractError(f"{name} deve ser int (recebido: {value!r})")
    if value < minimum:
        raise ContractError(f"{name} deve ser >= {minimum} (recebido: {value})")


def check_finite(
    name: str, value: Any, minimum: float | None = None, maximum: float | None = None
) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ContractError(f"{name} deve ser um número finito (recebido: {value!r})")
    if minimum is not None and value < minimum:
        raise ContractError(f"{name} deve ser >= {minimum} (recebido: {value})")
    if maximum is not None and value > maximum:
        raise ContractError(f"{name} deve ser <= {maximum} (recebido: {value})")


def check_instance(name: str, value: Any, cls: type) -> None:
    if not isinstance(value, cls):
        raise ContractError(f"{name} deve ser {cls.__name__} (recebido: {type(value).__name__})")


def check_tuple(name: str, value: Any, item_type: type | None = None) -> None:
    if not isinstance(value, tuple):
        raise ContractError(f"{name} deve ser tuple (recebido: {type(value).__name__})")
    if item_type is not None:
        for item in value:
            if not isinstance(item, item_type):
                raise ContractError(
                    f"{name} contém item inválido: esperado {item_type.__name__}, "
                    f"recebido {type(item).__name__}"
                )


def check_pairs(name: str, value: Any) -> None:
    check_tuple(name, value)
    for pair in value:
        if not (
            isinstance(pair, tuple)
            and len(pair) == 2
            and isinstance(pair[0], str)
            and isinstance(pair[1], str)
        ):
            raise ContractError(f"{name} deve conter pares (str, str); item inválido: {pair!r}")
