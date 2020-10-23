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

    def _map_uniforms(self):
        self.vs_transformation_matrix_loc = self._load_uniform_location("u_transformation_matrix")
        self.vs_view_matrix_loc = self._load_uniform_location("u_view_matrix")
        self.vs_projection_matrix_loc = self._load_uniform_location("u_projection_matrix")

    def load_transformation_matrix(self, mat):
        gl.glUniformMatrix4fv(self.vs_transformation_matrix_loc, 1, gl.GL_FALSE, glm.value_ptr(mat))

    def load_view_matrix(self, mat):
        gl.glUniformMatrix4fv(self.vs_view_matrix_loc, 1, gl.GL_FALSE, glm.value_ptr(mat))

    def load_projection_matrix(self, mat):
        gl.glUniformMatrix4fv(self.vs_projection_matrix_loc, 1, gl.GL_FALSE, glm.value_ptr(mat))


class TerrainShader(Common3DShaderProgram):
    def __init__(self):
        super().__init__()

        vertex_file = open(os.getcwd() + "/res/shader/terrain.vert")
        fragment_file = open(os.getcwd() + "/res/shader/terrain.frag")
        shaders = {
            "terrain.vert": [gl.GL_VERTEX_SHADER, vertex_file.read()], 
            "terrain.frag": [gl.GL_FRAGMENT_SHADER, fragment_file.read()]
        }
        vertex_file.close()
        fragment_file.close()

        self._compile_shaders(shaders)

        self._map_uniforms()

        print("Terrain shader is alive")
