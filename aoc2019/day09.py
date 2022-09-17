import logging
from dataclasses import replace

from .inputs.day09 import instructions
from .intcomputer import prepare_improved_tape, run
from .intcomputer.main import run_single
from .intcomputer.models import End

logging.basicConfig(level=logging.INFO)

tape = prepare_improved_tape(instructions)


def solve_part_one():
    """
    >>> solve_part_one()
    2714716640
    """
    t = replace(tape, memory=[1])
    result = run(t)
    return result.memory[0]


def solve_part_two():
    """
    >>> solve_part_two()
    58879
    """
    t = replace(tape, memory=[2])
    result = None

    while not isinstance(t, End):
        result = t
        t = run_single(t)
    return result.memory[0]


if __name__ == "__main__":
    # result_part_one = solve_part_one()

    import doctest

    doctest.testmod()
