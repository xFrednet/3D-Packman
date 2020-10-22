import glm
import esper
import pygame.locals

from components import Transformation


def clamp(value, m_min, m_max):
    if value <= m_min:
        return m_min
    if value >= m_max:
        return m_max
    return value


class FreeCameraControlSystem(esper.Processor):
    def process(self):
        movement = _get_wasd_movement()
        transformation = self.world.component_for_entity(self.world.camera_id, Transformation)
        transformation.position += movement * 0.01


def _get_wasd_movement():
    keys = pygame.key.get_pressed()
    movement = glm.vec3(0.0, 0.0, 0.0)

    # WASD
    if keys[pygame.locals.K_w]:
        movement.z += 1
    if keys[pygame.locals.K_s]:
        movement.z -= 1
    if keys[pygame.locals.K_a]:
        movement.x += 1
    if keys[pygame.locals.K_d]:
        movement.x -= 1
    if keys[pygame.locals.K_SPACE]:
        movement.z += 1
    if keys[pygame.locals.K_LSHIFT]:
        movement.z -= -1

    return movement