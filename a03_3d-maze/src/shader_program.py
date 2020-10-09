import math
import sys

import glm
from OpenGL import GL as gl


class ShaderProgram2D:
    def __init__(self):
        self.program_id = gl.glCreateProgram()
        self.shaders = []
        # transformation matrix
        # projection matrix

    def _compile_shaders(self, shaders):
        pass

    def _load_uniform_location(self, mat_name):
        return gl.glGetUniformLocation(self.program_id, mat_name)

    def start(self):
        pass

    def stop(self):
        pass

    def clean_up(self):
        pass


class StandardShaderProgram2D(ShaderProgram2D):
    POSITION_ATTR = 0
    NORMAL_ATTR = 1

    TRANSFORMATION_MATRIX_NAME = 'transformationMatrix'
    VIEW_MATRIX_NAME = 'viewMatrix'
    PROJECTION_MATRIX_NAME = 'projectionMatrix'

    def __init__(self):
        ShaderProgram2D.__init__(self)
        vertex_file = open(sys.path[0] + "/simple2D.vert")
        fragment_file = open(sys.path[0] + "/simple2D.frag")
        shaders = {
            gl.GL_VERTEX_SHADER: vertex_file.read(),
            gl.GL_FRAGMENT_SHADER: fragment_file.read()
        }
        vertex_file.close()
        fragment_file.close()

        self._compile_shaders(shaders)

        self.transformation_matrix_location = self._load_uniform_location(
            StandardShaderProgram2D.TRANSFORMATION_MATRIX_NAME)
        self.view_matrix_location = self._load_uniform_location(StandardShaderProgram2D.VIEW_MATRIX_NAME)
        self.projection_matrix_location = self._load_uniform_location(StandardShaderProgram2D.PROJECTION_MATRIX_NAME)

        print("StandardShaderProgram2D created")

    def start(self):
        ShaderProgram2D.start(self)

    def stop(self):
        ShaderProgram2D.stop(self)

    def set_transformation_matrix(self, matrix):
        gl.glUniformMatrix4fv(self.transformation_matrix_location, 1, gl.GL_FALSE, glm.value_ptr(matrix))

    def set_view_matrix(self, matrix):
        gl.glUniformMatrix4fv(self.view_matrix_location, 1, gl.GL_FALSE, glm.value_ptr(matrix))

    def set_projection_matrix(self, matrix):
        gl.glUniformMatrix4fv(self.projection_matrix_location, 1, gl.GL_FALSE, glm.value_ptr(matrix))

    def update_projection_matrix(self, resolution, fov=(math.pi / 2), n=0.25, f=50.0):
        aspect = resolution.x / resolution.y

        top = n * math.tan(fov / 2)
        bottom = -top
        right = top * aspect
        left = -right

        mat = glm.mat4(0.0)
        mat[0][0] = (2 * n) / (right - left)
        mat[1][1] = (2 * n) / (top - bottom)
        mat[2][0] = (left + right) / (right - left)
        mat[2][1] = (top + bottom) / (top - bottom)
        mat[2][2] = (-(f + n)) / (f - n)
        mat[2][3] = -1
        mat[3][2] = (-(2 * f * n)) / (f - n)

        self.start()
        self.set_projection_matrix(mat)
        self.stop()


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
        for shader_type, shader_src in shaders.items():
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


