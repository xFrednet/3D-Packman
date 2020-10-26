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
                tex_coords.append((x + 1) / (width + 1))
                tex_coords.append((z + 1) / (depth + 1))

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


        vba = TerrainMesh(len(indices), self._load_height_maps())
        vba.load_tex_coords_data(tex_coords)
        vba.load_index_buffer(indices)

        world.create_entity(
            vba,
            Transformation(position=glm.vec3(1.0, 0.0, 0.0), rotation=glm.vec3(0.0, 0.0, 0.0)),
            TransformationMatrix())

    def _load_height_maps(self):
        height_maps = [] 
        height_maps.append(Sprite('../res/terrain/height_map_0.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_1.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_2.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_3.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_4.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_5.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_6.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_7.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_8.png').gen_texture())
        height_maps.append(Sprite('../res/terrain/height_map_9.png').gen_texture())
        return height_maps