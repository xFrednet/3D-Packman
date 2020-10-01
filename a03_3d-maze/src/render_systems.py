from OpenGL import GL as gl
import glm
import glfw
import pygame
from esper import Processor

from shader_program import StandardShaderProgram
from vertex_buffer_array import StandardShaderVertexArray
import components as com

#
# Prepare frame
#
class PrepareFrameSystem(Processor):
    
    def process(self):
        gl.glClearColor(1.0, 0, 1.0, 0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        matrix = self.world.component_for_entity(self.world.camera_id, com.ViewMatrix).value
        self.world.standard_shader.start()
        self.world.standard_shader.set_view_matrix(matrix)
#        self.world.standard_shader.set_projection_matrix(glm.mat4(1.0))
        self.world.standard_shader.stop()

class BuildTranformationMatrixSystem(Processor):
    def process(self):
        for _id, (mat_target, position, scale, rotation) in self.world.get_components(
                com.TransformationMatrix,
                com.Position,
                com.Scale,
                com.Rotation):
            mat = glm.mat4x4(1.0)
            mat = glm.translate(mat, position.value)
            mat = glm.rotate(mat, rotation.value.x, glm.vec3(1, 0, 0))
            mat = glm.rotate(mat, rotation.value.y, glm.vec3(0, 1, 0))
            mat = glm.rotate(mat, rotation.value.z, glm.vec3(0, 0, 1))
            mat = glm.scale(mat, glm.vec3(scale.value, scale.value, scale.value))

            mat_target.value = mat

class BuildViewMatrixSystem(Processor):
    def process(self):
        for _id, (mat_target, position, orientation) in self.world.get_components(
                com.ViewMatrix,
                com.Position,
                com.CameraOrientation):
            mat = glm.mat4x4(1.0)
            mat = glm.rotate(mat, orientation.pitch, glm.vec3(1, 0, 0))
            mat = glm.rotate(mat, orientation.yaw  , glm.vec3(0, 1, 0))
            mat = glm.rotate(mat, orientation.role , glm.vec3(0, 0, 1))

            # u = glm.vec3(mat[0][0], mat[0][1], mat[0][2])
            # v = glm.vec3(mat[1][0], mat[1][1], mat[1][2])
            # n = glm.vec3(mat[2][0], mat[2][1], mat[2][2])
            # mat[3][0] = -(glm.dot(position.value, u))
            # mat[3][1] = -(glm.dot(position.value, v))
            # mat[3][2] = -(glm.dot(position.value, n))

            mat[3][0] = -position.value.x
            mat[3][1] = -position.value.y
            mat[3][2] = -position.value.z

            # I have no and I mean NO idea why we need glm.inverse here
            # We shouldn't need it. the above code is exactly the code I've used in
            # a different project an it works perfectly. But this works and we need to do
            # other stuff so let's leave it!! ~xFrednet
            # https://stackoverflow.com/questions/22194424/creating-a-view-matrix-with-glm
            mat_target.value = glm.inverse(mat)

#
# Draw frame
#
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
            shader.set_transformation_matrix(translation.value)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, vba.vertex_count)
            
            # Unbind the thingies
            gl.glDisableVertexAttribArray(shader.POSITION_ATTR)
            gl.glDisableVertexAttribArray(shader.COLOR_ATTR)
            gl.glBindVertexArray(0)

        shader.stop()

#
# Complete frame
#
class FinishFrameSystem(Processor):

    def process(self):
        pygame.display.flip()
        