class StandardShaderProgram(ShaderProgram):
    POSITION_ATTR = 0
    NORMAL_ATTR = 1

    TRANSFORMATION_MATRIX_NAME = 'transformationMatrix'
    VIEW_MATRIX_NAME = 'viewMatrix'
    PROJECTION_MATRIX_NAME = 'projectionMatrix'

    VS_LIGHT_POSITION_NAME = 'u_light_position'
    VS_LIGHT_COUNT_NAME = 'u_light_count'
    VS_CAMERA_POSITION_NAME = 'u_camera_position'

    FS_DIFFUSE_NAME = 'u_diffuse'
    FS_SPECULAR_NAME = 'u_specular'
    FS_SHININESS_NAME = 'u_shininess'

    FS_LIGHT_COLOR_NAME = 'u_light_color'
    FS_LIGHT_ATTENUATION_NAME = 'u_light_attenuation'
    FS_LIGHT_COUNT_NAME = 'u_light_count'
    FS_GLOBAL_AMBIENT_NAME = 'u_global_ambient'

    def __init__(self):
        ShaderProgram.__init__(self)

        vertex_file = open(sys.path[0] + "/simple3D.vert")
        fragment_file = open(sys.path[0] + "/simple3D.frag")
        shaders = {
            gl.GL_VERTEX_SHADER: vertex_file.read(),
            gl.GL_FRAGMENT_SHADER: fragment_file.read()
        }
        vertex_file.close()
        fragment_file.close()

        self._compile_shaders(shaders)

        self.transformation_matrix_location = self._load_uniform_location(
            StandardShaderProgram.TRANSFORMATION_MATRIX_NAME)
        self.view_matrix_location = self._load_uniform_location(StandardShaderProgram.VIEW_MATRIX_NAME)
        self.projection_matrix_location = self._load_uniform_location(StandardShaderProgram.PROJECTION_MATRIX_NAME)

        # This is not beautiful but I've tried. DirectX can actually just load entire
        # structs. This makes stuff like this simple and clean as it only requires one 
        # loading command but who cares it's not like we can rewrite OpenGl now :) ~ xFrednet 2020.10.05
        self.vs_light_position = self._load_uniform_location(StandardShaderProgram.VS_LIGHT_POSITION_NAME)
        self.vs_light_count = self._load_uniform_location(StandardShaderProgram.VS_LIGHT_COUNT_NAME)
        self.vs_camera_position = self._load_uniform_location(StandardShaderProgram.VS_CAMERA_POSITION_NAME)

        self.ps_diffuse = self._load_uniform_location(StandardShaderProgram.FS_DIFFUSE_NAME)
        self.ps_specular = self._load_uniform_location(StandardShaderProgram.FS_SPECULAR_NAME)
        self.ps_shininess = self._load_uniform_location(StandardShaderProgram.FS_SHININESS_NAME)

        self.ps_light_color = self._load_uniform_location(StandardShaderProgram.FS_LIGHT_COLOR_NAME)
        self.ps_light_attenuation = self._load_uniform_location(StandardShaderProgram.FS_LIGHT_ATTENUATION_NAME)
        self.ps_light_count = self._load_uniform_location(StandardShaderProgram.FS_LIGHT_COUNT_NAME)
        self.ps_global_ambient = self._load_uniform_location(StandardShaderProgram.FS_GLOBAL_AMBIENT_NAME)

        print("StandardShaderProgram created")

    # The vertex data has the following layout:
    # [
    #   x_0, y_0, z_0,
    #   x_1, y_1, z_1,
    #   x_n, y_n, z_n]

    def start(self):
        ShaderProgram.start(self)

    def stop(self):
        ShaderProgram.stop(self)

    def set_transformation_matrix(self, matrix):
        gl.glUniformMatrix4fv(self.transformation_matrix_location, 1, gl.GL_FALSE, glm.value_ptr(matrix))

    def set_view_matrix(self, matrix):
        gl.glUniformMatrix4fv(self.view_matrix_location, 1, gl.GL_FALSE, glm.value_ptr(matrix))

    def set_projection_matrix(self, matrix):
        gl.glUniformMatrix4fv(self.projection_matrix_location, 1, gl.GL_FALSE, glm.value_ptr(matrix))

    def set_object_material(self, material):
        gl.glUniform3fv(self.ps_diffuse, 1, glm.value_ptr(material.diffuse))
        gl.glUniform3fv(self.ps_specular, 1, glm.value_ptr(material.specular))
        gl.glUniform1ui(self.ps_shininess, material.shininess)

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
        gl.glUniform1ui(self.ps_light_count, light_setup.light_count)
        gl.glUniform3fv(self.ps_global_ambient, 1, glm.value_ptr(light_setup.global_ambient))
        for index in range(light_setup.light_count):
            gl.glUniform3fv(
                self.ps_light_color + index,
                1,
                glm.value_ptr(light_setup.lights[index].color))
            gl.glUniform3fv(
                self.ps_light_attenuation + index,
                1,
                glm.value_ptr(light_setup.lights[index].attenuation))

    def update_projection_matrix(self, resolution, fov=(math.pi / 2), n=0.5, f=100.0):
        aspect = resolution.x / resolution.y

        top = n * math.tan(fov / 2)
        bottom = -top
        right = top * aspect
        left = -right

        mat = glm.mat4(0.0)
        mat[0][0] = (2 * n) / (right - left)
        mat[1][1] = (2 * n) / (top - bottom)
        mat[2][0] = (left + right) / (right - left)
        mat[2][1] = (top + bottom) / (top - bottom)
        mat[2][2] = (-(f + n)) / (f - n)
        mat[2][3] = -1
        mat[3][2] = (-(2 * f * n)) / (f - n)

        self.start()
        self.set_projection_matrix(mat)
        self.stop()
