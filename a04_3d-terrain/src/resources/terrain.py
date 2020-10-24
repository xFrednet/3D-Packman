import glm
import math
import esper
import random

from components import Transformation, TransformationMatrix, ObjectMaterial
from graphics import TerrainMesh, Sprite


class Terrain:
    Y_MULTIPLIER = 1.0
    Y_WATER_LEVEL = 128.0 * Y_MULTIPLIER

    def __init__(self):
        pass
    
    def create_chunks(self, world, width=250, depth=250):
        tex_coords = []
        for z in range(depth):
            for x in range(width):
                tex_coords.append(x / width)
                tex_coords.append(z / depth)

        indices = []
        for col in range(width - 1):
            for row in range(depth - 1):
                # 0  1
                # 2  3
                c0 = row * width + col
                c1 = row * width + (col + 1)
                c2 = (row + 1) * width + col
                c3 = (row + 1) * width + (col + 1)
                
                if random.choice([True, False]):
                    # c0  c1|     c1
                    # c2    | c2  c3
                    indices.append(c0)
                    indices.append(c2)
                    indices.append(c1)

                    indices.append(c2)
                    indices.append(c3)
                    indices.append(c1)
                    pass
                else:
                    # c0  c1 | c0  
                    #     c3 | c2  c3
                    indices.append(c0)
                    indices.append(c3)
                    indices.append(c1)

                    indices.append(c0)
                    indices.append(c2)
                    indices.append(c3)


        height_map = Sprite('res/terrain/height_map.png')
        vba = TerrainMesh(len(indices), height_map.gen_texture())
        vba.load_tex_coords_data(tex_coords)
        vba.load_index_buffer(indices)

        world.create_entity(
            vba,
            Transformation(position=glm.vec3(1.0, 0.0, 0.0), rotation=glm.vec3(0.0, 0.0, 0.0)),
            TransformationMatrix(),
            ObjectMaterial(diffuse=glm.vec3(0.25, 0.8, 0.0)))
