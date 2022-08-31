ITEMS = [" ", "#", "x", "-", "*", ""]

class Arcade:
    def __init__(self):
        self.score = 0

    def get_map(self, map_instructions):
        _map = {}
        for x, y, block in zip(*[iter(map_instructions)]*3):
            _map[(x,y)] = block
        return _map

    def draw(self, map_instructions):
        _map = self.get_map(map_instructions)
        self.score = _map.get((-1,0), 0)
        for y in range(21):
            for x in range(43):
                # print(x, y, _map.get((x,y)))
                print(ITEMS[_map.get((x,y), 5)], end="")
            print()