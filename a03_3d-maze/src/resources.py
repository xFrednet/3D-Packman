import components_3d as com
import glm
from object_loader import ObjLoader
import pygame.locals
from vertex_buffer_array import StandardShaderVertexArray

"""
Resources are data objects that only get initiated by the world as world variables
"""

STATE_RUNNING = 1
STATE_PAUSED = 3

class GameControlState:
    FREE_CAM_MODE = 1
    PLAYER_MODE = 0

    def __init__(self):
        self.control_mode = GameControlState.PLAYER_MODE
        self.allow_camera_swap = True

        self.key_swap_camera = pygame.locals.K_m
        self.key_swap_camera_state = False
        self.key_return_to_home = pygame.locals.K_h
        self.key_return_to_home_state = False

        self.mouse_sensitivity = 0.0025

        self.player_speed = 10.0
        self.player_jump_height = 15.0
        self.free_camera_speed = 10.0
        self.free_camera_vertical_speed = 5.0


class LightSetup:
    MAX_LIGHT_COUNT = 4

    def __init__(self, global_ambient):
        self.light_positions = [glm.vec3()] * LightSetup.MAX_LIGHT_COUNT
        self.lights = [com.Light(glm.vec3())] * LightSetup.MAX_LIGHT_COUNT
        self.global_ambient = global_ambient
        self.camera_position = glm.vec3()
        self.light_count = 0


class ModelRegistry:
    CUBE = "cube"
    GHOST = "ghost"

    def __init__(self):
        self._index = 0
        self._name_registry = {}
        self._model_registry = []

        self._load_default_models()

    def _load_default_models(self):
        self.add(ModelRegistry.CUBE, StandardShaderVertexArray.create_cube())
        self.add(ModelRegistry.GHOST, ObjLoader("res/ghost.obj", swap_yz=True).get_obj())

    def add(self, name, model):
        index = self._index
        self._index += 1

        self._name_registry[name] = index
        self._model_registry.append(model)

    def get_model_id(self, name):
        return self._name_registry[name]

    def get_model(self, model_id):
        return self._model_registry[model_id]

    def get_model_count(self):
        return self._index

    def cleanup(self):
        for vbo in self._model_registry:
            vbo.cleanup()