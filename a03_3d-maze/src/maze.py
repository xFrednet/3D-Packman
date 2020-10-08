"""
Python implementation of a maze generation algorithm:
https://en.wikipedia.org/wiki/Maze_generation_algorithm
"""
from random import randint
import glm
from vertex_buffer_array import StandardShaderVertexArray
import components_3d as com
import ressources as res


# TODO:
# minimap


def unites(i, j, world, w, h, depth, model_id):
    cube = world.create_entity()
    world.add_component(cube, com.Model3D(model_id))
    world.add_component(cube, com.Position(i + w / 2, j + h / 2, 2.0))
    world.add_component(cube, com.BoundingBox(com.Rectangle3D(float(w), float(h), depth)))
    world.add_component(cube, com.Scale(float(w), float(h), depth))
    world.add_component(cube, com.Rotation())
    world.add_component(cube, com.TransformationMatrix())
    world.add_component(cube, com.ObjectMaterial(diffuse=glm.vec3(0.4, 0.4, 0.4)))


def _setup_maze(world, width, height, depth=2.0):
    model_id = world.model_registry.get_model_id(res.ModelRegistry.CUBE)
    maze = Maze(w=width, l=height)
    m = maze.generate_maze()
    scale = 3  # scales the empty space of the maze
    y = 0
    m[1][1] = False
    for i in range(len(m[0])):
        x = 0
        h = 0
        if i % 2 == 0:
            h = 1
        else:
            h = scale
        
        shape_w = 0
        shape_x = 0
        has_shape = False
        for j in range(len(m[0]) + 1):
            w = 0
            if j % 2 == 0:
                w = 1
            else:
                w = scale
            
            is_set = False
            if (j < len(m[0])):
                is_set = m[i][j]

            if is_set:
                if not has_shape:
                    has_shape = True
                    shape_x = x
                shape_w += w
            elif has_shape:
                # Draw last shape
                unites(shape_x, y, world, shape_w, h, depth, model_id)
                has_shape = False
                shape_w = 0
            x += w
        y += h
    return m


class Maze:
    def __init__(self, w=30, l=30, complexity=.75, density=.75):
        # min values for w and l are 6
        self.width = w
        self.height = l
        self.complexity = complexity
        self.density = density
        self.shape = ((self.height // 2) * 2 + 1, (self.width // 2) * 2 + 1)
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
