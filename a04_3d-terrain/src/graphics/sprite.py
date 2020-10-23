import os
import pygame.image

class Sprite:
    def __init__(self, file):
        self.pygame_surface = pygame.image.load(os.getcwd() + "/" + file)
        self.width = self.pygame_surface.get_size()[0]
        self.height = self.pygame_surface.get_size()[1]
        self.str_buffer = pygame.image.tostring(self.pygame_surface, "RGB")
        self.depth = 3
    
    def get_avg(self, x, y):
        if (x < 0 or x >= self.width or y < 0 or y > self.height):
            return 0
        
        index = (x + y * self.width) * self.depth

        value = 0
        for i in range(self.depth):
            value += self.str_buffer[index + i]

        return value / self.depth
