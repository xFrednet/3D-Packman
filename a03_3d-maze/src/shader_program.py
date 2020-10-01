import sys, ctypes
import glm
import math
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
        return gl.glGetUniformLocation(self.program_id, mat_name);

    def start(self):
        gl.glUseProgram(self.program_id)

    def stop(self):
        gl.glUseProgram(0)

class StandardShaderProgram(ShaderProgram):
    
    POSITION_ATTR = 0
    COLOR_ATTR = 1

    TRANSFORMATION_MATRIX_NAME = 'transformationMatrix'
    VIEW_MATRIX_NAME = 'viewMatrix'
    PROJECTION_MATRIX_NAME = 'projectionMatrix'

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

        self.transformation_matrix_location = self._load_uniform_location(StandardShaderProgram.TRANSFORMATION_MATRIX_NAME)
        self.view_matrix_location = self._load_uniform_location(StandardShaderProgram.VIEW_MATRIX_NAME)
        self.projection_matrix_location = self._load_uniform_location(StandardShaderProgram.PROJECTION_MATRIX_NAME)
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
    
    def update_projection_matrix(self, resolution, fov=(math.pi / 2), n=0.5, f=50.0):
        aspect = resolution.x / resolution.y
        
        top = n * math.tan(fov / 2)
        bottom = -top
        right = top * aspect
        left = -right

        mat = glm.mat4(0.0)
        mat[0][0] = (2 * n) / (right - left)
        mat[1][1] = (2 * n) / (top - bottom)
        #mat[2][0] = (left + right) / (right - left)
        #mat[2][1] = (top + bottom) / (top - bottom)
        mat[2][2] = (-(f + n)) / (f - n)
        mat[2][3] = -1
        mat[3][2] = (-(2 * f * n)) / (f - n)

        mat[0][0] =  0.45052942369783683
        mat[0][1] = -0.10435451285616304
        mat[0][2] = -0.2953940042189954
        mat[0][3] = -0.2672612419124244
        
        mat[1][0] =  0.0
        mat[1][1] =  0.5217725642808152
        mat[1][2] = -0.5907880084379908
        mat[1][3] = -0.5345224838248488

        mat[2][0] = -0.15017647456594563
        mat[2][1] = -0.3130635385684891
        mat[2][2] = -0.8861820126569863
        mat[2][3] = -0.8017837257372732

        mat[3][0] = 0.0
        mat[3][1] = 0.0
        mat[3][2] = 3.082884480118567
        mat[3][3] = 3.7416573867739413

        print(mat)

        self.start()
        self.set_projection_matrix(mat)
        self.stop()
