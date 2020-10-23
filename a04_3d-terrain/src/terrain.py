import glm
import esper

from components import Transformation, TransformationMatrix
from graphics.vba import TerrainVba


class Terrain:
    def __init__(self):
        pass
    
    def create_chunks(self, world):
        vba = TerrainVba(3)
        vba.load_position_data([
            -0.5,  0.5, 0.0, 
            -0.5, -0.5, 0.0, 
             0.5,  0.5, 0.0 
        ])
        vba.load_normal_data([
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ])

        world.create_entity(
            vba,
            Transformation(position=glm.vec3(1.0, 0.0, 0.0), rotation=glm.vec3(0.0, 1.6, 0.0)),
            TransformationMatrix())
