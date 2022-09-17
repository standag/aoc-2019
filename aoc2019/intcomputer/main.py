import logging
from collections import defaultdict
from dataclasses import replace
from functools import reduce
from typing import Iterable, overload

from . import operations
from .models import (End, ImprovedTape, Mode, OpCode, Operations, SimpleTape,
                     Tape)
from .tape_operations import _pop, _replace_instructions


def _int_to_opcode(i: int) -> OpCode:
    code = f"{i:05}"
    op = int(code[-2:])
    mode_A, mode_B, mode_C = [int(code[x]) for x in range(3)]  # A B C
    return OpCode(operation=Operations(op), modes=(Mode(mode_C), Mode(mode_B), Mode(mode_A)))


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
        case Operations.adjust_relative_offset:
            return operations._adjust_relative_offset(tape, opcode)
        case Operations.stop:
            logging.debug(f"operation: {opcode.operation}, pointer:{tape.pointer}")
            return End()

    raise NotImplemented()


@overload
def run(tape: SimpleTape) -> SimpleTape:
    ...


@overload
def run(tape: ImprovedTape) -> ImprovedTape:
    ...


def run(tape: Tape) -> Tape:
    opcode = _int_to_opcode(_pop(tape))
    offset = getattr(tape, "offset", None)
    modes = [mode.name for mode in opcode.modes]
    logging.debug(
        f"Operation: {opcode.operation.name:23}, pointer: {tape.pointer}, offset: {offset}, modes: {modes}"
    )
    new = _eval(opcode, replace(tape, pointer=tape.pointer + 1))
    match new:
        case End():
            return tape
        case Tape:
            return run(new)

def run_single(tape: Tape) -> Tape | End:
    opcode = _int_to_opcode(_pop(tape))
    offset = getattr(tape, "offset", None)
    modes = [mode.name for mode in opcode.modes]
    logging.debug(
        f"Operation: {opcode.operation.name:23}, pointer: {tape.pointer}, offset: {offset}, modes: {modes}"
    )
    return _eval(opcode, replace(tape, pointer=tape.pointer + 1))

def replace_instructions(tape: Tape, position_with_new_value: dict[int, int]) -> Tape:
    new_instructions = reduce(
        lambda acc, x: _replace_instructions(acc, x[0], x[1]),
        position_with_new_value.items(),
        tape.instructions,
    )
    return replace(tape, instructions=new_instructions)


def prepare_improved_tape(instructions: list[int]) -> ImprovedTape:
    inst: dict[int, int] = defaultdict(int, enumerate(instructions)) 
    return ImprovedTape(instructions=inst)
