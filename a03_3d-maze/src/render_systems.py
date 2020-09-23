from OpenGL import GL as gl
import glm
import glfw
import pygame

# pylint: disable=import-error
from esper import Processor
from shader_program import StandardShaderProgram 
from vertex_buffer_array import StandardShaderVertexArray
from application import Application
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

            # glm::mat4x4 matrix(
            #     glm::vec4(1, 0, 0, 0),
            #     glm::vec4(0, 1, 0, 0),
            #     glm::vec4(0, 0, 1, 0),
            #     glm::vec4(0, 0, 0, 1));
            # matrix = glm::translate(matrix, position);
            # matrix = glm::rotate(matrix, (float)(rotation.x / 180.0 * PI), glm::vec3(1, 0, 0));
            # matrix = glm::rotate(matrix, (float)(rotation.y / 180.0 * PI), glm::vec3(0, 1, 0));
            # matrix = glm::rotate(matrix, (float)(rotation.z / 180.0 * PI), glm::vec3(0, 0, 1));
            # matrix = glm::scale(matrix, glm::vec3(scale, scale, scale));
            # return matrix;

class StandardRenderSystem(Processor):

    VERTEX_POS_INDEX = 0

    def __init__(self):
        self.__shader = StandardShaderProgram()

    def process(self):
        # Ugly hacks, because hacker man!!
        # You should delete this command before you hand in the assignment
        # nawww ~xFrednet
        gl.glUseProgram(self.__shader.program_id)
        transformation_matrix_location = self.__shader.transformation_matrix_location

        for _id, (vba, translation) in self.world.get_components(StandardShaderVertexArray, com.TransformationMatrix):
            # Bind buffers
            gl.glBindVertexArray(vba.vertex_array_id)
            gl.glEnableVertexAttribArray(StandardShaderProgram.POSITION_ATTR)
            gl.glEnableVertexAttribArray(StandardShaderProgram.COLOR_ATTR)
            
            # Draw the beautiful
            gl.glUniformMatrix4fv(transformation_matrix_location, 1, gl.GL_FALSE, glm.value_ptr(translation.value))
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, vba.vertex_count)
            
            # Unbind the thingies
            gl.glDisableVertexAttribArray(StandardShaderProgram.POSITION_ATTR)
            gl.glDisableVertexAttribArray(StandardShaderProgram.COLOR_ATTR)
            gl.glBindVertexArray(0)

        gl.glUseProgram(0)

class FinishFrameSystem(Processor):

    def process(self):
        pygame.display.flip()
        