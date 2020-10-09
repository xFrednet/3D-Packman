import math
import esper
import glm
import pygame
import pygame.locals

import components_3d as com
import ressources as res


def add_physics_systems_to_world(world):
    world.add_processor(VelocityToEntityAxis())
    world.add_processor(CollisionSystem())
    world.add_processor(MovementSystem())


class MovementSystem(esper.Processor):
    def process(self):
        for entity_id, (transformation, velocity) in self.world.get_components(com.Transformation, com.Velocity):
            planned_velocity = velocity.value * self.world.delta

            if (self.world.has_component(entity_id, com.CollisionComponent)):
                collision = self.world.component_for_entity(entity_id, com.CollisionComponent)
                if (collision.is_colliding_x):
                    planned_velocity.x = 0.0
                if (collision.is_colliding_y):
                    planned_velocity.y = 0.0
                if (collision.is_colliding_z):
                    planned_velocity.z = 0.0

            transformation.position = transformation.position + planned_velocity
            # print(_id, position.value, velocity.value, self.world.delta)


class CollisionSystem(esper.Processor):
    """
    Welcome to the world of cheats and lairs. We are only doing collision
    detection on the x and y direction. 
    """

    def process(self):
        for hero_id, (hero_transformation, hero_velocity, hero_bounding_box, hero_collision) in self.world.get_components(
                com.Transformation,
                com.Velocity,
                com.BoundingBox,
                com.CollisionComponent):

            target_velocity = hero_velocity.value * self.world.delta
            hero_confort_zone = hero_bounding_box.radius

            hero_rectangle = hero_bounding_box.shape
            hero_min_x = hero_transformation.position.x + target_velocity.x + hero_rectangle.min_x()
            hero_max_x = hero_transformation.position.x + target_velocity.x + hero_rectangle.max_x()
            hero_min_y = hero_transformation.position.y + target_velocity.y + hero_rectangle.min_y()
            hero_max_y = hero_transformation.position.y + target_velocity.y + hero_rectangle.max_y()
            hero_max_z = hero_transformation.position.z + target_velocity.z + hero_rectangle.max_z()
            hero_min_z = hero_transformation.position.z + target_velocity.z + hero_rectangle.min_z()
            hero_collision.is_colliding_y = False
            hero_collision.is_colliding_x = False
            hero_collision.is_colliding_z = False

            for villan_id, (villan_tranformation, villan_bounding_box) in self.world.get_components(
                    com.Transformation,
                    com.BoundingBox):

                villan_rectangle = villan_bounding_box.shape

                # Don't hit your self
                if (villan_id == hero_id):
                    continue
                
                # Are they in each others confort zones?
                if (glm.distance(villan_tranformation.position, villan_tranformation.position) > 
                        (hero_confort_zone + villan_bounding_box.radius)):
                    continue

                # Positions
                villan_min_x = villan_tranformation.position.x + villan_rectangle.min_x()
                villan_max_x = villan_tranformation.position.x + villan_rectangle.max_x()
                villan_min_y = villan_tranformation.position.y + villan_rectangle.min_y()
                villan_max_y = villan_tranformation.position.y + villan_rectangle.max_y()
                villan_min_z = villan_tranformation.position.z + villan_rectangle.min_z()
                villan_max_z = villan_tranformation.position.z + villan_rectangle.max_z()

                # Collision testing
                if (hero_max_y < villan_min_y or
                        hero_min_y >= villan_max_y):
                    continue
                if (hero_max_x < villan_min_x or
                        hero_min_x >= villan_max_x):
                    continue
                if (hero_max_z < villan_min_z or
                        hero_min_z >= villan_max_z):
                    continue

                # Find side
                hero_min_x_old = hero_transformation.position.x + hero_rectangle.min_x()
                hero_max_x_old = hero_transformation.position.x + hero_rectangle.max_x()
                hero_min_y_old = hero_transformation.position.y + hero_rectangle.min_y()
                hero_max_y_old = hero_transformation.position.y + hero_rectangle.max_y()
                hero_min_z_old = hero_transformation.position.z + hero_rectangle.min_z()
                hero_max_z_old = hero_transformation.position.z + hero_rectangle.max_z()

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

                if (hero_collision.is_colliding_x and
                        hero_collision.is_colliding_y and
                        hero_collision.is_colliding_z):
                    return


class VelocityToEntityAxis(esper.Processor):
    def process(self):
        for _id, (velocity, transformation) in self.world.get_components(com.Velocity, com.Transformation):
            if velocity.along_world_axis:
                continue
            
            rotation = transformation.rotation
            new_v = glm.vec3()

            new_v.x += math.sin(rotation.x) * velocity.value.y
            new_v.y += math.cos(rotation.x) * velocity.value.y

            new_v.x += math.cos(-rotation.x) * velocity.value.x
            new_v.y += math.sin(-rotation.x) * velocity.value.x

            new_v.z = velocity.value.z

            velocity.value = new_v
