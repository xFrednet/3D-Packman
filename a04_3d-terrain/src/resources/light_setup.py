import glm

from components import Light

class LightSetup:
    MAX_LIGHT_COUNT = 4

    def __init__(self, global_ambient):
        self.light_positions = [glm.vec3()] * LightSetup.MAX_LIGHT_COUNT
        self.lights = [Light(glm.vec3())] * LightSetup.MAX_LIGHT_COUNT
        self.global_ambient = global_ambient
        self.camera_position = glm.vec3()
        self.light_count = 0