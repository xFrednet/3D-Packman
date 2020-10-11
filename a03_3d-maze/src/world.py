import random
import time

import components_3d as com
import control_system as consys
import esper
import glm
import physic_systems as psys
import render_systems as rsys
import render_systems_3d as rsys3d
import resources as res
from maze import _setup_maze
from shader_program import StandardShaderProgram
from vertex_buffer_array import StandardShaderVertexArray


class World(esper.World):
    def __init__(self, resolution):
        super().__init__()

        self.resolution = resolution
        self.running = True
        self.life = 3
        self.standard_shader = StandardShaderProgram()
        self.delta = 0.00001
        self.light_setup = res.LightSetup(global_ambient=glm.vec3(0.3, 0.3, 0.3))
        self.controls = res.GameControlState()
        self.model_registry = res.ModelRegistry()
        self.camera_id = 0
        self.view_matrix = glm.mat4(1.0)
        self.maze = _setup_maze(self, 30, 30, depth=1.5)
        self._setup_systems()
        self._setup_entities()
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
        consys.add_systems_1_to_world(self)
        psys.add_physics_systems_to_world(self)

        #
        # Rendering
        #
        # Prepare
        consys.add_systems_2_to_world(self)
        self.add_processor(rsys.PrepareFrameSystem())
        rsys3d.add_3d_render_systems_to_world(self)
        self.add_processor(rsys.FinishFrameSystem())

    def _setup_entities(self):
        # Crappy mixed entity, OOP is a thing... well actually an object...
        # WTF. I'm always amazed by the comments I leave in my code. ~xFrednet 2020.09.23
        self.player_object = self.create_entity(
            com.Model3D(self.model_registry.get_model_id(res.ModelRegistry.CUBE)),
            com.Transformation(position=glm.vec3(2.0, 2.0, 2.0)),
            com.TransformationMatrix(),
            com.ObjectMaterial(diffuse=glm.vec3(0.3 * self.life, 0.0, 0.0)),
            com.Velocity(along_world_axis=False),
            com.Home(x=2.0, y=2.0, z=2.0),
            com.BoundingBox(com.Rectangle3D(1, 1, 1)),
            com.CollisionComponent(),
            com.PhysicsObject(),
            com.Light(
                color=glm.vec3(0.6, 0.3, 1.2),
                attenuation=glm.vec3(0.1, 0.0, 1.0))
        )
        # ghost
        ghosts = min((len(self.maze[0]) // 10), self.light_setup.MAX_LIGHT_COUNT - 2)
        if ghosts < 5:
            ghosts = 5
        for i in range(ghosts):
            coord = random.randint(0, len(self.maze[0]) - 1)
            r = random.random()
            g = random.random()
            b = random.random()
            x, y = self.maze[0][coord]
            self.ghost = self.create_entity(
                com.Model3D(self.model_registry.get_model_id(res.ModelRegistry.GHOST)),
                com.Ghost(),
                com.Transformation(position=glm.vec3(x + 1, y + 1, 2.0), scale=glm.vec3(2, 2, 2)),
                com.TransformationMatrix(),
                com.ObjectMaterial(diffuse=glm.vec3(r, g, b)),
                com.Velocity(along_world_axis=True),
                com.BoundingBox(com.Rectangle3D(1, 1, 1)),
                com.CollisionComponent(),
                com.PhysicsObject()
            )

        self.player_cam = self.create_entity(
            com.ThirdPersonCamera(self.player_object, distance=4.0, pitch=-0.5),
            com.CameraOrientation(),
            com.Transformation()
        )

        self.create_entity(
            com.Transformation(position=glm.vec3(self.maze[1].x, self.maze[1].y, 10.0)),
            com.Light(
                color=glm.vec3(0.7, 0.6, 0.6)))
        self.free_cam = self.create_entity(
            com.Transformation(glm.vec3(0.0, 10.0, 5.0)),
            com.Velocity(along_world_axis=False),
            com.FreeCamera(),
            com.CameraOrientation(),
            com.Home(z=5.0))

        self.camera_id = self.player_cam

    def damage_player(self):
        self.life -= 1
        self.component_for_entity(self.player_object, com.ObjectMaterial).diffuse = glm.vec3(0.3 * self.life,
                                                                                             0.0,
                                                                                             0.0)
        for _id, (home, transformation, velocity) in self.get_components(
                com.Home,
                com.Transformation,
                com.Velocity):
            transformation.position = home.position
            velocity.value = glm.vec3()
        if self.life == 0:
            time.sleep(3)
            print('Game Over!')
            self.running = False
        elif self.life == 1:
            print(f'You have {self.life} live left!')
        else:
            print(f'You have {self.life} lives left!')

    def update_resolution(self, resolution):
        self.resolution = resolution
        self.standard_shader.update_projection_matrix(resolution)
