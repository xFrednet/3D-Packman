import components_2d as com
import glm
from OpenGL import GL as gl
from esper import Processor
from vertex_buffer_array import StandardShaderVertexArray


def add_2d_render_systems_to_world(world):
    world.add_processor(BuildTransformationMatrixSystem())
    world.add_processor(Start2DDrawSystem())
    world.add_processor(StandardRenderSystem())
    world.add_processor(Stop2DDrawSystem())


class BuildTransformationMatrixSystem(Processor):
    def process(self):
        for _id, (mat_target, position, scale, rotation) in self.world.get_components(
                com.TransformationMatrix,
                com.Position,
                com.Scale,
                com.Rotation):
            mat = glm.mat4x4(1.0)
            mat = glm.translate(mat, position.value)
            # No rotation for you
            # mat = glm.rotate(mat, rotation.role, glm.vec3(1, 0, 0))
            # mat = glm.rotate(mat, rotation.pitch, glm.vec3(0, 1, 0))
            # mat = glm.rotate(mat, rotation.yaw, glm.vec3(0, 0, 1))
            mat = glm.scale(mat, glm.vec3(scale.value, scale.value, scale.value))

            mat_target.value = mat


class Start3DDrawSystem(Processor):
    def process(self):
        # build view matrix
        position = self.world.component_for_entity(self.world.camera_id, com.Position)
        orientation = self.world.component_for_entity(self.world.camera_id, com.CameraOrientation)
        self.world.view_matrix = glm.lookAt(
            position.value,
            orientation.look_at,
            orientation.up)

        # Upload shader data
        self.world.standard_shader.start()
        self.world.standard_shader.set_view_matrix(self.world.view_matrix)
        self.world.standard_shader.load_light_setup(self.world.light_setup)


class StandardRenderSystem(Processor):
    VERTEX_POS_INDEX = 0

    def process(self):
        # Ugly hacks, because hacker man!!
        # You should delete this command before you hand in the assignment
        # nawww ~xFrednet
        shader: StandardShaderProgram = self.world.standard_shader

        for _id, (vba, translation, material) in self.world.get_components(
                StandardShaderVertexArray,
                com.TransformationMatrix,
                com.ObjectMaterial):
            # Bind buffers
            gl.glBindVertexArray(vba.vertex_array_id)
            gl.glEnableVertexAttribArray(shader.POSITION_ATTR)
            gl.glEnableVertexAttribArray(shader.NORMAL_ATTR)

            # Draw the beautiful
            shader.set_transformation_matrix(translation.value)
            shader.set_object_material(material)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, vba.vertex_count)

            # Unbind the thingies
            gl.glDisableVertexAttribArray(shader.POSITION_ATTR)
            gl.glDisableVertexAttribArray(shader.NORMAL_ATTR)
            gl.glBindVertexArray(0)


class Stop3DDrawSystem(Processor):
    def process(self):
        self.world.standard_shader.stop()
