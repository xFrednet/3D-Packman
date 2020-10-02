import glm
import esper
import pygame
import pygame.locals
import math

import components as com

def clamp(value, min, max):
    if (value <= min):
        return min
    if (value >= max):
        return max
    
    return value

class MovementSystem(esper.Processor):
    def process(self):
        for _id, (position, velocity) in self.world.get_components(com.Position, com.Velocity):
            position.value = position.value + velocity.value * self.world.delta
            #print(_id, position.value, velocity.value, self.world.delta)

class VelocityToEntityAxis(esper.Processor):
    def process(self):
        for _id, (velocity, rotation) in self.world.get_components(com.Velocity, com.Rotation):
            if (velocity.along_world_axis):
                continue
            
            new_v = glm.vec3()

            new_v.x += math.sin(rotation.yaw) * velocity.value.y
            new_v.y += math.cos(rotation.yaw) * velocity.value.y

            new_v.x += math.cos(-rotation.yaw) * velocity.value.x
            new_v.y += math.sin(-rotation.yaw) * velocity.value.x

            #new_v.z = velocity.value.z

            velocity.value = new_v

class WasdControlSystem(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed()
        for _id, (control, velocity) in self.world.get_components(
                com.WasdControlComponent,
                com.Velocity):
            
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