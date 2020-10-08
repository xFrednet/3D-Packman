import glm
import pygame.locals

from vertex_buffer_array import StandardShaderVertexArray

import components_3d as com

"""
Ressources are data objects that only get initiated by the world as world variables
"""

class GameControlState:
    def __init__(self):
        self.key_swap_camera = pygame.locals.K_m
        self.key_return_to_home = pygame.locals.K_h

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

    def __init__(self):
        self._index = 0
        self._name_registry = {}
        self._model_registry = []

        self._load_default_models()
    
    def _load_default_models(self):
        self.add(ModelRegistry.CUBE, StandardShaderVertexArray.create_cube())

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