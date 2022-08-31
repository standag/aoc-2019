from intcomputer import IntCodeComputer


def test_day_5():
    computer = IntCodeComputer(tape=[int(x) for x in "1002,4,3,4,33".split(",")])
    computer.run()
    assert computer.tape[4] == 99


def test_day_5_2():
    computer = IntCodeComputer(tape=[1101, 100, -1, 4, 0])
    computer.run()


def test_day_5_3():
    computer = IntCodeComputer(tape=[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    computer.run([8])
    assert computer.memory == [1]
    computer = IntCodeComputer(tape=[3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    computer.run([5])
    assert computer.memory == [0]


def test_day_5_4():
    computer = IntCodeComputer(tape=[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
    computer.run([8])
    assert computer.memory == [0]
    computer = IntCodeComputer(tape=[3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
    computer.run([5])
    assert computer.memory == [1]


def test_day_5_5():
    computer = IntCodeComputer(tape=[3, 3, 1108, -1, 8, 3, 4, 3, 99])
    computer.run([8])
    assert computer.memory == [1]
    computer = IntCodeComputer(tape=[3, 3, 1108, -1, 8, 3, 4, 3, 99])
    computer.run([5])
    assert computer.memory == [0]


def test_day_5_6():
    computer = IntCodeComputer(tape=[3, 3, 1107, -1, 8, 3, 4, 3, 99])
    computer.run([8])
    assert computer.memory == [0]
    computer = IntCodeComputer(tape=[3, 3, 1107, -1, 8, 3, 4, 3, 99])
    computer.run([5])
    assert computer.memory == [1]


def test_day_5_7():
    computer = IntCodeComputer(
        tape=[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    )
    computer.run([8])
    assert computer.memory == [1]
    computer = IntCodeComputer(
        tape=[3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    )
    computer.run([0])
    assert computer.memory == [0]


def test_day_5_8():
    computer = IntCodeComputer(tape=[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
    computer.run([8])
    assert computer.memory == [1]
    computer = IntCodeComputer(tape=[3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
    computer.run([0])
    assert computer.memory == [0]


def test_day_9_1():
    tape = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    computer = IntCodeComputer(tape)
    computer.run()
    assert computer.memory == tape
    print()


def test_day_9_2():
    computer = IntCodeComputer(tape=[1102, 34915192, 34915192, 7, 4, 7, 99, 0])
    computer.run()
    assert computer.memory == [1219070632396864]


def test_day_9_3():
    computer = IntCodeComputer(tape=[104, 1125899906842624, 99])
    computer.run()
    assert computer.memory == [1125899906842624]
