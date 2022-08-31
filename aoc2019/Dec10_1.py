import math


class Map:
    def __init__(self, raw_map):
        self._matrix = []
        lines = raw_map.split()
        for line in lines:
            self._matrix.append([x for x in line])

    @property
    def dimension(self):
        return (len(self._matrix[0]), len(self._matrix))

    def is_in_map(self, x, y) -> bool:
        return 0 <= x < self.dimension[0] and 0 <= y < self.dimension[1]

    def get(self, x, y):
        return self._matrix[y][x]

    def check_visible_asteroids(self, x, y) -> list:
        counter = 0
        asteroids = []
        for _x in list(range(0, self.dimension[0] - x)) + list(range(-1, -x - 1, -1)):
            for _y in list(range(0, self.dimension[1] - y)) + list(
                range(-1, -y - 1, -1)
            ):
                X = _x + x
                Y = _y + y
                if X == x and Y == y:
                    continue
                # print(f">>{self.get(X, Y)} position: ({X}, {Y})")
                if not (
                    # X >= 0  # outside map
                    # and Y >= 0  # outside map
                    # and (abs(_y) == i or abs(_x) == i)  # outer layer only
                    # and self.is_in_map(X, Y)
                    self.get(X, Y)
                    != "."
                ):
                    continue
                # vector_to_candidate = (X - x, Y - y)
                # if 0 not in (vector_to_candidate):
                #     print(
                #         f"{self.get(X, Y)}: position: ({X}, {Y}), vector: ({X - x}, {Y-y}), norm: ({(X - x)/abs(X - x)}, {(Y-y)/abs(X-x)})"
                #     )

                if X - x == 0 and 0 not in [
                    asteroid[0] - x
                    for asteroid in asteroids
                    if min(Y - y, 0) < asteroid[1] - y < max(Y - y, 0)
                ]:
                    candidate = (X, Y)
                elif Y - y == 0 and 0 not in [
                    asteroid[1] - y
                    for asteroid in asteroids
                    if min(X - x, 0) < asteroid[0] - x < max(X - x, 0)
                ]:
                    candidate = (X, Y)
                elif (X - x) != 0 and (
                    (X - x) / abs(X - x),
                    (Y - y) / abs(X - x),
                ) not in [
                    (
                        (asteroid[0] - x) / abs(asteroid[0] - x),
                        (asteroid[1] - y) / abs(asteroid[0] - x),
                    )
                    for asteroid in asteroids
                    if asteroid[0] - x != 0
                ]:
                    candidate = (X, Y)
                else:
                    candidate = None
                if candidate:
                    asteroids.append(candidate)
        return asteroids

    def find_best_place(self):
        best = 0
        location: tuple = tuple()
        for x in range(self.dimension[0]):
            for y in range(self.dimension[1]):
                if self.get(x, y) == ".":
                    continue
                asteroids = self.check_visible_asteroids(x, y)
                if len(asteroids) > best:
                    best = len(asteroids)
                    location = (x, y)
        return location, best

    def destroy_asteroid(self, x, y):
        self._matrix[y][x] = "."

    def use_laser(self):
        location, count = self.find_best_place()
        i = 1
        while True:
            asteroids = self.check_visible_asteroids(*location)
            if not asteroids:
                break
            asteroids_with_angle = [
                (*x, angle((x[0] - location[0], x[1] - location[1]), (0, 1)))
                for x in asteroids
            ]
            asteroids_with_angle.sort(key=lambda x: x[2], reverse=True)
            print(asteroids_with_angle)
            for asteroid in asteroids_with_angle:
                self.destroy_asteroid(*asteroid[:2])
                print(f"{i}: asteroid destroyed ({asteroid[0]}, {asteroid[1]})")
                i += 1


def dotproduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))


def length(v):
    return math.sqrt(dotproduct(v, v))


def angle(v1, v2):
    x = 1
    if v1[0] != 0:
        x = v1[0] / abs(v1[0])
    return math.degrees(math.acos(dotproduct(v1, v2) / (length(v1) * length(v2))) * x)


def test_angle():
    assert round(angle((5, 24), (1, 3)), 3) == 6.667
    assert round(angle((-2, -5), (0, -1)), 3) == 21.801
    assert round(angle((2, -5), (0, -1)), 3) == 21.801


def test_in_map():
    map = Map(
        """...
...
..."""
    )
    assert map.is_in_map(0, 0) == True
    assert map.is_in_map(-1, 0) == False
    assert map.is_in_map(-1, -1) == False
    assert map.is_in_map(0, -1) == False
    assert map.is_in_map(2, 2) == True
    assert map.is_in_map(2, 3) == False
    assert map.is_in_map(3, 0) == False
    assert map.is_in_map(3, 3) == False


def test_visibility():
    raw = """#.........
...A......
...B..a...
.EDCG....a
..F.c.b...
.....c....
..efd.c.gb
.......c..
....f...c.
...e..d..c"""
    map = Map(raw)
    positions = map.check_visible_asteroids(0, 0)
    assert len(positions) == 7


