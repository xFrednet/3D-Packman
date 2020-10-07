import math

import components_3d as com
import glm
from OpenGL import GL as gl
from esper import Processor
from shader_program import StandardShaderProgram
from vertex_buffer_array import StandardShaderVertexArray
import components_3d as com
import ressources as res


def add_3d_render_systems_to_world(world):
    world.add_processor(FreeCamOrientation())
    world.add_processor(ThirdPersonCameraSystem())
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
        light_setup.camera_position = self.world.component_for_entity(self.world.camera_id, com.Position).value

        index = 0
        for _id, (light, position) in self.world.get_components(com.Light, com.Position):
            light_setup.light_positions[index] = position.value
            light_setup.lights[index] = light
            index += 1
            if (index >= res.LightSetup.MAX_LIGHT_COUNT):
                break
        
        light_setup.light_count = index
        self.world.light_setup = light_setup


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
            mat = glm.scale(mat, scale.value)

            mat_target.value = mat


class ThirdPersonCameraSystem(Processor):
    def process(self):
        for _id, (position, orientation, third_person_cam) in self.world.get_components(
                com.Position,
                com.CameraOrientation,
                com.ThirdPersonCamera):
            orientation.look_at = self.world.component_for_entity(third_person_cam.target, com.Position).value

            yaw = self.world.component_for_entity(third_person_cam.target, com.Rotation).yaw
            pitch = third_person_cam.pitch

            dir_height = math.sin(pitch)
            dir_vec = glm.vec3(
                math.sin(yaw) * (1.0 - abs(dir_height)),
                math.cos(yaw) * (1.0 - abs(dir_height)),
                dir_height
            )

            target_pos = self.world.component_for_entity(third_person_cam.target, com.Position).value
            position.value = target_pos + ((dir_vec * -1) * third_person_cam.distance)


class FreeCamOrientation(Processor):
    def process(self):
        for _id, (position, orientation, rotation, _free_cam) in self.world.get_components(
                com.Position,
                com.CameraOrientation,
                com.Rotation,
                com.FreeCamera):
            height = math.sin(rotation.pitch)
            orientation.look_at = position.value + glm.vec3(
                math.sin(-rotation.yaw) * (1.0 - abs(height)),
                math.cos(-rotation.yaw) * (1.0 - abs(height)),
                height
            )


#
# Draw frame
#
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
        
        model_list = [[]] * registry.get_model_count()
        
        for _id, (model, translation, material) in self.world.get_components(
                com.Model3D,
                com.TransformationMatrix,
                com.ObjectMaterial):

            model_list[model.model_id].append((translation, material))
        
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
