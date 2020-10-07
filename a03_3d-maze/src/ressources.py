import glm

"""
Ressources are data objects that only get initiated by the world as world variables
"""

class LightSetup:
    def __init__(self, global_ambient):
        self.lights = []
        self.global_ambient = global_ambient
        self.camera_position = glm.vec3()
        self.light_count = 0