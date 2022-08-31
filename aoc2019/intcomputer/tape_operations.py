from typing import Iterable

from .models import Mode, Tape


def _take(tape: Tape, size: int) -> list[int]:
    return tape.instructions[tape.pointer : tape.pointer + size]


def _pop(tape: Tape) -> int:
    return tape.instructions[tape.pointer]


def _get(tape: Tape, position: int, mode: Mode) -> int:
    match mode:
        case Mode.position:
            return tape.instructions[position]
        case Mode.immediate:
            return position

def _get_multiple(tape: Tape, positions: Iterable, modes: tuple[Mode,Mode,Mode]) -> list[int]:
    return [_get(tape,position,modes[i]) for i,position in enumerate(positions) ]


def _replace_instructions(
    instructions: list[int], position: int, value: int
) -> list[int]:
    instructions = instructions[:]
    instructions[position] = value
    return instructions
