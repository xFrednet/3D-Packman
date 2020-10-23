import esper
import pygame
from OpenGL import GL as gl

from components import Transformation, CameraOrientation
from graphics import graphics_math

class PrepareFrameSystem(esper.Processor):
    def process(self):
        position = self.world.component_for_entity(self.world.camera_id, Transformation).position
        orientation = self.world.component_for_entity(self.world.camera_id, CameraOrientation)
        self.world.view_matrix = graphics_math.build_view_matrix(
            position,
            orientation.look_at,
            orientation.up)

        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClearColor(0.2, 0.2, 0.2, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)


class FinishFrameSystem(esper.Processor):
    def process(self):
        pygame.display.flip()
