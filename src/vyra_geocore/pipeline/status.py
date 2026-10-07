"""Official status vocabulary for gates and pipeline stages."""

from enum import Enum


class Status(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_EXECUTED = "NOT_EXECUTED"
    WARNING = "WARNING"

    def __str__(self) -> str:
        return self.value
