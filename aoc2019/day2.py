import logging
from itertools import permutations

from .inputs.day2 import instructions
from .intcomputer import Tape, replace_instructions, run

logging.basicConfig(level=logging.INFO)

tape = Tape(instructions=instructions)


if __name__ == "__main__":
    # replace position 1 with the value 12 and replace position 2 with the value 2
    part1_tape = replace_instructions(tape, {1: 12, 2: 2})
    part1_tape = run(part1_tape)
    logging.info(f"Part One result: {part1_tape.instructions[0]}")

    for noun, verb in permutations(range(0, 100), 2):
        test_tape = replace_instructions(tape, {1: noun, 2: verb})
        if run(test_tape).instructions[0] == 19690720:
            logging.info(
                f"Part Two result: {100*noun+verb}, noun: {noun}, verb: {verb}"
            )
            break
