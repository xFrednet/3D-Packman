import glm


#
# Object physics
#
class Velocity:
    def __init__(self, x=0.0, y=0.0, z=0.0, along_world_axis=True):
        self.value = glm.vec3(x, y, z)
        self.along_world_axis = along_world_axis

class CollisionComponent:
    def __init__(self):
        self.is_colliding_y = False
        self.is_colliding_x = False

#
# Control components
#
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

class Home:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.position = glm.vec3(x, y, z)
        self.orientation = glm.vec3(x, y, z)

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


class FreeCamera:
    pass


class ThirdPersonCamera:
    def __init__(self, target, distance=1.0, pitch=0.0):
        self.target = target
        self.distance = distance
        self.pitch = pitch

#
# Shape
#
class Rectangle:
    """
    This should not be rotated or scaled. Top view:
    
     width (x axis)
    #######
    #  1  # depth (y axis)
    #######
    
    1 is the height (z axis)
    """

    def __init__(self, width, depth, height):
        self.width = width
        self.depth = depth
        self.height = height

    def min_x(self):
        return -self.width / 2

    def max_x(self):
        return self.width / 2

    def min_y(self):
        return -self.depth / 2

    def max_y(self):
        return self.depth / 2

    def min_z(self):
        return -self.height / 2

    def max_z(self):
        return self.height / 2


class Circle:
    def __init__(self, center_x, center_y, radius):
        self.position = glm.vec2(center_x, center_y)
        self.radius = radius


#
# Graphics
#
class ObjectMaterial:
    def __init__(self,
            diffuse=glm.vec3(0, 0, 0),
            specular=glm.vec3(0, 0, 0),
            shininess=5):
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess

class Light:
    def __init__(
            self,
            color,
            attenuation=glm.vec3(0.0, 0.0, 1.0)):
        self.color = color
        self.attenuation = attenuation
        # The attenuation is calculates like: 
        #   d := distance
        #   attenuation.x * d^2 + attenuation.y * d + attenuation.z
