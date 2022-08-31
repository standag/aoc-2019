from dataclasses import dataclass

matrix = [[[], [], []], [[], [], []], [[], [], []], [[], [], []]]
sequence_size = [0, 0, 0]  # [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

X = 100

@dataclass
class Point:
    x: int
    y: int
    z: int

    def abssum(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def __getitem__(self, key):
        MAP = {0: self.x, 1: self.y, 2: self.z}
        return MAP[key]


class Moon:
    def __init__(self, x, y, z):
        self.position = Point(x, y, z)
        self.velocity = Point(0, 0, 0)

    def __repr__(self):
        return f"Position: {self.position}, velocity: {self.velocity}"

    def move(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y
        self.position.z += self.velocity.z

    def update_velocity(self, gravity: Point):
        self.velocity.x += gravity.x
        self.velocity.y += gravity.y
        self.velocity.z += gravity.z

    def calc_energy(self):
        return self.position.abssum() * self.velocity.abssum()

    def update_matrix(self, j):

        for i in range(3):
            # if sequence_size[i] != 0:
            #     continue
            if not is_full_sequence(matrix[j][i]):
                matrix[j][i].append(self.velocity[i])
            else:
                sequence_size[i] = len(matrix[j][i]) - X


def gravity(moons):
    gravity = []
    for moon in moons:
        point = [
            sum([1 for m in moons if m.position[i] > moon.position[i]])
            - sum([1 for m in moons if m.position[i] < moon.position[i]])
            for i in range(3)
        ]
        gravity.append(Point(*point))
    return gravity


def is_full_sequence(sequence):
    return (
        len(sequence) > X
        and len(sequence) % 2 == 0
        and sequence[:X] == sequence[-X:]
    )


def iterate(moons, number_of_iterations):
    for i in range(number_of_iterations):
        if i % 10000 == 0:
            print(f" == iteration {i} ==")
            print(sequence_size)
            # print(matrix)
        g = gravity(moons)
        for j in range(len(moons)):
            moons[j].update_velocity(g[j])
            moons[j].move()
        moons[j].update_matrix(j)
            

        # if any(moon.velocity.x == 0 or moon.velocity.y == 0 or moon.velocity.z == 0 for moon in moons):
        #     print(f" == iteration {i} ==")
        #     [print(moon) for moon in moons]
        # print(f"Total energy: {sum(moon.calc_energy() for moon in moons)}")
        if 0 not in sequence_size:
            print(i)
            print(sequence_size)
            break


moons1 = [Moon(-1, 0, 2), Moon(2, -10, -7), Moon(4, -8, 8), Moon(3, 5, -1)]

moons2 = [Moon(-8, -10, 0), Moon(5, 5, 10), Moon(2, -7, 3), Moon(9, -8, -3)]

# <x=0, y=4, z=0>
# <x=-10, y=-6, z=-14>
# <x=9, y=-16, z=-3>
# <x=6, y=-1, z=2>

moons = [Moon(0, 4, 0), Moon(-10, -6, -14), Moon(9, -16, -3), Moon(6, -1, 2)]

iterate(moons, 1000000)
# breakpoint()
