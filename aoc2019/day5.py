import logging
from dataclasses import replace

from .inputs.day5 import instructions
from .intcomputer import Tape, run

logging.basicConfig(level=logging.INFO)

tape = Tape(instructions=instructions)


if __name__ == "__main__":
    part1_tape = replace(tape, ram=1)
    part1_tape = run(part1_tape)
    logging.info(f"Part One result: {part1_tape.ram}")

    part2_tape = run(replace(tape, ram=5))
    logging.info(f"Part Two result: {part2_tape.ram}")
