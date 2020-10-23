import math
import os
import sys

import glm
from OpenGL import GL as gl


class ShaderProgram:
    def __init__(self):
        self.program_id = gl.glCreateProgram()
        self.shader_ids = []

    def cleanup(self):
        for shader_id in self.shader_ids:
            gl.glDetachShader(self.program_id, shader_id)
            gl.glDeleteShader(shader_id)
        gl.glUseProgram(0)
        gl.glDeleteProgram(self.program_id)

    def _compile_shaders(self, shaders):
        for name, info in shaders.items():
            shader_type = info[0]
            shader_src = info[1]
            
            print("Compiling: ", name)
            shader_id = gl.glCreateShader(shader_type)
            gl.glShaderSource(shader_id, shader_src)

            gl.glCompileShader(shader_id)

            # check if compilation was successful
            gl.glGetShaderiv(shader_id, gl.GL_COMPILE_STATUS)
            info_log_len = gl.glGetShaderiv(shader_id, gl.GL_INFO_LOG_LENGTH)
            if info_log_len:
                logmsg = gl.glGetShaderInfoLog(shader_id)
                print(logmsg)
                sys.exit(10)

            gl.glAttachShader(self.program_id, shader_id)
            self.shader_ids.append(shader_id)

        gl.glLinkProgram(self.program_id)

        # check if linking was successful
        gl.glGetProgramiv(self.program_id, gl.GL_LINK_STATUS)
        info_log_len = gl.glGetProgramiv(self.program_id, gl.GL_INFO_LOG_LENGTH)
        if info_log_len:
            logmsg = gl.glGetProgramInfoLog(self.program_id)
            print(logmsg)
            sys.exit(11)

    def _load_uniform_location(self, mat_name):
        return gl.glGetUniformLocation(self.program_id, mat_name)

    def start(self):
        gl.glUseProgram(self.program_id)

    def stop(self):
        gl.glUseProgram(0)


class Common3DShaderProgram(ShaderProgram):
    def __init__(self):
        super().__init__()

        self.vs_transformation_matrix_loc = None
        self.vs_view_matrix_loc = None
        self.vs_projection_matrix_loc = None

        self.vs_light_position = None
        self.vs_light_count = None
        self.vs_camera_position = None

        self.fs_diffuse = None
        self.fs_specular = None
        self.fs_shininess = None

        self.fs_light_color = None
        self.fs_light_attenuation = None
        self.fs_light_count = None
        self.fs_global_ambient = None

    def _map_uniforms(self):
        self.vs_transformation_matrix_loc = self._load_uniform_location("u_transformation_matrix")
        self.vs_view_matrix_loc = self._load_uniform_location("u_view_matrix")
        self.vs_projection_matrix_loc = self._load_uniform_location("u_projection_matrix")

        self.vs_light_position = self._load_uniform_location("u_light_position")
        self.vs_light_count = self._load_uniform_location("u_light_count")
        self.vs_camera_position = self._load_uniform_location("u_camera_position")

        self.fs_diffuse = self._load_uniform_location("u_diffuse")
        self.fs_specular = self._load_uniform_location("u_specular")
        self.fs_shininess = self._load_uniform_location("u_shininess")
        
        self.fs_light_color = self._load_uniform_location("u_light_color")
        self.fs_light_attenuation = self._load_uniform_location("u_light_attenuation")
        self.fs_light_count = self._load_uniform_location("u_light_count")
        self.fs_global_ambient = self._load_uniform_location("u_global_ambient")

    def load_transformation_matrix(self, mat):
        gl.glUniformMatrix4fv(self.vs_transformation_matrix_loc, 1, gl.GL_FALSE, glm.value_ptr(mat))

    def load_view_matrix(self, mat):
        gl.glUniformMatrix4fv(self.vs_view_matrix_loc, 1, gl.GL_FALSE, glm.value_ptr(mat))

    def load_projection_matrix(self, mat):
        gl.glUniformMatrix4fv(self.vs_projection_matrix_loc, 1, gl.GL_FALSE, glm.value_ptr(mat))
    
    def load_object_material(self, material):
        gl.glUniform3fv(self.fs_diffuse, 1, glm.value_ptr(material.diffuse))
        gl.glUniform3fv(self.fs_specular, 1, glm.value_ptr(material.specular))
        gl.glUniform1ui(self.fs_shininess, material.shininess)
    
    def load_light_setup(self, light_setup):
        # Vertex Shader
        gl.glUniform1ui(self.vs_light_count, light_setup.light_count)
        gl.glUniform3fv(self.vs_camera_position, 1, glm.value_ptr(light_setup.camera_position))
        for index in range(light_setup.light_count):
            gl.glUniform3fv(
                self.vs_light_position + index,
                1,
                glm.value_ptr(light_setup.light_positions[index]))

        # Fragment shader
        gl.glUniform1ui(self.fs_light_count, light_setup.light_count)
        gl.glUniform3fv(self.fs_global_ambient, 1, glm.value_ptr(light_setup.global_ambient))
        for index in range(light_setup.light_count):
            gl.glUniform3fv(
                self.fs_light_color + index,
                1,
                glm.value_ptr(light_setup.lights[index].color))
            gl.glUniform3fv(
                self.fs_light_attenuation + index,
                1,
                glm.value_ptr(light_setup.lights[index].attenuation))


class TerrainShader(Common3DShaderProgram):
    def __init__(self):
        super().__init__()

        vertex_file = open(os.getcwd() + "/res/shader/terrain.vert")
        geometry_file = open(os.getcwd() + "/res/shader/terrain.geom")
        fragment_file = open(os.getcwd() + "/res/shader/terrain.frag")
        shaders = {
            "terrain.vert": [gl.GL_VERTEX_SHADER, vertex_file.read()], 
            "terrain.geom": [gl.GL_GEOMETRY_SHADER, geometry_file.read()],
            "terrain.frag": [gl.GL_FRAGMENT_SHADER, fragment_file.read()]
        }
        vertex_file.close()
        geometry_file.close()
        fragment_file.close()

        self._compile_shaders(shaders)

        self._map_uniforms()

        print("Terrain shader is alive")