def test_0():
    raw = """.#..#
.....
#####
....#
...##"""
    map = Map(raw)
    # print([(ast[0]-3, ast[1]-4) for ast in map.check_visible_asteroids(3, 4)])
    assert len(map.check_visible_asteroids(3, 4)) == 8
    location, count = map.find_best_place()
    assert location == (3, 4)
    assert count == 8


def test_1():
    map1 = """......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####"""
    map = Map(map1)
    vis = map.check_visible_asteroids(5, 8)
    for y in range(map.dimension[1]):
        for x in range(map.dimension[0]):
            if (x, y) == (5, 8):
                print("*", end="")
            elif (x, y) not in vis and map.get(x, y) == "#":
                print("X", end="")
            elif (x, y) in vis:
                print("#", end="")
            else:
                print(".", end="")
        print()
    assert len(vis) == 33
    location, count = map.find_best_place()
    assert count == 33
    assert location == (5, 8)


def test_2():
    raw = """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###."""
    map = Map(raw)
    vis = map.check_visible_asteroids(1, 2)
    for y in range(map.dimension[1]):
        for x in range(map.dimension[0]):
            if (x, y) == (1, 2):
                print("*", end="")
            elif (x, y) not in vis and map.get(x, y) == "#":
                print("X", end="")
            elif (x, y) in vis:
                print("#", end="")
            else:
                print(".", end="")
        print()
    assert len(vis) == 35
    location, count = map.find_best_place()
    assert count == 35
    assert location == (1, 2)


def test_3():
    raw = """.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#.."""
    map = Map(raw)
    location, count = map.find_best_place()
    assert count == 41
    assert location == (6, 3)


def test_4():
    raw = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    map = Map(raw)
    location, count = map.find_best_place()
    assert count == 210
    assert location == (11, 13)


def test_5():
    raw = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##"""
    map = Map(raw)
    location, count = map.find_best_place()
    assert location == (8, 3)
    map.use_laser()


def main():
    raw = """.#..#..#..#...#..#...###....##.#....
.#.........#.#....#...........####.#
#..##.##.#....#...#.#....#..........
......###..#.#...............#.....#
......#......#....#..##....##.......
....................#..............#
..#....##...#.....#..#..........#..#
..#.#.....#..#..#..#.#....#.###.##.#
.........##.#..#.......#.........#..
.##..#..##....#.#...#.#.####.....#..
.##....#.#....#.......#......##....#
..#...#.#...##......#####..#......#.
##..#...#.....#...###..#..........#.
......##..#.##..#.....#.......##..#.
#..##..#..#.....#.#.####........#.#.
#......#..........###...#..#....##..
.......#...#....#.##.#..##......#...
.............##.......#.#.#..#...##.
..#..##...#...............#..#......
##....#...#.#....#..#.....##..##....
.#...##...........#..#..............
.............#....###...#.##....#.#.
#..#.#..#...#....#.....#............
....#.###....##....##...............
....#..........#..#..#.......#.#....
#..#....##.....#............#..#....
...##.............#...#.....#..###..
...#.......#........###.##..#..##.##
.#.##.#...##..#.#........#.....#....
#......#....#......#....###.#.....#.
......#.##......#...#.#.##.##...#...
..#...#.#........#....#...........#.
......#.##..#..#.....#......##..#...
..##.........#......#..##.#.#.......
.#....#..#....###..#....##..........
..............#....##...#.####...##."""
    map = Map(raw)
    location, count = map.find_best_place()
    print(location, count)

def main2():
    raw = """.#..#..#..#...#..#...###....##.#....
.#.........#.#....#...........####.#
#..##.##.#....#...#.#....#..........
......###..#.#...............#.....#
......#......#....#..##....##.......
....................#..............#
..#....##...#.....#..#..........#..#
..#.#.....#..#..#..#.#....#.###.##.#
.........##.#..#.......#.........#..
.##..#..##....#.#...#.#.####.....#..
.##....#.#....#.......#......##....#
..#...#.#...##......#####..#......#.
##..#...#.....#...###..#..........#.
......##..#.##..#.....#.......##..#.
#..##..#..#.....#.#.####........#.#.
#......#..........###...#..#....##..
.......#...#....#.##.#..##......#...
.............##.......#.#.#..#...##.
..#..##...#...............#..#......
##....#...#.#....#..#.....##..##....
.#...##...........#..#..............
.............#....###...#.##....#.#.
#..#.#..#...#....#.....#............
....#.###....##....##...............
....#..........#..#..#.......#.#....
#..#....##.....#............#..#....
...##.............#...#.....#..###..
...#.......#........###.##..#..##.##
.#.##.#...##..#.#........#.....#....
#......#....#......#....###.#.....#.
......#.##......#...#.#.##.##...#...
..#...#.#........#....#...........#.
......#.##..#..#.....#......##..#...
..##.........#......#..##.#.#.......
.#....#..#....###..#....##..........
..............#....##...#.####...##."""
    map = Map(raw)
    location, count = map.find_best_place()
    map.use_laser()

if __name__ == "__main__":

    main2()
