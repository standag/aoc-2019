from __future__ import annotations

from dataclasses import dataclass, field
from enum import Flag, IntEnum
from typing import Optional


@dataclass(frozen=True)
class SimpleTape:
    instructions: list[int]
    pointer: int = 0
    offset: int = 0
    ram: Optional[int] = None


@dataclass(frozen=True)
class ImprovedTape:
    instructions: dict[int, int]
    pointer: int = 0
    offset: int = 0
    ram: Optional[int] = None
    memory: list[int] = field(default_factory=list)

    @property
    def opcode(self) -> OpCode:
        ...


Tape = SimpleTape | ImprovedTape


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
    adjust_relative_offset = 9
    stop = 99


class Mode(IntEnum):
    position = 0
    immediate = 1
    relative = 2


# Parameters that an instruction writes to will never be in immediate mode.
class ReadWrite(Flag):
    read = 0
    write = 1
