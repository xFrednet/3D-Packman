import math
import glm
import esper
import pygame.locals

from components import Transformation, CameraOrientation, FreeCamera


def clamp(value, m_min, m_max):
    if value <= m_min:
        return m_min
    if value >= m_max:
        return m_max
    return value


class FreeCameraControlSystem(esper.Processor):

    MOVEMENT_MULTIPLIER = 8.0
    MAGIC_MULTIPLIER = 20.0
    ROTATION_MULTIPLIER = 3.0

    def process(self):
        movement = _get_wasd_movement()
        movement *= FreeCameraControlSystem.MOVEMENT_MULTIPLIER * self.world.delta
        rotation = _get_arrow_key_movement()
        rotation *= FreeCameraControlSystem.ROTATION_MULTIPLIER * self.world.delta

        if pygame.key.get_pressed()[pygame.locals.K_e]:
            movement *= FreeCameraControlSystem.MAGIC_MULTIPLIER

        for _id, (transformation, orientation, _free_cam) in self.world.get_components(
                Transformation,
                CameraOrientation,
                FreeCamera):
                
            # Rotation
            transformation.rotation.y = clamp(
                    transformation.rotation.y + rotation.y,
                    (math.pi - 0.2) / -2,
                    (math.pi - 0.2) / 2)
            transformation.rotation.x += rotation.x

            # Movement
            transformation.position += _xz_motion_to_object_axis(movement, transformation.rotation)
        
        self.world.height_map_index = _get_number_input(self.world.height_map_index)

def _get_wasd_movement():
    keys = pygame.key.get_pressed()
    movement = glm.vec3()

    # WASD
    if keys[pygame.locals.K_w]:
        movement.z += 1.0
    if keys[pygame.locals.K_s]:
        movement.z -= 1.0
    if keys[pygame.locals.K_a]:
        movement.x -= 1.0
    if keys[pygame.locals.K_d]:
        movement.x += 1.0
    if keys[pygame.locals.K_SPACE]:
        movement.y += 1.0
    if keys[pygame.locals.K_LSHIFT]:
        movement.y -= 1.0

    return movement

def _get_arrow_key_movement():
    keys = pygame.key.get_pressed()
    movement = glm.vec2()

    if keys[pygame.locals.K_UP]:
        movement.y += 1.0
    if keys[pygame.locals.K_DOWN]:
        movement.y -= 1.0
    if keys[pygame.locals.K_LEFT]:
        movement.x -= 1.0
    if keys[pygame.locals.K_RIGHT]:
        movement.x += 1.0
    
    return movement

def _xz_motion_to_object_axis(motion, rotation):
    new_v = glm.vec3()

    new_v.x += math.cos(rotation.x) * motion.z
    new_v.z += math.sin(rotation.x) * motion.z

    new_v.x += math.sin(-rotation.x) * motion.x
    new_v.z += math.cos(-rotation.x) * motion.x

    new_v.y = motion.y

    return new_v

def _get_number_input(default_value):
    keys = pygame.key.get_pressed()

    if keys[pygame.locals.K_0]:
        return 0;
    if keys[pygame.locals.K_1]:
        return 1;
    if keys[pygame.locals.K_2]:
        return 2;
    if keys[pygame.locals.K_3]:
        return 3;
    if keys[pygame.locals.K_4]:
        return 4;
    if keys[pygame.locals.K_5]:
        return 5;
    if keys[pygame.locals.K_6]:
        return 6;
    if keys[pygame.locals.K_7]:
        return 7;
    if keys[pygame.locals.K_8]:
        return 8;
    if keys[pygame.locals.K_9]:
        return 9;
    
    return default_value;

class FreeCameraOrientationSystem(esper.Processor):
    def process(self):
        for _id, (transformation, orientation, _free_cam) in self.world.get_components(
                Transformation,
                CameraOrientation,
                FreeCamera):
            height = math.sin(transformation.rotation.y)
            orientation.look_at = transformation.position + glm.vec3(
                math.cos(transformation.rotation.x) * (1.0 - abs(height)),
                height,
                math.sin(transformation.rotation.x) * (1.0 - abs(height))
            )
