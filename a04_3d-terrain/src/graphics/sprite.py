import os
import pygame.image

from OpenGL import GL as gl

from components import Texture2D

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
        
    def gen_texture(self):
        texture = gl.glGenTextures(1)

        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)

        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, self.width, self.height, 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE,
                pygame.image.tostring(self.pygame_surface, "RGBA"))

        return Texture2D(texture)
