import esper
import pygame
from OpenGL import GL as gl


class PrepareFrameSystem(esper.Processor):
    def process(self):
        # gl.glEnable(gl.GL_DEPTH_TEST)
        # gl.glEnable(gl.GL_CULL_FACE)
        gl.glClearColor(0.2, 0.2, 0.2, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


class FinishFrameSystem(esper.Processor):
    def process(self):
        pygame.display.flip()
