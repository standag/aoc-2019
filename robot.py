TURNS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
VISUAL_DIRECTION = ["^", ">", "v", "<"]


class Robot:
    def __init__(self):
        self.position = (0, 0)
        self.direction = (0, -1)
        self.map = {}

    def make_step(self, color, turn):
        self.paint(color)
        self.make_turn(turn)
        self.move()
        
    
    def paint(self, color):
        self.map[self.position] = color

    def make_turn(self, turn):
        i = TURNS.index(self.direction)
        # print(f"i={i}, turn={turn}, ({TURNS[(i + 1) % 4]}) or ({TURNS[(i + 4 - 1) % 4]})")
        if turn:
            self.direction = TURNS[(i + 1) % 4]
        else:
            self.direction = TURNS[(i + 4 - 1) % 4]

    def move(self):
        print(self.position, self.direction)
        self.position = (
            self.position[0] + self.direction[0],
            self.position[1] + self.direction[1],
        )
        print(self.position, self.direction)

    def draw_map(self):
        for y in range(0,7):
            for x in range(0,42):
                if (x,y) == self.position:
                    print(VISUAL_DIRECTION[TURNS.index(self.direction)], end="")
                    continue
                color = "."
                if self.map.get((x,y), False):
                    color="#"
                print(color, end="")
            print()