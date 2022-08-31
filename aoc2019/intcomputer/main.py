import logging
from dataclasses import replace
from functools import reduce

from . import operations
from .models import End, Mode, OpCode, Operations, Tape
from .tape_operations import _pop, _replace_instructions


def _int_to_opcode(i: int) -> OpCode:
    code = f"{i:05}"
    op = int(code[-2:])
    _, mode_B, mode_C = [int(code[x]) for x in range(3)]  # A B C
    return OpCode(
        operation=Operations(op), modes=(Mode(mode_C), Mode(mode_B), Mode(1))
    )


def _eval(opcode: OpCode, tape: Tape) -> Tape | End:
    match opcode.operation:
        case Operations.addition:
            return operations._addition(tape, opcode)
        case Operations.multiplication:
            return operations._multiplication(tape, opcode)
        case Operations.update:
            return operations._update(tape, opcode)
        case Operations.read:
            return operations._read(tape, opcode)
        case Operations.jump_if_true:
            return operations._jump_if_true(tape, opcode)
        case Operations.jump_if_false:
            return operations._jump_if_false(tape, opcode)
        case Operations.less_than:
            return operations._less_than(tape, opcode)
        case Operations.equals:
            return operations._equals(tape, opcode)
        case Operations.stop:
            logging.debug(f"operation: {opcode.operation}, pointer:{tape.pointer}")
            return End()

    raise NotImplemented()


def run(tape: Tape) -> Tape:
    opcode = _int_to_opcode(_pop(tape))
    new = _eval(opcode, replace(tape, pointer=tape.pointer + 1))
    match new:
        case End():
            return tape
        case Tape():
            return run(new)


def replace_instructions(tape: Tape, position_with_new_value: dict[int, int]) -> Tape:
    new_instructions = reduce(
        lambda acc, x: _replace_instructions(acc, x[0], x[1]),
        position_with_new_value.items(),
        tape.instructions,
    )
    return replace(tape, instructions=new_instructions)
