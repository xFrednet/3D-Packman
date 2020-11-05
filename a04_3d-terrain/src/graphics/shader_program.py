import math
import os
import sys
import glm

from OpenGL import GL as gl

from components import ParticleEmitter

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
            
            print("    > Compiling: ", name)
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


class Common3DLightShaderProgram(Common3DShaderProgram):
    """
    Looking at this inheritance cancer makes me realize that I should have
    build these in a modular fashion as well. Good to know for the rework but this
    is also good enough for now ^^.
    """

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

        self.fs_light_color = self._load_uniform_location("u_light_color")
        self.fs_light_attenuation = self._load_uniform_location("u_light_attenuation")
        self.fs_light_count = self._load_uniform_location("u_light_count")
        self.fs_global_ambient = self._load_uniform_location("u_global_ambient")
    
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


class TerrainShader(Common3DLightShaderProgram):
    def __init__(self):
        super().__init__()

        cur_dir = os.getcwd()
        vertex_path = "../res/shader/terrain.vert"
        fragment_path = "../res/shader/terrain.frag"
        geometry_path = "../res/shader/terrain.geom"
        vertex_file = open(os.path.join(cur_dir, vertex_path))
        fragment_file = open(os.path.join(cur_dir, fragment_path))
        geometry_file = open(os.path.join(cur_dir, geometry_path))
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

        self.u_tex_map = self._load_uniform_location('u_tex_map')

        print("Terrain shader is alive: _/\\_/\\_")


class WaterShader(Common3DLightShaderProgram):
    def __init__(self):
        super().__init__()

        cur_dir = os.getcwd()
        terrain_path = "../res/shader/water.vert"
        fragment_path = "../res/shader/water.frag"
        geometry_path = "../res/shader/water.geom"
        vertex_file = open(os.path.join(cur_dir, terrain_path))
        fragment_file = open(os.path.join(cur_dir, fragment_path))
        geometry_file = open(os.path.join(cur_dir, geometry_path))
        shaders = {
            "water.vert": [gl.GL_VERTEX_SHADER, vertex_file.read()], 
            "water.geom": [gl.GL_GEOMETRY_SHADER, geometry_file.read()],
            "water.frag": [gl.GL_FRAGMENT_SHADER, fragment_file.read()]
        }
        vertex_file.close()
        geometry_file.close()
        fragment_file.close()

        self._compile_shaders(shaders)

        self._map_uniforms()

        self.u_tex_map = self._load_uniform_location('u_tex_map')
        
        self.world_delta = 0.0
        self.u_world_delta = self._load_uniform_location('u_world_delta')

        print("Water shader is alive: ~~~~~")
    
    def add_delta(self, delta):
        self.world_delta += delta
        gl.glUniform1f(self.u_world_delta, self.world_delta)


class ParticleShader(Common3DShaderProgram):
    def __init__(self):
        super().__init__()

        cur_dir = os.getcwd()
        vertex_path = "../res/shader/particle.vert"
        geometry_path = "../res/shader/particle.geom"
        fragment_path = "../res/shader/particle.frag"
        vertex_file = open(os.path.join(cur_dir, vertex_path))
        geometry_file = open(os.path.join(cur_dir, geometry_path))
        fragment_file = open(os.path.join(cur_dir, fragment_path))
        shaders = {
            "particle.vert": [gl.GL_VERTEX_SHADER, vertex_file.read()],
            "particle.geom": [gl.GL_GEOMETRY_SHADER, geometry_file.read()],
            "particle.frag": [gl.GL_FRAGMENT_SHADER, fragment_file.read()]
        }
        vertex_file.close()
        geometry_file.close();
        fragment_file.close()

        self._compile_shaders(shaders)

        self._map_uniforms()

        self.u_world_time = self._load_uniform_location("u_world_time")

        self.u_emit_times = self._load_uniform_location("u_emit_times")
        self.u_emit_positions = self._load_uniform_location("u_emit_positions")
        self.u_sprite_incices = self._load_uniform_location("u_sprite_incices")

        self.u_camera_position = self._load_uniform_location("u_camera_position")
        self.u_camera_up = self._load_uniform_location("u_camera_up")

        print("Particle shader is alive: * x . *")

    def load_camera_position(self, position):
        gl.glUniform3fv(self.u_camera_position, 1, glm.value_ptr(position))

    def load_camera_up(self, up):
        gl.glUniform3fv(self.u_camera_up, 1, glm.value_ptr(up))
    
    def load_world_time(self, time):
        gl.glUniform1f(self.u_world_time, time)

    def load_emitter(self, emitter: ParticleEmitter):
        for index in range(emitter.particle_count):
            gl.glUniform1f(
                self.u_emit_times + index,
                emitter.data_emit_time[index])
            gl.glUniform3fv(
                self.u_emit_positions + index,
                1,
                glm.value_ptr(emitter.data_emit_position[index]))
            gl.glUniform1ui(
                self.u_sprite_incices + index,
                1,
                emitter.data_sprite_incices[index])