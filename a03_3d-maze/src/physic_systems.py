import glm
import esper
import pygame
import pygame.locals

import components as com

class MovementSystem(esper.Processor):
    def process(self):
        for _id, (position, velocity, rotation) in self.world.get_components(com.Position, com.Velocity, com.Rotation):
            #position.value = position.value + velocity.value * self.world.delta
            #rotation.value.z += 1.0 * self.world.delta
            pass

class CameraControlSystem(esper.Processor):
    def process(self):
        keys = pygame.key.get_pressed()
        for _id, (orientation) in self.world.get_component(com.CameraOrientation):
            if keys[pygame.locals.K_UP]:
                orientation.pitch += 0.1
            if keys[pygame.locals.K_DOWN]:
                orientation.pitch -= 0.1
            if keys[pygame.locals.K_LEFT]:
                orientation.yaw -= 0.1
            if keys[pygame.locals.K_RIGHT]:
                orientation.yaw += 0.1