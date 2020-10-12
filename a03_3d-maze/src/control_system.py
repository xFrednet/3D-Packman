import math

import components_3d as com
import esper
import glm
import pygame
import pygame.locals
import resources as res


def add_systems_1_to_world(world):
    world.add_processor(GameControlSystem())


def add_systems_2_to_world(world):
    world.add_processor(ThirdPersonCameraSystem())
    world.add_processor(FreeCamOrientation())


def clamp(value, m_min, m_max):
    if value <= m_min:
        return m_min
    if value >= m_max:
        return m_max
    return value


class GameControlSystem(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed()
        controls: res.GameControlState = self.world.controls

        # Swap camera
        if keys[controls.key_swap_camera] and not controls.key_swap_camera_state and controls.allow_camera_swap:
            # swap camera
            self.world._swap_camera()

        # Reset
        if keys[controls.key_return_to_home] and not controls.key_return_to_home_state:
            self.world.home_entities()

        controls.key_swap_camera_state = keys[controls.key_swap_camera]
        controls.key_return_to_home_state = keys[controls.key_return_to_home]

        self._acknowledge_input()

    def _acknowledge_input(self):
        controls: res.GameControlState = self.world.controls

        if controls.control_mode == res.GameControlState.PLAYER_MODE:
            self._wasd_movement(
                self.world.player_object,
                controls.player_speed,
                False,
                0.0)
            self._arrow_key_rotation(self.world.player_object, enable_pitch=False)
            self._mouse_control(self.world.player_object, enable_pitch=False)
            # self._player_jump()
        else:
            self._wasd_movement(
                self.world.free_cam,
                controls.free_camera_speed,
                True,
                controls.free_camera_vertical_speed)
            self._arrow_key_rotation(self.world.free_cam)
            self._mouse_control(self.world.free_cam)

        # self._change_light(self.world.win_object)

    def _wasd_movement(self, entity_id, speed, vertical_movement, vertical_speed):
        keys = pygame.key.get_pressed()
        velocity = self.world.component_for_entity(entity_id, com.Velocity)

        # WASD
        direction = glm.vec3()
        if keys[pygame.locals.K_w]:
            direction.y += 1
        if keys[pygame.locals.K_s]:
            direction.y -= 1
        if keys[pygame.locals.K_a]:
            direction.x += 1
        if keys[pygame.locals.K_d]:
            direction.x -= 1

        if glm.length(direction) > 0.001:
            new_v = glm.normalize(direction) * speed
            velocity.value.x = new_v.x
            velocity.value.y = new_v.y
        else:
            velocity.value.x = 0.0
            velocity.value.y = 0.0

        if vertical_movement:
            velocity.value.z = 0
            if keys[pygame.locals.K_SPACE]:
                velocity.value.z += vertical_speed
            if keys[pygame.locals.K_LSHIFT]:
                velocity.value.z -= vertical_speed

        if keys[pygame.locals.K_p]:
            tra = self.world.component_for_entity(entity_id, com.Transformation)
            print(f"Transformation(Position: {tra.position}, Rotation: {tra.rotation})")

    def _mouse_control(self, entity_id, enable_pitch=True):
        controls: res.GameControlState = self.world.controls
        screen_center = self.world.resolution / 2.0
        
        # If python breaks on this try updating pygame :D
        (is_pressed, _, _, _, _) = pygame.mouse.get_pressed()
        if is_pressed:
            transformation = self.world.component_for_entity(entity_id, com.Transformation)
            #(rel_x, rel_y) = pygame.mouse.get_rel()
            (pos_x, pos_y) = pygame.mouse.get_pos()
            rel_x = screen_center.x - pos_x
            rel_y = screen_center.y - pos_y

            if enable_pitch:
                pitch_change = rel_y * controls.mouse_sensitivity
                transformation.rotation.y = clamp(
                    transformation.rotation.y + pitch_change,
                    (math.pi - 0.2) / -2,
                    (math.pi - 0.2) / 2)

            transformation.rotation.x += rel_x * controls.mouse_sensitivity
            
        pygame.mouse.set_pos([screen_center.x, screen_center.y])

    def _arrow_key_rotation(self, entity_id, enable_pitch=True):
        transformation = self.world.component_for_entity(entity_id, com.Transformation)

        keys = pygame.key.get_pressed()

        if enable_pitch:
            pitch_change = 0.0
            if keys[pygame.locals.K_UP]:
                pitch_change += 0.1
            if keys[pygame.locals.K_DOWN]:
                pitch_change -= 0.1
            transformation.rotation.y = clamp(
                transformation.rotation.y + pitch_change,
                (math.pi - 0.2) / -2,
                (math.pi - 0.2) / 2)

        if keys[pygame.locals.K_LEFT]:
            transformation.rotation.x += 0.1
        if keys[pygame.locals.K_RIGHT]:
            transformation.rotation.x -= 0.1

    def _player_jump(self):
        collision = self.world.component_for_entity(self.world.player_object, com.CollisionComponent)
        if collision.is_colliding_z:
            keys = pygame.key.get_pressed()
            if keys[pygame.locals.K_SPACE]:
                v = self.world.component_for_entity(self.world.player_object, com.Velocity)
                v.value.z += self.world.controls.player_jump_height

    def _change_light(self, entity_id):
        keys = pygame.key.get_pressed()
        light: com.Light = self.world.component_for_entity(entity_id, com.Light)

        if keys[pygame.locals.K_t]:
            light.color.x += 0.01
        if keys[pygame.locals.K_g]:
            light.color.x -= 0.01
        if keys[pygame.locals.K_z]:
            light.color.y += 0.01
        if keys[pygame.locals.K_h]:
            light.color.y -= 0.01
        if keys[pygame.locals.K_u]:
            light.color.z += 0.01
        if keys[pygame.locals.K_h]:
            light.color.z -= 0.01

        if keys[pygame.locals.K_u]:
            light.attenuation.x += 0.01
        if keys[pygame.locals.K_j]:
            light.attenuation.x -= 0.01
        if keys[pygame.locals.K_i]:
            light.attenuation.y += 0.01
        if keys[pygame.locals.K_k]:
            light.attenuation.y -= 0.01
        if keys[pygame.locals.K_o]:
            light.attenuation.z += 0.01
        if keys[pygame.locals.K_l]:
            light.attenuation.z -= 0.01

        if keys[pygame.locals.K_p]:
            print(f"Light(color: {light.color}, attenuation: {light.attenuation})")


class ThirdPersonCameraSystem(esper.Processor):
    def process(self):
        for _id, (transformation, orientation, third_person_cam) in self.world.get_components(
                com.Transformation,
                com.CameraOrientation,
                com.ThirdPersonCamera):
            orientation.look_at = self.world.component_for_entity(third_person_cam.target, com.Transformation).position

            yaw = self.world.component_for_entity(third_person_cam.target, com.Transformation).rotation.x
            pitch = third_person_cam.pitch

            dir_height = math.sin(pitch)
            dir_vec = glm.vec3(
                math.cos(yaw) * (1.0 - abs(dir_height)),
                math.sin(yaw) * (1.0 - abs(dir_height)),
                dir_height
            )

            target_pos = self.world.component_for_entity(third_person_cam.target, com.Transformation).position
            transformation.position = target_pos - (dir_vec * third_person_cam.distance)


class FreeCamOrientation(esper.Processor):
    def process(self):
        for _id, (transformation, orientation, _free_cam) in self.world.get_components(
                com.Transformation,
                com.CameraOrientation,
                com.FreeCamera):
            height = math.sin(transformation.rotation.y)
            orientation.look_at = transformation.position + glm.vec3(
                math.cos(transformation.rotation.x) * (1.0 - abs(height)),
                math.sin(transformation.rotation.x) * (1.0 - abs(height)),
                height
            )
