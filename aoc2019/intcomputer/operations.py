from dataclasses import replace

from .models import ImprovedTape, Mode, OpCode, ReadWrite, SimpleTape, Tape
from .tape_operations import (_get, _get_multiple, _pop, _replace_instructions,
                              _take)


def _addition(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(
        tape,
        _take(tape, 3),
        opcode.modes,
        (ReadWrite.read, ReadWrite.read, ReadWrite.write),
    )
    result = first + second
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(tape.instructions, third, result),
    )


def _multiplication(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(
        tape,
        _take(tape, 3),
        opcode.modes,
        (ReadWrite.read, ReadWrite.read, ReadWrite.write),
    )
    result = first * second
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(tape.instructions, third, result),
    )


def _update(tape: Tape, opcode: OpCode) -> Tape:
    position = _get(tape, _pop(tape), opcode.modes[0], ReadWrite.write)
    memory = []
    match tape:
        case SimpleTape():
            assert tape.ram is not None
            ram = tape.ram
        case ImprovedTape():
            ram = tape.memory[-1]
            memory = tape.memory[:-1]
        case _:
            raise NotImplementedError

    return replace(
        tape,
        pointer=tape.pointer + 1,
        instructions=_replace_instructions(
            tape.instructions,
            position,
            ram,
        ),
        memory=memory,
    )


def _read(tape: Tape, opcode: OpCode) -> Tape:
    value = _get(tape, _pop(tape), opcode.modes[0])
    update = dict()
    match tape:
        case SimpleTape():
            update = dict(ram=value)
        case ImprovedTape():
            update = dict(memory=tape.memory + [value])
        case _:
            raise NotImplementedError
    return replace(tape, pointer=tape.pointer + 1, **update)


def _jump_if_true(tape: Tape, opcode: OpCode) -> Tape:
    condition, position = _get_multiple(tape, _take(tape, 2), opcode.modes)
    return replace(tape, pointer=position if condition != 0 else tape.pointer + 2)


def _jump_if_false(tape: Tape, opcode: OpCode) -> Tape:
    condition, position = _get_multiple(tape, _take(tape, 2), opcode.modes)
    return replace(tape, pointer=position if condition == 0 else tape.pointer + 2)


def _less_than(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(
        tape,
        _take(tape, 3),
        opcode.modes,
        (ReadWrite.read, ReadWrite.read, ReadWrite.write),
    )
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(
            tape.instructions, third, int(first < second)
        ),
    )


def _equals(tape: Tape, opcode: OpCode) -> Tape:
    first, second, third = _get_multiple(
        tape,
        _take(tape, 3),
        opcode.modes,
        (ReadWrite.read, ReadWrite.read, ReadWrite.write),
    )
    return replace(
        tape,
        pointer=tape.pointer + 3,
        instructions=_replace_instructions(
            tape.instructions, third, int(first == second)
        ),
    )


def _adjust_relative_offset(tape: Tape, opcode: OpCode) -> Tape:
    """
    >>> from collections import defaultdict
    >>> from .main import _int_to_opcode
    >>> _adjust_relative_offset(ImprovedTape(instructions=defaultdict(int,enumerate([9,2000])), pointer=1), _int_to_opcode(9))
    ImprovedTape(instructions=defaultdict(int,enumerate([9,2000]))), _int_to_opcode(9), offset=2000)
    """
    value = _get(tape, _pop(tape), opcode.modes[0])
    return replace(tape, pointer=tape.pointer + 1, offset=tape.offset + value)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
