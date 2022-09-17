from .intcomputer import IntCodeComputer


tape = Tape([int(x) for x in open("aoc2019/inputs/day15.txt").read().split(",")])


def _take(tape: Tape, size: int) -> list[int]:
    return tape.instructions[tape.pointer : tape.pointer + size]


def calculate(instruction: int) -> None:
    _instruction = f"{instruction:05}"
    print(_instruction)


def move(tape: Tape) -> Tape:
    orientation, status = _take(tape, 2)
    calculate(status)
    print(f"orientation {orientation}, status: {status}")

    return tape


if __name__ == "__main__":
    # move(tape)

    computer = IntCodeComputer(tape.instructions)
    print(computer.run(stop_after_number_of_output=1))
    breakpoint()
