import glm
import esper
import pygame
import pygame.locals
import math

import components as com


def clamp(value, m_min, m_max):
    if value <= m_min:
        return m_min
    if value >= m_max:
        return m_max
    return value


class ResetSystem(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed()
        for _id, (home, position) in self.world.get_components(com.Home, com.Position):
            # Home reset
            if keys[pygame.locals.K_h]:
                position.value = home.position


class MovementSystem(esper.Processor):
    def process(self):
        for entity_id, (position, velocity) in self.world.get_components(com.Position, com.Velocity):
            planned_velocity = velocity.value * self.world.delta

            if (self.world.has_component(entity_id, com.CollisionComponent)):
                collision = self.world.component_for_entity(entity_id, com.CollisionComponent)
                if (collision.is_colliding_x):
                    planned_velocity.x = 0.0
                if (collision.is_colliding_y):
                    planned_velocity.y = 0.0

            position.value = position.value + planned_velocity
            # print(_id, position.value, velocity.value, self.world.delta)


class CollisionSystem(esper.Processor):
    """
    Welcome to the world of cheats and lairs. We are only doing collision
    detection on the x and y direction. 
    """

    def process(self):
        for hero_id, (hero_position, hero_velocity, hero_rectangle, hero_collision) in self.world.get_components(
                com.Position,
                com.Velocity,
                com.Rectangle,
                com.CollisionComponent):

            target_velocity = hero_velocity.value * self.world.delta

            hero_min_x = hero_position.value.x + target_velocity.x + hero_rectangle.min_x()
            hero_max_x = hero_position.value.x + target_velocity.x + hero_rectangle.max_x()
            hero_min_y = hero_position.value.y + target_velocity.y + hero_rectangle.min_y()
            hero_max_y = hero_position.value.y + target_velocity.y + hero_rectangle.max_y()
            hero_max_z = hero_position.value.z + target_velocity.z + hero_rectangle.max_z()
            hero_min_z = hero_position.value.z + target_velocity.z + hero_rectangle.min_z()
            hero_collision.is_colliding_y = False
            hero_collision.is_colliding_x = False

            for villan_id, (villan_position, villan_rectangle) in self.world.get_components(
                    com.Position,
                    com.Rectangle):

                # Don't hit your self
                if (villan_id == hero_id):
                    continue

                # Positions
                villan_min_x = villan_position.value.x + villan_rectangle.min_x()
                villan_max_x = villan_position.value.x + villan_rectangle.max_x()
                villan_min_y = villan_position.value.y + villan_rectangle.min_y()
                villan_max_y = villan_position.value.y + villan_rectangle.max_y()
                villan_min_z = villan_position.value.z + villan_rectangle.min_z()
                villan_max_z = villan_position.value.z + villan_rectangle.max_z()

                # Collision testing
                if (hero_max_x < villan_min_x or
                        hero_min_x >= villan_max_x):
                    continue
                if (hero_max_y < villan_min_y or
                        hero_min_y >= villan_max_y):
                    continue
                if (hero_max_z < villan_min_z or
                        hero_min_z >= villan_max_z):
                    continue
                

                # Find side
                hero_min_x_old = hero_position.value.x + hero_rectangle.min_x()
                hero_max_x_old = hero_position.value.x + hero_rectangle.max_x()
                hero_min_y_old = hero_position.value.y + hero_rectangle.min_y()
                hero_max_y_old = hero_position.value.y + hero_rectangle.max_y()

                if hero_max_y_old > villan_min_y and hero_min_y_old <= villan_max_y:
                    if hero_min_x_old > villan_max_x and hero_min_x <= villan_max_x:
                        hero_collision.is_colliding_x = True
                    elif hero_max_x_old < villan_min_x and hero_max_x >= villan_min_x:
                        hero_collision.is_colliding_x = True

                if hero_max_x_old > villan_min_x and hero_min_x_old <= villan_max_x:
                    if hero_min_y_old > villan_max_y and hero_min_y <= villan_max_y:
                        hero_collision.is_colliding_y = True
                    elif hero_max_y_old < villan_min_y and hero_max_y >= villan_min_y:
                        hero_collision.is_colliding_y = True

                if hero_collision.is_colliding_x and hero_collision.is_colliding_y:
                    return


class VelocityToEntityAxis(esper.Processor):
    def process(self):
        for _id, (velocity, rotation) in self.world.get_components(com.Velocity, com.Rotation):
            if velocity.along_world_axis:
                continue

            new_v = glm.vec3()

            new_v.x += math.sin(rotation.yaw) * velocity.value.y
            new_v.y += math.cos(rotation.yaw) * velocity.value.y

            new_v.x += math.cos(-rotation.yaw) * velocity.value.x
            new_v.y += math.sin(-rotation.yaw) * velocity.value.x

            new_v.z = velocity.value.z

            velocity.value = new_v


class WasdControlSystem(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed()
        for _id, (control, velocity, position) in self.world.get_components(
                com.WasdControlComponent,
                com.Velocity,
                com.Position):

            # Active check
            if not control.active:
                continue

            direction = glm.vec3()

            # WASD
            if keys[pygame.locals.K_w]:
                direction.y += 1
            if keys[pygame.locals.K_s]:
                direction.y -= 1
            if keys[pygame.locals.K_a]:
                direction.x -= 1
            if keys[pygame.locals.K_d]:
                direction.x += 1

            if glm.length(direction) > 0.001:
                velocity.value = glm.normalize(direction) * control.speed
            else:
                velocity.value = glm.vec3()

            if keys[pygame.locals.K_SPACE]:
                velocity.value.z += control.speed
            if keys[pygame.locals.K_LSHIFT]:
                velocity.value.z -= control.speed

            self.world.component_for_entity(self.world.follow_light, com.Light).position = position.value


class CameraControlSystem(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed()
        for _id, (rotation, _control) in self.world.get_components(com.Rotation, com.ArrowKeyRotationControlComponent):

            pitch_change = 0.0
            if keys[pygame.locals.K_UP]:
                pitch_change += 0.1
            if keys[pygame.locals.K_DOWN]:
                pitch_change -= 0.1
            rotation.pitch = clamp(
                rotation.pitch + pitch_change,
                (math.pi - 0.2) / -2,
                (math.pi - 0.2) / 2)

            if keys[pygame.locals.K_LEFT]:
                rotation.yaw -= 0.1
            if keys[pygame.locals.K_RIGHT]:
                rotation.yaw += 0.1
