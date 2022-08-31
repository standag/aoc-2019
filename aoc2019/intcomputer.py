from typing import Optional, List


class HaltInstruction(Exception):
    pass


class InvalidOperation(Exception):
    pass


class BaseOperation:
    def __init__(self, computer):
        self.computer = computer

    def get(self, pointer, mode):
        mode = int(mode)
        # positional mode
        if mode == 0:
            return self.computer.tape[self.computer.tape[pointer]]
        elif mode == 1:
            return self.computer.tape[pointer]
        elif mode == 2:
            return self.computer.tape[
                (self.computer.tape[pointer] + self.computer.base)
            ]

    def set(self, pointer, value, mode):
        mode = int(mode)
        if mode == 0:
            self.computer.tape[
                self.computer.tape[pointer] % len(self.computer.tape)
            ] = value
        # elif mode == 1:
        #     self.computer.tape[pointer] = value
        elif mode == 2:
            self.computer.tape[
                (self.computer.tape[pointer] + self.computer.base)
                % len(self.computer.tape)
            ] = value


class SumOperation(BaseOperation):
    def run(self, opcode):
        result = self.get(self.computer.pointer + 1, opcode[-3]) + self.get(
            self.computer.pointer + 2, opcode[-4]
        )
        self.set(self.computer.pointer + 3, result, opcode[-5])
        self.computer.pointer += 4


class MultiplyOperation(BaseOperation):
    def run(self, opcode):
        result = self.get(self.computer.pointer + 1, opcode[-3]) * self.get(
            self.computer.pointer + 2, opcode[-4]
        )
        self.set(self.computer.pointer + 3, result, opcode[-5])
        self.computer.pointer += 4


class WriteOperation(BaseOperation):
    def run(self, opcode):
        self.set(self.computer.pointer + 1, self.computer.memory.pop(0), opcode[-3])
        self.computer.pointer += 2


class ReadOperation(BaseOperation):
    def run(self, opcode):
        self.computer.memory.append(self.get(self.computer.pointer + 1, opcode[-3]))
        # print(self.get(self.computer.pointer + 1, opcode[-3]))
        self.computer.pointer += 2


class JumpIfOperation(BaseOperation):
    def run(self, opcode):
        if self.get(self.computer.pointer + 1, opcode[-3]):
            self.computer.pointer = self.get(self.computer.pointer + 2, opcode[-4])
        else:
            self.computer.pointer += 3


class JumpIfNotOperation(BaseOperation):
    def run(self, opcode):
        if not self.get(self.computer.pointer + 1, opcode[-3]):
            self.computer.pointer = self.get(self.computer.pointer + 2, opcode[-4])
        else:
            self.computer.pointer += 3


class LessThanOperation(BaseOperation):
    def run(self, opcode):
        self.set(
            self.computer.pointer + 3,
            int(
                self.get(self.computer.pointer + 1, opcode[-3])
                < self.get(self.computer.pointer + 2, opcode[-4])
            ),
            opcode[-5],
        )
        self.computer.pointer += 4


class EqualOperation(BaseOperation):
    def run(self, opcode):
        self.set(
            self.computer.pointer + 3,
            int(
                self.get(self.computer.pointer + 1, opcode[-3])
                == self.get(self.computer.pointer + 2, opcode[-4])
            ),
            opcode[-5],
        )
        self.computer.pointer += 4


class AdjustRelativeBaseOperation(BaseOperation):
    def run(self, opcode):
        self.computer.base += self.get(self.computer.pointer + 1, opcode[-3])
        self.computer.pointer += 2


class HaltOperation(BaseOperation):
    def run(self, _):
        self.computer.pointer = 0
        raise HaltInstruction


OPERATIONS = {
    "01": SumOperation,
    "02": MultiplyOperation,
    "03": WriteOperation,
    "04": ReadOperation,
    "05": JumpIfOperation,
    "06": JumpIfNotOperation,
    "07": LessThanOperation,
    "08": EqualOperation,
    "09": AdjustRelativeBaseOperation,
    "99": HaltOperation,
}


class IntCodeComputer:
    def __init__(self, tape: List):
        self.tape = tape[:] + [0] * 10000000
        self.pointer = 0
        self.base = 0
        self.memory = []

    def run(
        self,
        memory: Optional[List] = None,
        pointer=None,
        stop_after_number_of_output=None,
    ):
        if memory:
            self.memory = memory

        if pointer is not None:
            self.pointer = pointer

        try:
            while 0 <= self.pointer <= len(self.tape):
                opcode = f"{self.tape[self.pointer]:05}"
                # print(self.pointer, opcode)
                operation = opcode[-2:]
                result = OPERATIONS[operation](self).run(opcode)
                if stop_after_number_of_output and len(self.memory) == stop_after_number_of_output:
                    break
        except HaltInstruction:
            pass
        except KeyError:
            raise InvalidOperation(operation)
