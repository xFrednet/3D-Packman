from OpenGL import GL as gl
import glm
import glfw
import pygame
from esper import Processor
import math

from shader_program import StandardShaderProgram
from vertex_buffer_array import StandardShaderVertexArray
import components_3d as com
import ressources as res

def add_3d_render_systems_to_world(world):
    world.add_processor(FreeCamOrientation())
    world.add_processor(ThirdPersonCameraSystem())
    world.add_processor(UpdateLightSetup())
    world.add_processor(BuildTranformationMatrixSystem())
    
    world.add_processor(Start3DDrawSystem())
    world.add_processor(StandardRenderSystem())
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

class BuildTranformationMatrixSystem(Processor):
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