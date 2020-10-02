"""
Python implementation of a maze generation algorithm:
https://en.wikipedia.org/wiki/Maze_generation_algorithm
"""
from random import randint
import glm
from vertex_buffer_array import StandardShaderVertexArray
import components as com


# TODO:
# fix Le Maze to be able to create a better maze
# depth-testing
# lightning


def unit(i, j, world, h, cl=1.0, cw=1.0):
    cube = world.create_entity()
    rect = com.Rectangle(cl, cw, h)
    world.add_component(cube, rect)
    world.add_component(cube, com.Position(i + cl, j + cw, 2.0))
    world.add_component(cube, StandardShaderVertexArray.from_rectangle(rect))
    world.add_component(cube, com.Scale())
    world.add_component(cube, com.Rotation())
    world.add_component(cube, com.TransformationMatrix())
    world.add_component(cube, com.ObjectMaterial(color=glm.vec3(0.3, 0.3, 0.3)))


def _setup_maze(world):
    maze = Maze()
    m = maze.generate_maze()
    print(len(m))
    print(len(m[1]))
    for i in range(len(m)):
        for j in range(len(m[0])):
            if m[i][j]:
                if i % 2 == 0:
                    unit(i, j, world, maze.height, 1.0)
                if i % 2 == 1:
                    unit(i, j, world, maze.height, 1.0, 1.0)


class Maze:
    def __init__(self, w=10, l=20, h=1.0, complexity=.75, density=.75):
        self.width = w
        self.length = l
        self.height = h
        self.complexity = complexity
        self.density = density
        self.shape = ((self.length // 2) * 2 + 1, (self.width // 2) * 2 + 1)
        self.maze = []

    def generate_maze(self):
        complexity = int(self.complexity * (5 * (self.shape[0] + self.shape[1])))
        density = int(self.density * ((self.shape[0] // 2) * (self.shape[1] // 2)))
        m = []
        for a in range(self.shape[0]):
            arr = [False] * self.shape[0]
            m.append(arr)
        # Make borders
        m[0] = m[len(m) - 1] = [True] * self.shape[0]
        for i in range(1, len(m) - 1):
            m[i][0] = m[i][len(m) - 1] = True
        # Open cubes
        for _ in range(density):
            x, y = randint(0, self.shape[0] // 2) * 2, randint(0, self.shape[1] // 2) * 2
            m[y][x] = True
            for _ in range(complexity):
                neighbours = []
                if x > 1:
                    neighbours.append((y, x - 2))
                if x < self.shape[1] - 2:
                    neighbours.append((y, x + 2))
                if y > 1:
                    neighbours.append((y - 2, x))
                if y < self.shape[0] - 2:
                    neighbours.append((y + 2, x))
                if len(neighbours):
                    a, b = neighbours[randint(0, len(neighbours) - 1)]
                    if not m[a][b]:
                        m[a][b] = True
                        m[a + (y - a) // 2][b + (x - b) // 2] = True
                        x, y = b, a
        self.maze = m
        return m
