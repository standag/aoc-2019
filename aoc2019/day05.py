import logging
from dataclasses import replace

from .inputs.day5 import instructions
from .intcomputer import SimpleTape, run

logging.basicConfig(level=logging.INFO)

tape = SimpleTape(instructions=instructions)


def solve_part_one():
    """
    >>> solve_part_one()
    16489636
    """
    part1_tape = replace(tape, ram=1)
    part1_tape = run(part1_tape)
    logging.info(f"Part One result: {part1_tape.ram}")
    return part1_tape.ram


def solve_part_two():
    """
    >>> solve_part_two()
    9386583
    """
    part2_tape = run(replace(tape, ram=5))
    logging.info(f"Part Two result: {part2_tape.ram}")
    return part2_tape.ram


if __name__ == "__main__":

    import doctest

    doctest.testmod()
