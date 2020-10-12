"""
Python implementation of a maze generation algorithm:
https://en.wikipedia.org/wiki/Maze_generation_algorithm
"""
import math
from random import randint

import components_3d as com
import glm
import resources as res


def unites(i, j, world, w, h, depth, model_id, diffuse):
    cube = world.create_entity(
        com.Model3D(model_id),
        com.Transformation(
            position=glm.vec3(i + w / 2, j + h / 2, depth / 2),
            scale=glm.vec3(float(w), float(h), depth)),
        com.BoundingBox(com.Rectangle3D(float(w), float(h), depth)),
        com.TransformationMatrix(),
        com.ObjectMaterial(diffuse=diffuse)
    )


def _setup_maze(world, width, height, depth=2.0, wall_width=1.0, path_width=3.0):
    model_id = world.model_registry.get_model_id(res.ModelRegistry.CUBE)
    maze = Maze(w=width, l=height)
    m = maze.generate_maze()
    y = 0
    m[1][1] = False  # always free

    # Le floor
    floor_size = glm.vec2(width * (wall_width + path_width) / 2, height * (wall_width + path_width) / 2)
    maze.center = glm.vec3(floor_size.x / 2, floor_size.y / 2, 0)
    world.create_entity(
        com.Model3D(model_id),
        com.Transformation(
            position=glm.vec3(maze.center.x, maze.center.y, -(path_width / 2)),
            scale=glm.vec3(floor_size.x, floor_size.y, path_width)),
        com.BoundingBox(com.Rectangle3D(floor_size.x, floor_size.y, path_width)),
        com.TransformationMatrix(),
        com.ObjectMaterial(
            diffuse=glm.vec3(0.6, 0.6, 0.6),
            specular=glm.vec3(0.2, 0.3, 0.6),
            shininess=6)
    )
    # i + w / 2, j + h / 2
    # Le Walls
    for i in range(len(m[0])):
        x = 0
        h = 0
        if i % 2 == 0:
            h = wall_width
        else:
            h = path_width

        shape_w = 0
        shape_x = 0
        has_shape = False
        for j in range(len(m[0]) + 1):
            w = 0
            if j % 2 == 0:
                w = wall_width
            else:
                w = path_width
            is_set = False
            if j < len(m[0]):
                is_set = m[i][j]
            if is_set:
                if not has_shape:
                    has_shape = True
                    shape_x = x
                shape_w += w
            elif has_shape:
                # Draw last shape
                diffuse = glm.vec3(
                    shape_x / floor_size.x,
                    y / floor_size.y,
                    abs(math.cos(y / 10.0))
                )
                unites(shape_x, y, world, shape_w, h, depth, model_id, diffuse)
                has_shape = False
                shape_w = 0
            else:
                maze.empty_areas_loc.append([x, y])
            x += w
        y += h
    return maze


class Maze:
    def __init__(self, w=30, l=30, complexity=0.75, density=0.75):
        # min values for w and l are 6
        self.width = w
        self.height = l
        self.complexity = complexity
        self.density = density
        self.shape = ((self.height // 2) * 2 + 1, (self.width // 2) * 2 + 1)
        self.maze = []
        self.center = glm.vec3()
        self.empty_areas_loc = []

    def generate_maze(self):
        complexity = int(self.complexity * (5 * (self.shape[0] + self.shape[1])))
        density = int(self.density * ((self.shape[0] // 2) * (self.shape[1] // 2)))
        m = []
        for a in range(self.shape[0]):
            arr = [False] * self.shape[0]
            m.append(arr)
        # Le borders
        m[0] = m[len(m) - 1] = [True] * self.shape[0]
        for i in range(1, len(m) - 1):
            m[i][0] = m[i][len(m) - 1] = True
        # Le open cubes
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
