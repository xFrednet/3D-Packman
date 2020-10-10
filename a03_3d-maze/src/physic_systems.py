import math
import esper
import glm
import pygame
import pygame.locals

import components_3d as com
import resources as res


def add_physics_systems_to_world(world):
    world.add_processor(VelocityToEntityAxis())
    world.add_processor(GravitySystem())
    world.add_processor(CollisionSystem())
    world.add_processor(MovementSystem())
    world.add_processor(GravitySystem())


class MovementSystem(esper.Processor):
    def process(self):
        for entity_id, (transformation, velocity) in self.world.get_components(com.Transformation, com.Velocity):
            planned_velocity = velocity.value * self.world.delta
            transformation.position = transformation.position + planned_velocity

class GravitySystem(esper.Processor):
    def process(self):
        for entity_id, (velocity, phys, collision) in self.world.get_components(
                com.Velocity, 
                com.PhysicsObject,
                com.CollisionComponent):
            if (collision.is_colliding_z):
                phys.air_time = 0.0
            else:
                gravity = 9.0
                old_grav = phys.air_time**2 * gravity
                phys.air_time += self.world.delta
                new_grav = phys.air_time**2 * gravity
                velocity.value.z -= new_grav - old_grav


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
            hero_target_pos = hero_transformation.position + target_velocity

            hero_collision.is_colliding_x = False
            hero_collision.is_colliding_y = False
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
                
                diff = glm.vec3(
                    villan_tranformation.position.x - hero_target_pos.x,
                    villan_tranformation.position.y - hero_target_pos.y,
                    villan_tranformation.position.z - hero_target_pos.z
                )
                gap = glm.vec3(
                    (hero_rectangle.width + villan_rectangle.width) - abs(diff.x),
                    (hero_rectangle.depth + villan_rectangle.depth) - abs(diff.y),
                    (hero_rectangle.height + villan_rectangle.height) - abs(diff.z)
                )

                old_gap_x = (
                    (hero_rectangle.width + villan_rectangle.width) - 
                    abs(villan_tranformation.position.x - hero_transformation.position.x))
                
                # One side is outside
                if gap.x < 0.0 or gap.y < 0.0 or gap.z < 0.0:
                    continue
                
                old_diff = hero_transformation.position - villan_tranformation.position

                if gap.x <= gap.y and gap.x <= gap.z:
                    offset = hero_rectangle.width + villan_rectangle.width
                    hero_target_pos.x = villan_tranformation.position.x + math.copysign(offset, old_diff.x)
                    hero_collision.is_colliding_x = True
                elif gap.y <= gap.z:
                    if old_gap_x <= 0:
                        continue 
                    offset = hero_rectangle.depth + villan_rectangle.depth
                    hero_target_pos.y = villan_tranformation.position.y + math.copysign(offset, old_diff.y)
                    hero_collision.is_colliding_y = True
                else:
                    offset = hero_rectangle.height + villan_rectangle.height
                    hero_target_pos.z = villan_tranformation.position.z + math.copysign(offset, old_diff.z)
                    hero_collision.is_colliding_z = True
            
            hero_velocity.value = (hero_target_pos - hero_transformation.position) / self.world.delta


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
