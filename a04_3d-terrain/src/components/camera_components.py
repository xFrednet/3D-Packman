import glm

class CameraOrientation:
    def __init__(self):
        self.look_at = glm.vec3(0.0, 0.0, 0.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)