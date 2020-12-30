import components_3d as com
import glm
import resources as res
from OpenGL import GL as gl
from esper import Processor
from shader_program import StandardShaderProgram
from vertex_buffer_array import StandardShaderVertexArray


def add_systems_to_world(world):
    world.add_processor(UpdateLightSetup())
    world.add_processor(BuildTransformationMatrixSystem())
    world.add_processor(Start3DDrawSystem())
    world.add_processor(StandardRenderSystem())
    world.add_processor(ModelRenderer())
    world.add_processor(Stop3DDrawSystem())


#
# Prepare frame
#
class UpdateLightSetup(Processor):
    def process(self):
        light_setup: com.LightSetup = self.world.light_setup
        light_setup.camera_position = self.world.component_for_entity(self.world.camera_id, com.Transformation).position

        index = 0
        for _id, (light, transformation) in self.world.get_components(com.Light, com.Transformation):
            if light.enabled:
                light_setup.light_positions[index] = transformation.position
                light_setup.lights[index] = light
                index += 1
                if index >= res.LightSetup.MAX_LIGHT_COUNT: break

        light_setup.light_count = index
        self.world.light_setup = light_setup


class BuildTransformationMatrixSystem(Processor):
    def process(self):
        for _id, (mat_target, transformation) in self.world.get_components(
                com.TransformationMatrix,
                com.Transformation):
            mat = glm.mat4x4(1.0)
            mat = glm.translate(mat, transformation.position)
            # No rotation for you
            # mat = glm.rotate(mat, transformation.rotation.z, glm.vec3(1, 0, 0))
            mat = glm.rotate(mat, transformation.rotation.y, glm.vec3(1, 0, 0))
            mat = glm.rotate(mat, transformation.rotation.x, glm.vec3(0, 0, 1))
            mat = glm.scale(mat, transformation.scale)

            mat_target.value = mat


#
# Draw frame
#
class Start3DDrawSystem(Processor):
    def process(self):
        # build view matrix
        position = self.world.component_for_entity(self.world.camera_id, com.Transformation).position
        orientation = self.world.component_for_entity(self.world.camera_id, com.CameraOrientation)
        
        forward = glm.normalize(position - orientation.look_at)
        right = glm.normalize(glm.cross(orientation.up, forward))
        up = glm.normalize(glm.cross(forward, right))

        mat = glm.mat4x4(1.0)
        mat[0][0] = right.x
        mat[1][0] = right.y
        mat[2][0] = right.z
        mat[0][1] = up.x
        mat[1][1] = up.y
        mat[2][1] = up.z
        mat[0][2] = forward.x
        mat[1][2] = forward.y
        mat[2][2] = forward.z

        mat[3][0] = -(glm.dot(right, position))
        mat[3][1] = -(glm.dot(up, position))
        mat[3][2] = -(glm.dot(forward, position))
        
        self.world.view_matrix = mat

        # Upload shader data
        self.world.standard_shader.start()
        self.world.standard_shader.set_view_matrix(self.world.view_matrix)
        self.world.standard_shader.load_light_setup(self.world.light_setup)


class StandardRenderSystem(Processor):
    VERTEX_POS_INDEX = 0

    def _create_model_registry(self):
        models = [[]] * self.world.model_registry.get_model_count

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


class ModelRenderer(Processor):
    def __init__(self):
        self.map = None

    def _create_model_registry(self):
        registry: res.ModelRegistry = self.world.model_registry

        model_list = []
        for index in range(registry.get_model_count()):
            model_list.append([])

        for _id, (model, translation, material) in self.world.get_components(
                com.Model3D,
                com.TransformationMatrix,
                com.ObjectMaterial):
            model_list[model.model_id].append([translation, material])

        self.map = model_list

    def process(self):
        # You should delete this command before you hand in the assignment
        shader: StandardShaderProgram = self.world.standard_shader
        registry: res.ModelRegistry = self.world.model_registry

        if self.map is None:
            self._create_model_registry()

        models = self.map
        for index in range(0, len(models)):
            if len(models[index]) == 0:
                continue

            vba = registry.get_model(index)

            # Bind buffers
            gl.glBindVertexArray(vba.vertex_array_id)
            gl.glEnableVertexAttribArray(shader.POSITION_ATTR)
            gl.glEnableVertexAttribArray(shader.NORMAL_ATTR)

            for transformation, material in models[index]:
                shader.set_transformation_matrix(transformation.value)
                shader.set_object_material(material)
                gl.glDrawArrays(gl.GL_TRIANGLES, 0, vba.vertex_count)

            gl.glDisableVertexAttribArray(shader.POSITION_ATTR)
            gl.glDisableVertexAttribArray(shader.NORMAL_ATTR)
            gl.glBindVertexArray(0)


class Stop3DDrawSystem(Processor):
    def process(self):
        self.world.standard_shader.stop()
