from itertools import permutations

# step 1
instructions = "3,8,1001,8,10,8,105,1,0,0,21,42,67,88,105,114,195,276,357,438,99999,3,9,101,4,9,9,102,3,9,9,1001,9,2,9,102,4,9,9,4,9,99,3,9,1001,9,4,9,102,4,9,9,101,2,9,9,1002,9,5,9,1001,9,2,9,4,9,99,3,9,1001,9,4,9,1002,9,4,9,101,2,9,9,1002,9,2,9,4,9,99,3,9,101,4,9,9,102,3,9,9,1001,9,5,9,4,9,99,3,9,102,5,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,99"
# instructions = "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10"
instructions_raw = "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"
# instructions_raw = "4,2,99"
instructions = [int(x) for x in instructions.split(",")]
input = [4,3,2,1]



OPERATIONS = {
    # "00": lambda x: (x, 0),
    "01": lambda inst, pointer, input, opcode: s(inst, pointer+3, g(inst, pointer+1, opcode[-3]) + g(inst, pointer+2, opcode[-4])) or (pointer+4, None),
    "02": lambda inst, pointer, input, opcode: s(inst, pointer+3, g(inst, pointer+1, opcode[-3]) * g(inst, pointer+2, opcode[-4])) or (pointer+4, None),
    "03": lambda inst, pointer, input, opcode: s(inst, pointer+1, input.pop(0)) or (pointer+2, None),
    # "04": lambda inst, pointer, input, opcode: print(g(inst, pointer+1, opcode[-3])) or (pointer+2, g(inst, pointer+1, opcode[-3])),
    "04": lambda inst, pointer, input, opcode: si(g(inst, pointer+1, opcode[-3]), input) or (pointer+2, g(inst, pointer+1, opcode[-3])),
    "05": lambda inst, pointer, input, opcode: (g(inst, pointer+2, opcode[-4]), None) if g(inst, pointer+1, opcode[-3]) else (pointer+3, None),
    "06": lambda inst, pointer, input, opcode: (g(inst, pointer+2, opcode[-4]), None) if not g(inst, pointer+1, opcode[-3]) else (pointer+3, None),
    "07": lambda inst, pointer, input, opcode: s(inst, pointer+3, int(g(inst, pointer+1, opcode[-3]) < g(inst, pointer+2, opcode[-4]))) or (pointer+4, None),
    "08": lambda inst, pointer, input, opcode: s(inst, pointer+3, int(g(inst, pointer+1, opcode[-3]) == g(inst, pointer+2, opcode[-4]))) or (pointer+4, None),
    "99": lambda inst, pointer, input, opcode: (-1,None)
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

def si(i, input):
    if input[0] == 0:
        input[0] = i
    else:
        input[1] = i

def run_diagnostic(instructions, pointer, input):
    result = -1
    opcode = f"{instructions[pointer]:05}"
    operation = opcode[-2:]
    pointer, output = OPERATIONS[operation](instructions, pointer, input, opcode)
    if output: 
        print(">",output)
        result= output
    if pointer < 0:
        return result
    return run_diagnostic(instructions, pointer, input)

def get_signal(settings):
    p = 0
    input=[]
    [input.extend((settings[i%5], 0)) for i in range(1000)]

    instructions = [int(x) for x in instructions_raw.split(",")]
    p = run_diagnostic(instructions, 0, input)
    # if p is None: break
    # print(f"step {i}: {p}")
    # return p

# print(max([get_signal(x) for x in permutations(range(5,10))]))
print(get_signal((9,8,7,6,5)))