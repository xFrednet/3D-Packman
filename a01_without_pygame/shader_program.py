import sys, ctypes
from OpenGL import GL as gl

class ShaderProgram:
    def __init__(self):
        self.program_id = gl.glCreateProgram()
        self.shader_ids = []

    def __del__(self):
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

    SHADERS = {
        gl.GL_VERTEX_SHADER: '''\
            #version 330 core
            
            layout(location = 0) in vec3 position;
            layout(location = 1) in vec3 color;

            out vec3 vb_color;

            uniform mat4 transformationMatrix;

            void main(){
                vb_color = color;
                gl_Position = transformationMatrix * vec4(position, 1.0);
                gl_Position.w = 1.0;
            }
            ''',
        gl.GL_FRAGMENT_SHADER: '''\
            #version 330 core
            
            in vec3 vb_color;

            out vec3 color;
            
            void main(){
                color = vec3((vb_color.x + 1) / 2, (vb_color.y + 1) / 2, (vb_color.z + 1) / 2);
            }
            '''
        }

    def __init__(self):
        ShaderProgram.__init__(self)
        self._compile_shaders(StandardShaderProgram.SHADERS)

        self.transformation_matrix_location = self._load_uniform_location(StandardShaderProgram.TRANSFORMATION_MATRIX_NAME)
        print("StandardShaderProgram created")

    def __del__(self):
        print("StandardShaderProgram deleted")

    # The vertex data has the following layout:
    # [
    #   x_0, y_0, z_0,
    #   x_1, y_1, z_1,
    #   x_n, y_n, z_n]
    

    def start(self):
        ShaderProgram.start(self)
    
    def stop(self):
        ShaderProgram.stop(self)
    