import math

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
        self.is_colliding_z = False


class PhysicsObject:
    def __init__(self):
        self.air_time = 0.0


#
# Control components
#
class Home:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.position = glm.vec3(x, y, z)
        self.orientation = glm.vec3(x, y, z)


#
# Object Translation
#
class Transformation:
    def __init__(
            self,
            position=glm.vec3(),
            scale=glm.vec3(1.0, 1.0, 1.0),
            rotation=glm.vec3()):
        self.position = position
        self.scale = scale
        self.rotation = rotation


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
    def __init__(self, position=glm.vec3()):
        self.position = position


class ThirdPersonCamera:
    def __init__(self, target, distance=1.0, pitch=0.0):
        self.target = target
        self.distance = distance
        self.pitch = pitch


#
# Shape
#
class BoundingBox:
    def __init__(self, shape):
        self.shape = shape
        self.radius = shape.get_radius()


class Rectangle3D:
    """
    This should not be rotated or scaled. Top view:
    
     width (x axis)
    #######
    #  1  # depth (y axis)
    #######
    
    1 is the height (z axis)
    """

    def __init__(self, width, depth, height):
        self.width = width / 2.0
        self.depth = depth / 2.0
        self.height = height / 2.0

    def min_x(self):
        return -self.width

    def max_x(self):
        return self.width

    def min_y(self):
        return -self.depth

    def max_y(self):
        return self.depth

    def min_z(self):
        return -self.height

    def max_z(self):
        return self.height

    def get_radius(self):
        return math.sqrt(self.width ** 2 + self.depth ** 2 + self.height ** 2)


#    def get_corners(self, rotation):
#        x_axis = glm.vec3(
#            math.cos(-rotation.x) * self.width,
#            math.sin(-rotation.x) * self.width,
#            0.0)
#        y_axis = glm.vec3(
#            math.sin(rotation.x) * self.depth,
#            math.cos(rotation.x) * self.depth,
#            0.0)
#        z_axis = glm.vec3(0.0, 0.0, self.height)
#
#        return [
#             x_axis + y_axis + z_axis,
#             x_axis - y_axis + z_axis,
#            -x_axis + y_axis + z_axis,
#            -x_axis - y_axis + z_axis,
#
#             x_axis + y_axis - z_axis,
#             x_axis - y_axis - z_axis,
#            -x_axis + y_axis - z_axis,
#            -x_axis - y_axis - z_axis
#        ]


class Circle:
    def __init__(self, center_x, center_y, radius):
        self.position = glm.vec2(center_x, center_y)
        self.radius = radius


#
# Graphics
#
class Model3D:
    def __init__(self, model_id):
        self.model_id = model_id


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
