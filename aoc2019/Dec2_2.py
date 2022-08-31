input_raw = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,5,19,23,1,6,23,27,1,27,10,31,1,31,5,35,2,10,35,39,1,9,39,43,1,43,5,47,1,47,6,51,2,51,6,55,1,13,55,59,2,6,59,63,1,63,5,67,2,10,67,71,1,9,71,75,1,75,13,79,1,10,79,83,2,83,13,87,1,87,6,91,1,5,91,95,2,95,9,99,1,5,99,103,1,103,6,107,2,107,13,111,1,111,10,115,2,10,115,119,1,9,119,123,1,123,9,127,1,13,127,131,2,10,131,135,1,135,5,139,1,2,139,143,1,143,5,0,99,2,0,14,0"



def call_code(noon, verb):
    input = [int(x) for x in input_raw.split(",")]
    input[1] = noon
    input[2] = verb
    for i in range(0, len(input), 4):
        (opcode, pos1, pos2, pos3) = input[i:i+4]
        if opcode == 99: break
        if opcode == 1:
            input[pos3] = input[pos1] + input[pos2]
        elif opcode == 2:
            input[pos3] = input[pos1] * input[pos2]
        else:
            raise ValueError(f"Position: {i}, opcode: {opcode}")

    return input[0]

size = input_raw.count(",")
for i in range(size):
    for j in range(size):
        if call_code(i,j) == 19690720:
            print(i*100+j)
