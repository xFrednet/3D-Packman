import glm

#
# Object physics
#
class Velocity:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.value = glm.vec3(x, y, z)

#
# Object Translation
#
class Position:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.value = glm.vec3(x, y, z)

class Scale:
    def __init__(self, scale=1.0):
        self.value = scale

class Rotation:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.value = glm.vec3(x, y, z)

class TransformationMatrix:
    def __init__(self):
        self.value = glm.mat4x4(1.0)

#
# Camera
#
class CameraOrientation:
    def __init__(self):
        self.yaw = 0.0    # turning <- ->
        self.pitch = 0.0  # up and down
        self.up = glm.vec3(0.0, 0.0, 1.0)
        
class ViewMatrix:
    def __init__(self):
        self.value = glm.mat4x4(1.0)