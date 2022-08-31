from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from enum import IntEnum


@dataclass(frozen=True)
class Tape:
    instructions: list[int]
    pointer: int = 0
    ram: Optional[int] = None


@dataclass(frozen=True)
class OpCode:
    operation: Operations
    modes: tuple[Mode, Mode, Mode]


class End:
    ...


class Operations(IntEnum):
    addition = 1
    multiplication = 2
    update = 3
    read = 4
    jump_if_true = 5
    jump_if_false = 6
    less_than = 7
    equals = 8
    stop = 99


class Mode(IntEnum):
    position = 0
    immediate = 1
