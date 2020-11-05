import esper
import glm

import systems

from components import Transformation, CameraOrientation, FreeCamera, Light
from graphics import graphics_math, shader_program
from resources import Terrain, LightSetup

class World(esper.World):
    def __init__(self, resolution):
        super().__init__()
        self.resolution = glm.vec2(resolution[0], resolution[1])
        self.delta = 0.00001
        self.time = self.delta
        self.view_matrix = glm.mat4()
        self.projection_matrix = graphics_math.build_projection_matrix(self.resolution)
        
        self.camera_id = 0
        
        self.terrain = Terrain()
        self.height_map_index = 1
        self.terrain_shader = shader_program.TerrainShader()
        self.water_shader = shader_program.WaterShader()
        self.particle_shader = shader_program.ParticleShader()
        self.light_setup = LightSetup(glm.vec3(0.3, 0.3, 0.3))
        
        self._setup_systems()
        self._setup_entities()

        self.terrain.create_chunks(self)

        print("World was created")

    def _setup_systems(self):
        self.add_processor(systems.FreeCameraControlSystem())
        self.add_processor(systems.UpdateLightSetupSystem())
        self.add_processor(systems.FreeCameraOrientationSystem())
        self.add_processor(systems.BuildTransformationMatrixSystem())
        self.add_processor(systems.PrepareFrameSystem())
        self.add_processor(systems.TerrainRenderer())
        self.add_processor(systems.WaterRendererSystem())
        self.add_processor(systems.ParticleRenderSystem())
        self.add_processor(systems.FinishFrameSystem())

    def _setup_entities(self):
        self.camera_id = self.create_entity(
            Transformation(position=glm.vec3(0.0, 20.0, 0.0), rotation=glm.vec3(0.0, -1.6, 0.0)),
            CameraOrientation(),
            FreeCamera(),
            Light(color=glm.vec3(0.3, 0.3, 0.3))
        )

        # The sun
        self.create_entity(
            Transformation(position=glm.vec3(100.0, 200.0, 100.0)),
            Light(color=glm.vec3(0.6, 0.6, 0.6))
        )

    def cleanup(self):
        self.terrain_shader.cleanup()
        self.water_shader.cleanup()

        print("World cleanup complete")

class TestSystem(esper.Processor):
    def process(self):
        # for _id, transformation in self.world.get_component(Transformation):
        #     transformation.rotation.x += 0.01
        
        self.world.component_for_entity(self.world.camera_id, Transformation).position.x += 0.001
