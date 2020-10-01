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
        for _id, (position, velocity, rotation) in self.world.get_components(com.Position, com.Velocity, com.Rotation):
            #position.value = position.value + velocity.value * self.world.delta
            #rotation.value.z += 1.0 * self.world.delta
            pass

class CameraControlSystem(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed()
        for _id, (orientation, position) in self.world.get_components(com.CameraOrientation, com.Position):
            pitch_change = 0.0
            if keys[pygame.locals.K_UP]:
                pitch_change += 0.1
            if keys[pygame.locals.K_DOWN]:
                pitch_change -= 0.1
            orientation.pitch = clamp(
                orientation.pitch + pitch_change,
                math.pi / -2,
                math.pi / 2)

            if keys[pygame.locals.K_LEFT]:
                orientation.yaw -= 0.1
            if keys[pygame.locals.K_RIGHT]:
                orientation.yaw += 0.1

            # Position
            if keys[pygame.locals.K_w]:
                position.value.z += 0.1
            if keys[pygame.locals.K_s]:
                position.value.z -= 0.1
            if keys[pygame.locals.K_a]:
                position.value.x -= 0.1
            if keys[pygame.locals.K_d]:
                position.value.x += 0.1