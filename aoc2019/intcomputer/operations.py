from dataclasses import replace

from .models import OpCode, Tape
from .tape_operations import (_get, _get_multiple, _pop, _replace_instructions,
                              _take)

# Parameters that an instruction writes to will never be in immediate mode.
# TODO: solve this problem

def _addition(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(tape, _take(tape, 3), opcode.modes)  # third is location, immediate mode by default
    result = first + second
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(tape.instructions, third, result),
    )


def _multiplication(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(tape, _take(tape, 3), opcode.modes)
    result = first * second
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(tape.instructions, third, result),
    )


def _update(tape: Tape, opcode: OpCode) -> Tape:
    assert tape.ram is not None
    return replace(
        tape,
        pointer=tape.pointer + 1,
        instructions=_replace_instructions(tape.instructions, _pop(tape), tape.ram),
    )


def _read(tape: Tape, opcode: OpCode) -> Tape:
    value = _get(tape, _pop(tape), opcode.modes[0])
    return replace(tape, pointer=tape.pointer + 1, ram=value)


def _jump_if_true(tape: Tape, opcode: OpCode) -> Tape:
    condition, position = _get_multiple(tape, _take(tape, 2), opcode.modes)
    return replace(tape, pointer=position if condition != 0 else tape.pointer + 2)


def _jump_if_false(tape: Tape, opcode: OpCode) -> Tape:
    condition, position = _get_multiple(tape, _take(tape, 2), opcode.modes)
    return replace(tape, pointer=position if condition == 0 else tape.pointer + 2)


def _less_than(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(tape, _take(tape, 3), opcode.modes)
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(
            tape.instructions, third, int(first < second)
        ),
    )


def _equals(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(tape, _take(tape, 3), opcode.modes)
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(
            tape.instructions, third, int(first == second)
        ),
    )
