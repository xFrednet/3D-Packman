import esper
import glm

import terrain

import systems

from components import Transformation, CameraOrientation
from graphics import graphics_math, shader_program

class World(esper.World):
    def __init__(self, resolution):
        super().__init__()
        self.resolution = glm.vec2(resolution[0], resolution[1])
        self.delta = 0.00001
        self.view_matrix = glm.mat4()
        self.projection_matrix = graphics_math.build_projection_matrix(self.resolution)
        
        self.camera_id = 0
        
        self.terrain = terrain.Terrain()
        self.terrainShader = shader_program.TerrainShader()
        
        self._setup_systems()
        self._setup_entities()

        self.terrain.create_chunks(self)

        print("World was created")

    def _setup_systems(self):
        self.add_processor(systems.FreeCameraControlSystem())
        self.add_processor(systems.BuildTransformationMatrixSystem())
        self.add_processor(systems.PrepareFrameSystem())
        self.add_processor(systems.TerrainRenderer())
        self.add_processor(systems.FinishFrameSystem())

    def _setup_entities(self):
        self.camera_id = self.create_entity(
            Transformation(position=glm.vec3(0.0, 0.0, -1.0)),
            CameraOrientation()
        )

    def cleanup(self):
        self.terrainShader.cleanup()

        print("World cleanup complete")

class TestSystem(esper.Processor):
    def process(self):
        # for _id, transformation in self.world.get_component(Transformation):
        #     transformation.rotation.x += 0.01
        
        self.world.component_for_entity(self.world.camera_id, Transformation).position.x += 0.001
