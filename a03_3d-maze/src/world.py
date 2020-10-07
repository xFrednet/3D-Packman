import esper
import random
import math
import glm

from shader_program import StandardShaderProgram
from vertex_buffer_array import StandardShaderVertexArray
import render_systems as rsys
import render_systems_3d as rsys3d
import physic_systems as psys
from maze import _setup_maze
import components_3d as com
import ressources as res

class World(esper.World):
    def __init__(self, resolution):
        super().__init__()

        self.resolution = resolution
        self.standard_shader = StandardShaderProgram()
        self.delta = 0.0
        self.camera_id = 0
        self.light_setup = res.LightSetup(global_ambient=glm.vec3(0.3, 0.3, 0.3))
        self.view_matrix = glm.mat4(1.0)

        self._setup_systems()
        self._setup_entities()
        self.maze = _setup_maze(self)
        self.update_resolution(resolution)

    def cleanup(self):
        """
        cleanup... cleanup so what's the story behind this cleanup method why wouldn't I just use `__del__`?
        Well let me tell you the stupidest thing I've found in Python so far... Do you think that
        `del object` calls `object.__del__`? Well you would be kind of right because it does... but not right away.
        YES yes trust me. It queues the `__del__` call. This is usually fine but not here do you want to guess why?
        Well the `__del__` of the VBOs get called after the destruction of PyOpenGL. Now HOW, tell me HOW should I
        destruct a VBO if the OpenGL bindings are unavailable????

        Now calm down and be happy that you've solved this bug after 4 total hours of debugging...... 
        ~ xFrednet 
        """
        for _entity, vbo in self.get_component(StandardShaderVertexArray):
            vbo.cleanup()

        self.standard_shader.cleanup()

        print("World: Cleanup complete")

    def _setup_systems(self):
        #
        # Physics
        #
        psys.add_physics_systems_to_world(self)

        #
        # Rendering
        #
        # Prepare
        self.add_processor(rsys.PrepareFrameSystem())
        rsys3d.add_3d_render_systems_to_world(self)
        self.add_processor(rsys.FinishFrameSystem())

    def _setup_entities(self):
        # Crappy mixed entity, OOP is a thing... well actually an object...
        # WTF. I'm always amazed by the comments I leave in my code. ~xFrednet 2020.09.23
        vba2 = StandardShaderVertexArray(6)
        vba2.load_position_data([
            -0.1, 0.1, 0.0,
            -0.1, -0.1, 0.0,
            0.1, -0.1, 0.0,
            -0.1, 0.1, 0.0,
            0.1, -0.1, 0.0,
            0.1, 0.1, 0.0
        ])
        vba2.load_normal_data([
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0
        ])

        floor = self.create_entity()
        self.add_component(floor, vba2)
        self.add_component(floor, com.Position(0, 0, -2))
        self.add_component(floor, com.Scale(100))
        self.add_component(floor, com.Rotation())
        self.add_component(floor, com.TransformationMatrix())
        self.add_component(floor, com.ObjectMaterial(diffuse=glm.vec3(0.8, 0.8, 0.8)))

        player_rect = com.Rectangle(1, 1, 1)
        self.player_object = self.create_entity(
              StandardShaderVertexArray.from_rectangle(player_rect),
              com.Position(x=0.0, y=20.0, z=4.0),
              com.Scale(),
              com.Rotation(yaw=3.1),
              com.TransformationMatrix(),
              com.ObjectMaterial(diffuse=glm.vec3(1.0, 0.0, 0.0)),
              com.Velocity(along_world_axis=False),
              com.WasdControlComponent(speed=10),
              com.Home(x=2.0, y=2.0, z=2.0),
              player_rect,
              com.CollisionComponent(),
              com.ArrowKeyRotationControlComponent()
          )

        self.camera_id = self.create_entity(
                com.ThirdPersonCamera(self.player_object, distance=4.0, pitch=-0.5),
                com.CameraOrientation(),
                com.Position()
            )
        
        self.create_entity(
            com.Light(
                position=glm.vec3(10.0, 10.0, 10.0),
                color=glm.vec3(0.7, 0.6, 0.6)))
        self.follow_light = self.create_entity(
            com.Light(
                position=glm.vec3(0.0, 0.0, 10.0),
                color=glm.vec3(1.0, 1.0, 1.0),
                attenuation=glm.vec3(0.25, 0.0, 1.0)))
#        self.camera_id = self.create_entity(
#                com.Position(x=0.0, y=20.0, z=5.0),
#                com.Velocity(along_world_axis=False),
#                com.FreeCamera(),
#                com.Rotation(),
#                com.WasdControlComponent(speed=10),
#                com.CameraOrientation(),
#                com.ArrowKeyRotationControlComponent(),
#                com.ViewMatrix(),
#                com.Home(z=5.0),
#                com.Rectangle(1, 1, 1))


    def update_resolution(self, resolution):
        self.resolution = resolution
        self.standard_shader.update_projection_matrix(resolution)
