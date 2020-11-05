import esper
import glm

from OpenGL import GL as gl

from graphics import PixelVBA, ParticleShader
from components import CameraOrientation

class ParticleRenderSystem(esper.Processor):
    DEFAULT_MAX_VERTEX_COUNT = 256

    def __init__(self):
        super().__init__()
        self._pixel_vbo = PixelVBA(ParticleRenderSystem.DEFAULT_MAX_VERTEX_COUNT)
        
        data = []
        for i in range(ParticleRenderSystem.DEFAULT_MAX_VERTEX_COUNT):
            data.append(float(i))

        self._pixel_vbo.load_indices(data)
        print("ParticleRenderSystem was created: Am I a particle yet?")
    
    def process(self):
        shader: ParticleShader = self.world.particle_shader
        shader.start()
        shader.load_view_matrix(self.world.view_matrix)
        shader.load_projection_matrix(self.world.projection_matrix)
        shader.load_camera_position(self.world.light_setup.camera_position)
        shader.load_camera_up(self.world.component_for_entity(self.world.camera_id, CameraOrientation).up)

        # VBO
        gl.glBindVertexArray(self._pixel_vbo.vba_id)
        gl.glEnableVertexAttribArray(PixelVBA.INDEX_ARRAY_ATTR)

        gl.glDrawArrays(gl.GL_POINTS, 0, self._pixel_vbo.vertex_count)

        # Unbind the thingies
        gl.glDisableVertexAttribArray(PixelVBA.INDEX_ARRAY_ATTR)
        gl.glBindVertexArray(0)
        shader.stop()