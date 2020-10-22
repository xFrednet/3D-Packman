import esper
import glm

import terrain

from graphics import shader_program
from systems import frame_system, render_preperation_system

from components import Transformation

class World(esper.World):
    def __init__(self, resolution):
        super().__init__()
        self.resolution = resolution
        self.delta = 0.00001
        self.view_matrix = glm.mat4()
        self.projection_matrix = glm.mat4()
        
        self.terrain = terrain.Terrain()
        self.terrainShader = shader_program.TerrainShader()
        
        self._setup_systems()

        self.terrain.create_chunks(self)

        print("World was created")

    def _setup_systems(self):
        self.add_processor(TestSystem())
        self.add_processor(render_preperation_system.BuildTransformationMatrixSystem())
        self.add_processor(frame_system.PrepareFrameSystem())
        self.add_processor(terrain.TerrainRenderer())
        self.add_processor(frame_system.FinishFrameSystem())

    def cleanup(self):
        self.terrainShader.cleanup()

        print("World cleanup complete")

class TestSystem(esper.Processor):
    def process(self, *args, **kwargs):
        for _id, transformation in self.world.get_component(Transformation):
            transformation.rotation.x += 0.1
