import math
import random as rand

import esper
import glm

import resources as res
import components_3d as com


def add_physics_systems_to_world(world):
    world.add_processor(VelocityToEntityAxis())
    world.add_processor(GravitySystem())
    world.add_processor(CollisionSystem())
    world.add_processor(MovementSystem())
    world.add_processor(GhostSystem())
    world.add_processor(WinSystem())
    world.add_processor(LightAnimationSystem())


class WinSystem(esper.Processor):
    def process(self):
        for e_id, (col, win, light) in self.world.get_components(com.CollisionComponent, com.Win, com.Light):
            if win.game_over:
                win.animation_time += self.world.delta
                if win.animation_time < 5.0:
                    if win.won:
                        light.color *= 1.075
                    else:
                        light.attenuation.x -= 0.2 * self.world.delta
            elif self.world.player_object in col.failed:
                win.won = True
                self.world.won_game()


class GhostSystem(esper.Processor):
    SPEED = 5.0
    def process(self):
        for e_id, (ghost_col, ghost, velocity) in self.world.get_components(com.CollisionComponent, com.Ghost,
                                                                            com.Velocity):
            if self.world.player_object in ghost_col.failed:
                self.world.damage_player()

            if ghost_col.is_colliding_y or ghost_col.is_colliding_x or glm.length(velocity.value) < 1:
                velocity.value = glm.normalize(
                    glm.vec3(rand.uniform(-1.0, 1.0), rand.uniform(-1.0, 1.0), 0.0)
                ) * GhostSystem.SPEED


class MovementSystem(esper.Processor):
    def process(self):
        for entity_id, (transformation, velocity) in self.world.get_components(com.Transformation, com.Velocity):
            if self.world.state == res.STATE_RUNNING or \
                    (self.world.state == res.STATE_PAUSED and velocity.allow_paused):
                planned_velocity = velocity.value * self.world.delta
                transformation.position = transformation.position + planned_velocity


class GravitySystem(esper.Processor):
    def process(self):
        for entity_id, (velocity, phys, collision) in self.world.get_components(
                com.Velocity,
                com.PhysicsObject,
                com.CollisionComponent):
            if self.world.state == res.STATE_RUNNING or \
                    (self.world.state == res.STATE_PAUSED and velocity.allow_paused):
                if collision.is_colliding_z:
                    phys.air_time = 0.0
                else:
                    gravity = 9.0
                    old_grav = phys.air_time ** 2 * gravity
                    phys.air_time += self.world.delta
                    new_grav = phys.air_time ** 2 * gravity
                    velocity.value.z -= new_grav - old_grav


class CollisionSystem(esper.Processor):
    """
    Welcome to the world of cheats and liars. We are only doing collision
    detection on the x and y direction. 
    We've now implemented vertical collision detection but I'm still super unhappy with it -.-.
    It's not as smooth as it should be and has multiple bugs
    """

    def process(self):
        if self.world.state == res.STATE_PAUSED:
            return

        for hero_id, (hero_transformation,
                      hero_velocity,
                      hero_bounding_box,
                      hero_collision) in \
                self.world.get_components(com.Transformation,
                                          com.Velocity,
                                          com.BoundingBox,
                                          com.CollisionComponent):

            target_velocity = hero_velocity.value * self.world.delta
            hero_comfort_zone = hero_bounding_box.radius

            hero_rectangle = hero_bounding_box.shape
            hero_target_pos = hero_transformation.position + target_velocity

            hero_collision.is_colliding_x = False
            hero_collision.is_colliding_y = False
            hero_collision.is_colliding_z = False
            hero_collision.failed = []

            for villain_id, (villain_transformation, villain_bounding_box) in self.world.get_components(
                    com.Transformation,
                    com.BoundingBox):

                villain_rectangle = villain_bounding_box.shape

                # Don't hit your self
                if villain_id == hero_id: continue

                # Are they in each others comfort zones?
                if (glm.distance(villain_transformation.position, villain_transformation.position) >
                        (hero_comfort_zone + villain_bounding_box.radius)):
                    continue

                diff = glm.vec3(
                    villain_transformation.position.x - hero_target_pos.x,
                    villain_transformation.position.y - hero_target_pos.y,
                    villain_transformation.position.z - hero_target_pos.z
                )
                gap = glm.vec3(
                    (hero_rectangle.width + villain_rectangle.width) - abs(diff.x),
                    (hero_rectangle.depth + villain_rectangle.depth) - abs(diff.y),
                    (hero_rectangle.height + villain_rectangle.height) - abs(diff.z)
                )

                old_gap_x = (
                        (hero_rectangle.width + villain_rectangle.width) -
                        abs(villain_transformation.position.x - hero_transformation.position.x))

                # One side is outside
                if gap.x < 0.0 or gap.y < 0.0 or gap.z < 0.0: continue
                # Has collided and append
                if not villain_id == 1:
                    hero_collision.failed.append(villain_id)

                old_diff = hero_transformation.position - villain_transformation.position

                if gap.x <= gap.y and gap.x <= gap.z:
                    offset = hero_rectangle.width + villain_rectangle.width
                    hero_target_pos.x = villain_transformation.position.x + math.copysign(offset, old_diff.x)
                    hero_collision.is_colliding_x = True
                elif gap.y <= gap.z:
                    if old_gap_x <= 0:
                        continue
                    offset = hero_rectangle.depth + villain_rectangle.depth
                    hero_target_pos.y = villain_transformation.position.y + math.copysign(offset, old_diff.y)
                    hero_collision.is_colliding_y = True
                else:
                    offset = hero_rectangle.height + villain_rectangle.height
                    hero_target_pos.z = villain_transformation.position.z + math.copysign(offset, old_diff.z)
                    hero_collision.is_colliding_z = True

            hero_velocity.value = (hero_target_pos - hero_transformation.position) / self.world.delta


class VelocityToEntityAxis(esper.Processor):
    def process(self):
        for _id, (velocity, transformation) in self.world.get_components(com.Velocity, com.Transformation):
            if velocity.along_world_axis:
                continue

            rotation = transformation.rotation
            new_v = glm.vec3()

            new_v.x += math.cos(rotation.x) * velocity.value.y
            new_v.y += math.sin(rotation.x) * velocity.value.y

            new_v.x += math.sin(-rotation.x) * velocity.value.x
            new_v.y += math.cos(-rotation.x) * velocity.value.x

            new_v.z = velocity.value.z

            velocity.value = new_v

class LightAnimationSystem(esper.Processor):
    def process(self):
        for _id, (light, animation) in self.world.get_components(com.Light, com.LightAnimation):
            if animation.enabled:
                animation.animation_delta += self.world.delta * animation.delta_factor
                factor = math.sin(animation.animation_delta)
                light.color = animation.base_color + animation.add_color * factor