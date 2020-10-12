import random

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
        self.state = res.STATE_RUNNING
        self.life = 3
        self.level = 1
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
        self._setup_level_objects()
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

        self.model_registry.cleanup()
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
        rsys3d.add_systems_to_world(self)
        self.add_processor(rsys.FinishFrameSystem())

    def _setup_entities(self):
        # Crappy mixed entity, OOP is a thing... well actually an object...
        # WTF. I'm always amazed by the comments I leave in my code. ~xFrednet 2020.09.23
        position = glm.vec3(2.0, 2.0, 1.0)
        rotation = glm.vec3(0.0, 0.0, 0.0)
        self.player_object = self.create_entity(
            com.Model3D(self.model_registry.get_model_id(res.ModelRegistry.CUBE)),
            com.Transformation(position=position, rotation=rotation),
            com.TransformationMatrix(),
            com.ObjectMaterial(diffuse=glm.vec3(1.0, 0.3, 0.3)),
            com.Velocity(along_world_axis=False),
            com.Home(position, rotation),
            com.BoundingBox(com.Rectangle3D(1, 1, 1)),
            com.CollisionComponent(),
            com.PhysicsObject(),
            com.Light(
                color=glm.vec3(0.6, 0.3, 1.2),
                attenuation=glm.vec3(0.1, 0.0, 1.0))
        )

        self.player_cam = self.create_entity(
            com.ThirdPersonCamera(self.player_object, distance=4.0, pitch=-0.5),
            com.CameraOrientation(),
            com.Transformation()
        )

        position = glm.vec3(-5.0, -5.0, 20.0)
        rotation = glm.vec3(0.9, -0.5, 0.0)
        self.free_cam = self.create_entity(
            com.Transformation(position=position, rotation=rotation),
            com.Velocity(along_world_axis=False, allow_paused=True),
            com.FreeCamera(),
            com.CameraOrientation(),
            com.Home(position, rotation))

        self.camera_id = self.player_cam

    def _setup_level_objects(self):
        # Central light
        self.create_entity(
            com.Transformation(position=glm.vec3(self.maze.center.x, self.maze.center.y, 20.0)),
            com.Light(
                color=glm.vec3(0.5, 0.4, 0.4)))

        # ghost
        ghosts = 5
        print(len(self.maze.empty_areas_loc))
        if self.level == 3:
            ghosts = (len(self.maze.empty_areas_loc) // 10)
        elif self.level == 2:
            ghosts = (len(self.maze.empty_areas_loc) // 20)
        if ghosts < 5:
            ghosts = 5
        for i in range(ghosts):
            coord = random.randint(0, len(self.maze.empty_areas_loc) - 1)
            r = random.random()
            g = random.random()
            b = random.random()
            x, y = self.maze.empty_areas_loc[coord]
            position = glm.vec3(x, y, 2.0)
            self.ghost = self.create_entity(
                com.Model3D(self.model_registry.get_model_id(res.ModelRegistry.GHOST)),
                com.Ghost(),
                com.Transformation(position=position, scale=glm.vec3(2.0, 2.0, 2.0)),
                com.TransformationMatrix(),
                com.ObjectMaterial(diffuse=glm.vec3(r, g, b)),
                com.Velocity(random.uniform(-1, 1), random.uniform(-1, 1), 0, along_world_axis=True),
                com.BoundingBox(com.Rectangle3D(2, 2, 2)),
                com.CollisionComponent(),
                com.PhysicsObject(),
                com.Home(position=position)
            )

        self.win_object = self.create_entity(
            com.Transformation(position=glm.vec3(self.maze.center.x, self.maze.center.y, 1.0)),
            com.Win(),
            com.Velocity(),
            com.BoundingBox(com.Rectangle3D(1.0, 1.0, 1.0)),
            com.CollisionComponent(),
            com.Light(
                color=glm.vec3(1.0, 0.8, 0.0),
                attenuation=glm.vec3(0.35, -0.36, 0.1))
        )

    def damage_player(self):
        self.life -= 1
        self.component_for_entity(self.player_object, com.ObjectMaterial).diffuse *= 0.7

        if self.life > 1:
            print(f'You have {self.life} lives left!')
            self.home_entities()
        elif self.life == 1:
            print(f'You have {self.life} life left!')
            self.home_entities()
        else:
            print('Game Over!')
            self.end_game()

    def won_game(self):
        print('You winted!')
        self.end_game()

    def end_game(self):
        # Clear collisions
        for _id, collision in self.get_component(com.CollisionComponent):
            collision.failed.clear()

        # Setup top-down camera
        transform = self.component_for_entity(self.free_cam, com.Transformation)
        transform.position.x = self.maze.center.x
        transform.position.y = self.maze.center.y
        transform.position.z = 50.0
        transform.rotation = glm.vec3(0.0, -1.4, 0.0)
        self.controls.allow_camera_swap = False
        if self.controls.control_mode == res.GameControlState.PLAYER_MODE:
            self._swap_camera()

        # Animation
        self.component_for_entity(self.win_object, com.Win).game_over = True

    def _swap_camera(self):
        controls: res.GameControlState = self.controls
        if controls.control_mode == res.GameControlState.PLAYER_MODE:
            self.camera_id = self.free_cam
            controls.control_mode = res.GameControlState.FREE_CAM_MODE
            self.state = res.STATE_PAUSED
        else:
            self.camera_id = self.player_cam
            controls.control_mode = res.GameControlState.PLAYER_MODE
            self.state = res.STATE_RUNNING

    def home_entities(self):
        for _id, (home, transformation, velocity) in self.get_components(
                com.Home,
                com.Transformation,
                com.Velocity):
            transformation.position = home.position
            transformation.rotation = home.rotation
            velocity.value = glm.vec3()

    def update_resolution(self, resolution):
        self.resolution = resolution
        self.standard_shader.update_projection_matrix(resolution)
