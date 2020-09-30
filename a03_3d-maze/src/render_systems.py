from OpenGL import GL as gl
import glm
import glfw
import pygame
from esper import Processor

from shader_program import StandardShaderProgram
from vertex_buffer_array import StandardShaderVertexArray
import components as com

class PrepareFrameSystem(Processor):
    
    def process(self):
        gl.glClearColor(1.0, 0, 1.0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

class TranslationMatricesSystem(Processor):
    def process(self):
        for _id, (translation, position, scale) in self.world.get_components(com.TransformationMatrix, com.Position, com.Scale):
            mat = glm.mat4x4(1.0)
            mat = glm.translate(mat, glm.vec3(position.value.x, position.value.y, 0.0))
            mat = glm.scale(mat, glm.vec3(scale.value, scale.value, scale.value))
            translation.value = mat

class StandardRenderSystem(Processor):

    VERTEX_POS_INDEX = 0

    def process(self):
        # Ugly hacks, because hacker man!!
        # You should delete this command before you hand in the assignment
        # nawww ~xFrednet
        shader : StandardShaderProgram = self.world.standard_shader
        shader.start()

        for _id, (vba, translation) in self.world.get_components(StandardShaderVertexArray, com.TransformationMatrix):
            # Bind buffers
            gl.glBindVertexArray(vba.vertex_array_id)
            gl.glEnableVertexAttribArray(shader.POSITION_ATTR)
            gl.glEnableVertexAttribArray(shader.COLOR_ATTR)
            
            # Draw the beautiful
            shader.set_transformation_matrix(translation)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, vba.vertex_count)
            
            # Unbind the thingies
            gl.glDisableVertexAttribArray(shader.POSITION_ATTR)
            gl.glDisableVertexAttribArray(shader.COLOR_ATTR)
            gl.glBindVertexArray(0)

        gl.glUseProgram(0)

class FinishFrameSystem(Processor):

    def process(self):
        pygame.display.flip()
        