import logging
from dataclasses import replace

import pytest

from aoc2019.intcomputer import SimpleTape as Tape
from aoc2019.intcomputer import prepare_improved_tape, run

logging.basicConfig(level=logging.DEBUG)


@pytest.mark.parametrize(
    "tape,result",
    [
        (Tape(instructions=[99]), 99),
        (Tape(instructions=[1, 0, 0, 0, 99]), 2),
        (Tape(instructions=[2, 3, 0, 3, 99]), 2),
        (Tape(instructions=[1, 1, 1, 4, 99, 5, 6, 0, 99]), 30),
    ],
)
def test_run_day2(tape: Tape, result: int) -> None:
    t = run(tape)
    assert isinstance(t, Tape)
    assert t.instructions[0] == result


def test_position_mode_jump_day5():
    i = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    tape = Tape(instructions=i)

    t0 = replace(tape, ram=0)
    t0_result = run(t0)
    assert isinstance(t0_result, Tape)
    assert t0_result.ram == 0

    t1 = replace(tape, ram=1)
    t1_result = run(t1)
    assert isinstance(t1_result, Tape)
    assert t1_result.ram == 1


def test_immediate_mode_jump_day5():
    i = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
    tape = Tape(instructions=i)

    t0 = replace(tape, ram=0)
    t0_result = run(t0)
    assert isinstance(t0_result, Tape)
    assert t0_result.ram == 0

    t1 = replace(tape, ram=1)
    t1_result = run(t1)
    assert isinstance(t1_result, Tape)
    assert t1_result.ram == 1


@pytest.mark.parametrize("ram,result", [(1, 999), (8, 1000), (10, 1001)])
def test_run_day5(ram: int, result: int) -> None:
    instructions = """
    3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
    1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
    999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"""

    tape = Tape(instructions=[int(x.strip()) for x in instructions.split(",")], ram=ram)
    tape_result = run(tape)

    assert isinstance(tape_result, Tape)
    assert tape_result.ram == result


def test_run_day9():
    instructions = [
        109,
        1,
        204,
        -1,
        1001,
        100,
        1,
        100,
        1008,
        100,
        16,
        101,
        1006,
        101,
        0,
        99,
    ]
    tape = prepare_improved_tape(instructions)
    result = run(tape)
    assert result.memory == instructions


@pytest.mark.parametrize(
    "instructions, result_memory",
    [
        ([1102, 34915192, 34915192, 7, 4, 7, 99, 0], [34915192 * 34915192]),
        ([104, 1125899906842624, 99], [1125899906842624]),
    ],
)
def test_run_day9_second(instructions: list[int], result_memory: list[int]):
    tape = prepare_improved_tape(instructions)
    result = run(tape)
    assert result.memory == result_memory


def test_run_day9_third():
    tape = prepare_improved_tape([109, 19, 204, -34, 99])
    tape.offset = 2000
    tape.instructions[1985] = 999
    result = run(tape)
    assert result.offset == 2019
    assert result.memory[0] == 999
