import glm
import pygame.locals

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