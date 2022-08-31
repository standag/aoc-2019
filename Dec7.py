from itertools import permutations

# step 1
instructions = "3,8,1001,8,10,8,105,1,0,0,21,42,67,88,105,114,195,276,357,438,99999,3,9,101,4,9,9,102,3,9,9,1001,9,2,9,102,4,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,101,2,9,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1001,9,4,9,1002,9,4,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99"
# instructions = "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
# instructions = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"
instructions = [int(x) for x in instructions.split(",")]
input = [4,3,2,1]



OPERATIONS = {
    # "00": lambda x: (x, 0),
    "01": lambda inst, pointer, input, opcode: s(inst, pointer+3, g(inst, pointer+1, opcode[-3]) + g(inst, pointer+2, opcode[-4])) or (pointer+4, None),
    "02": lambda inst, pointer, input, opcode: s(inst, pointer+3, g(inst, pointer+1, opcode[-3]) * g(inst, pointer+2, opcode[-4])) or (pointer+4, None),
    "03": lambda inst, pointer, input, opcode: s(inst, pointer+1, input.pop(0)) or (pointer+2, None),
    # "04": lambda inst, pointer, input, opcode: print(g(inst, pointer+1, opcode[-3])) or (pointer+2, g(inst, pointer+1, opcode[-3])),
    "04": lambda inst, pointer, input, opcode: (pointer+2, g(inst, pointer+1, opcode[-3])),
    "05": lambda inst, pointer, input, opcode: (g(inst, pointer+2, opcode[-4]), None) if g(inst, pointer+1, opcode[-3]) else (pointer+3, None),
    "06": lambda inst, pointer, input, opcode: (g(inst, pointer+2, opcode[-4]), None) if not g(inst, pointer+1, opcode[-3]) else (pointer+3, None),
    "07": lambda inst, pointer, input, opcode: s(inst, pointer+3, int(g(inst, pointer+1, opcode[-3]) < g(inst, pointer+2, opcode[-4]))) or (pointer+4, None),
    "08": lambda inst, pointer, input, opcode: s(inst, pointer+3, int(g(inst, pointer+1, opcode[-3]) == g(inst, pointer+2, opcode[-4]))) or (pointer+4, None),
    "99": lambda inst, pointer, input, opcode: (-1,0)
}

def g(instructions, position, immediate_mode):
    if int(immediate_mode):
        return instructions[position]
    else:
        return instructions[instructions[position]]

def s(instructions, position, v, immediate_mode=False):
    # print(position, v)
    if int(immediate_mode):
        instructions[position] = v
    else:
        instructions[instructions[position]] = v

def run_diagnostic(instructions, pointer, input):
    opcode = f"{instructions[pointer]:05}"
    operation = opcode[-2:]
    pointer, output = OPERATIONS[operation](instructions, pointer, input, opcode)
    if output or pointer < 0: 
        # print(">",pointer)
        return output
    return run_diagnostic(instructions, pointer, input)

def get_signal(settings):
    p = 0
    for _s in settings:
        input = [_s,p]
        p = run_diagnostic(instructions, 0, input)
        # print(f"step {_s}: {p}")
    return p

print(max([get_signal(x) for x in permutations(range(5))]))
