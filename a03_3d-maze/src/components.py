import glm


#
# Object physics
#
class Velocity:
    def __init__(self, x=0.0, y=0.0, z=0.0, along_world_axis=True):
        self.value = glm.vec3(x, y, z)
        self.along_world_axis = along_world_axis


class WasdControlComponent:
    """
    Note: 
        1. This component required the entity to have a Velocity component
        2. The system moves the component along the XYZ axis"""

    def __init__(self, speed=10.0, active=True):
        self.speed = speed
        self.active = active


class ArrowKeyRotationControlComponent:
    pass


#
# Object Translation
#
class Position:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.value = glm.vec3(x, y, z)


class Scale:
    def __init__(self, scale=1.0):
        self.value = scale


class Home:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.position = glm.vec3(x, y, z)
        self.orientation = glm.vec3(x, y, z)


class Rotation:
    def __init__(self, yaw=0.0, pitch=0.0, role=0):
        self.yaw = yaw
        self.pitch = pitch
        self.role = role


class TransformationMatrix:
    def __init__(self):
        self.value = glm.mat4x4(1.0)


#
# Camera
#
class CameraOrientation:
    def __init__(self):
        self.look_at = glm.vec3(0.0, 1.0, 0.0)
        self.up = glm.vec3(0.0, 0.0, 1.0)


class ViewMatrix:
    def __init__(self):
        self.value = glm.mat4x4(1.0)

#
# Shape
#
class Rectangle:
    """This should not be rotated.
     width (x axis)
    #######
    #  1  # length (y axis)
    #######
    
    1 is the height (z axis)
    """
    def __init__(self, center_x, center_y, width, length, height):
        self.position = glm.vec2(center_x, center_y)
        self.width = width
        self.length = length
        self.height = height

class Circle:
    def __init__(self, center_x, center_y, radius):
        self.position = glm.vec2(center_x, center_y)
        self.radius = radius


#
# Graphics
#
class ObjectMaterial:
    def __init__(self, color):
        self.color = color