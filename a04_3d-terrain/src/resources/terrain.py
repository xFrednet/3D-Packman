import glm
import math
import esper

from components import Transformation, TransformationMatrix, ObjectMaterial
from graphics import TerrainVba, Sprite


class Terrain:
    Y_MULTIPLIER = 1.0
    Y_WATER_LEVEL = 128.0 * Y_MULTIPLIER

    def __init__(self):
        pass
    
    def create_chunks(self, world):
        height_map = Sprite('res/terrain/height_map.png')
        width = height_map.width
        depth = height_map.height
        
        vertices = []
        tex_coords = []
        
        for z in range(depth):
            for x in range(width):
                y = height_map.get_avg(x, z) * Terrain.Y_MULTIPLIER - Terrain.Y_WATER_LEVEL
                vertices.append(float(x * 4))
                vertices.append(y)
                vertices.append(float(z * 4))

                tex_coords.append(x / width)
                tex_coords.append(z / depth)

        indices = []
        for col in range(width - 1):
            for row in range(depth - 1):
                # 0  1
                # 2  3
                c0 = col * width + row
                c1 = col * width + (row + 1)
                c2 = (col + 1) * width + row
                c3 = (col + 1) * width + (row + 1)
                
                indices.append(c0)
                indices.append(c2)
                indices.append(c1)

                # #    4
                # # 3  5
                indices.append(c2)
                indices.append(c3)
                indices.append(c1)

        vba = TerrainVba(len(indices))
        vba.load_position_data(vertices)
        vba.load_tex_coords_data(tex_coords)
        vba.load_index_buffer(indices)

        height_map = Sprite('res/terrain/texture_map.png')
        world.create_entity(
            vba,
            Transformation(position=glm.vec3(1.0, 0.0, 0.0), rotation=glm.vec3(0.0, 0.0, 0.0)),
            TransformationMatrix(),
            ObjectMaterial(diffuse=glm.vec3(0.25, 0.8, 0.0)),
            height_map.gen_texture())
