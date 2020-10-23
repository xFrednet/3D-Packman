import glm
import math
import esper

from components import Transformation, TransformationMatrix, ObjectMaterial
from graphics import TerrainVba, Sprite


class Terrain:
    Y_MULTIPLIER = 0.25
    Y_WATER_LEVEL = 128.0 * Y_MULTIPLIER

    def __init__(self):
        pass
    
    def create_chunks(self, world):
        height_map = Sprite('res/terrain/heightmap.png')
        width = height_map.width
        depth = height_map.height
        
        vertices = []
        normals = []
        n_vec = glm.vec3()
        for z in range(depth):
            for x in range(width):
                y = height_map.get_avg(x, z) * Terrain.Y_MULTIPLIER - Terrain.Y_WATER_LEVEL
                vertices.append(float(x * 10))
                vertices.append(y)
                vertices.append(float(z * 10))

                if (z != 0 and x != 0):
                    h = vertices[(x + (z - 1) * width) * 3 + 1] - y
                    l = vertices[((x - 1) + z * width) * 3 + 1] - y

                    total = math.sqrt((h ** 2) + (l ** 2) + 1)

                    normals.append(h / total)
                    normals.append(1.0 / total)
                    normals.append(l / total)
                else:
                    normals.append(0.0)
                    normals.append(1.0)
                    normals.append(0.0)

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
        vba.load_normal_data(normals)
        vba.load_index_buffer(indices)

        world.create_entity(
            vba,
            Transformation(position=glm.vec3(1.0, 0.0, 0.0), rotation=glm.vec3(0.0, 0.0, 0.0)),
            TransformationMatrix(),
            ObjectMaterial(diffuse=glm.vec3(0.25, 0.8, 0.0)))
