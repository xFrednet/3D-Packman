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
            
            speed = 10.0 * self.world.delta
            direction = glm.vec3()

            # Position
            if keys[pygame.locals.K_w]:
                direction.z += 1
            if keys[pygame.locals.K_s]:
                direction.z -= 1
            if keys[pygame.locals.K_a]:
                direction.x += 1
            if keys[pygame.locals.K_d]:
                direction.x -= 1
            
            direction *= speed
            
            # forward backwards
            position.value.x += direction.z * math.sin(orientation.yaw);
            position.value.z += direction.z * math.cos(orientation.yaw);

            # left right
            position.value.x += direction.x * math.cos(-orientation.yaw);
            position.value.z += direction.x * math.sin(-orientation.yaw);

            
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

            if keys[pygame.locals.K_PAGEUP]:
                orientation.role -= 0.1
            if keys[pygame.locals.K_PAGEDOWN]:
                orientation.role += 0.1