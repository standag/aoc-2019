from copy import copy, deepcopy
from typing import Iterable

from .models import Mode, ReadWrite, Tape


def _take(tape: Tape, size: int) -> list[int]:
    return [tape.instructions[i + tape.pointer] for i in range(size)]


def _pop(tape: Tape) -> int:
    return tape.instructions[tape.pointer]


def _get(tape: Tape, position: int, mode: Mode, read_write: ReadWrite = ReadWrite.read) -> int:
    """Get value from 'position` and mode."""
    match read_write:
        case ReadWrite.read:
            match mode:
                case Mode.position:
                    return tape.instructions[position]
                case Mode.immediate:
                    return position
                case Mode.relative:
                    return tape.instructions[tape.offset + position]
        case ReadWrite.write:
            match mode:
                case Mode.position | Mode.immediate:
                    return position
                case Mode.relative:
                    return position + tape.offset


def _get_multiple(
    tape: Tape,
    positions: Iterable,
    modes: tuple[Mode, Mode, Mode],
    op: tuple[ReadWrite, ReadWrite, ReadWrite] = (
        ReadWrite.read,
        ReadWrite.read,
        ReadWrite.read,
    ),
) -> list[int]:
    return [
        _get(tape, position, modes[i], op[i]) for i, position in enumerate(positions)
    ]


def _replace_instructions(
    instructions: list[int] | dict[int, int], position: int, value: int
) -> list[int] | dict[int, int]:
    instructions = deepcopy(instructions)
    instructions[position] = value
    return instructions
