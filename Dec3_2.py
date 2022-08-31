instructions = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"""

DIRECTION = {
    "R": (1,0),
    "L": (-1,0),
    "U": (0,1),
    "D": (0,-1)
}

def get_wired(position, instruction):
    direction = DIRECTION[instruction[0]]
    length = int(instruction[1:])
    return [(position[0]+direction[0]*i, position[1]+direction[1]*i) for i in range(1,length+1)], (position[0]+direction[0]*(length), position[1]+direction[1]*(length))

total = []
for wire in instructions.split():
    wired = []
    position = (0,0)
    for instruction in wire.split(","):
        w, position = get_wired(position, instruction)
        wired.extend(w)
    total.append(wired)

intersections = set(total[0]) & set(total[1])

print(min([total[0].index(intersection)+total[1].index(intersection) for intersection in intersections])+2)
    
