"""
Python implementation of a maze generation algorithm:
https://en.wikipedia.org/wiki/Maze_generation_algorithm
"""
from random import randint


def _setup_maze(world):
    maze = Maze()
    m = maze.generate_maze()


class Maze:
    def __init__(self, w=7, h=7, complexity=.75, density=.75):
        self.width = w
        self.height = h
        self.complexity = complexity
        self.density = density
        self.maze = None

    def generate_maze(self):
        # will allow only odd shapes
        shape = ((self.height // 2) * 2 + 1, (self.width // 2) * 2 + 1)
        # relative complexity, density
        complexity = int(self.complexity * (5 * (shape[0] + shape[1])))
        density = int(self.density * ((shape[0] // 2) * (shape[1] // 2)))
        m = []
        for a in range(shape[0]):
            arr = [False] * shape[0]
            m.append(arr)
        # Make borders
        m[0] = m[len(m) - 1] = [True] * shape[0]
        for i in range(1, len(m) - 1):
            m[i][0] = m[i][len(m) - 1] = True
        # Open cubes
        for _ in range(density):
            x, y = randint(0, shape[1] // 2) * 2, randint(0, shape[0] // 2) * 2
            m[y][x] = True
            for _ in range(complexity):
                neighbours = []
                if x > 1:
                    neighbours.append((y, x - 2))
                if x < shape[1] - 2:
                    neighbours.append((y, x + 2))
                if y > 1:
                    neighbours.append((y - 2, x))
                if y < shape[0] - 2:
                    neighbours.append((y + 2, x))
                if len(neighbours):
                    a, b = neighbours[randint(0, len(neighbours) - 1)]
                    if not m[a][b]:
                        m[a][b] = True
                        m[a + (y - a) // 2][b + (x - b) // 2] = True
                        x, y = b, a

        self.maze = m
        return m
