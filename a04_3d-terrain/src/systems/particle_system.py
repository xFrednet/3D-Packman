import esper
import glm
import sys

from OpenGL import GL as gl

from graphics import PixelVBA, ParticleShader
from components import CameraOrientation, ParticleEmitter, Transformation


class ParticleEmitterSystem(esper.Processor):
    def process(self):
        for _id, (transformation, emitter) in self.world.get_components(Transformation, ParticleEmitter):
            # Kill old ones
            while (emitter.particle_count > 0):
                alive_time = self.world.time - emitter.data_emit_time[0]
                if (alive_time < emitter.life_time):
                    # All particles are to young to die
                    # And yes this comment says a lot about what is going to happen to the rest... }:D
                    break

                emitter.data_emit_time.pop(0)
                emitter.data_sprite_incices.pop(0)
                emitter.data_emit_position.pop(0)
                
                emitter.particle_count -= 1

            # Spawn new ones
            if (emitter.emitting):
                emitter.emit_timer -= self.world.delta
                if (emitter.emit_timer < 0):
                    if (emitter.particle_count < emitter.max_particles):
                        # Emit new
                        emitter.data_emit_time.append(self.world.time)
                        emitter.data_emit_position.append(transformation.position * 1.0)
                        emitter.data_sprite_incices.append(0)

                        emitter.emit_timer = emitter.emit_interval
                        emitter.particle_count += 1


class ParticleRenderSystem(esper.Processor):
    DEFAULT_MAX_VERTEX_COUNT = 256
    PARTICLE_STAGES = 10
    MAX_BYTES_PER_PARTICLE = 12

    def __init__(self):
        super().__init__()
        self._pixel_vbo = PixelVBA(ParticleRenderSystem.DEFAULT_MAX_VERTEX_COUNT)
        
        data = []
        for i in range(ParticleRenderSystem.DEFAULT_MAX_VERTEX_COUNT):
            data.append(float(i))

        self._pixel_vbo.load_indices(data)

        min_requirement = (
                ParticleRenderSystem.PARTICLE_STAGES *
                ParticleRenderSystem.MAX_BYTES_PER_PARTICLE *
                ParticleRenderSystem.DEFAULT_MAX_VERTEX_COUNT)
        if (gl.glGetIntegerv(gl.GL_MAX_UNIFORM_BLOCK_SIZE) < min_requirement):
            # This was a joke at first but this actually filles out halve of my available block size
            print("ParticleRenderSystem: Error the system as a minimum uniform block size of: ", min_requirement)
            sys.exit(-15)
        
        print("ParticleRenderSystem was created: Am I a particle yet?")
    
    def process(self):
        shader: ParticleShader = self.world.particle_shader
        shader.start()
        shader.load_view_matrix(self.world.view_matrix)
        shader.load_projection_matrix(self.world.projection_matrix)
        shader.load_camera_position(self.world.light_setup.camera_position)
        shader.load_camera_up(self.world.component_for_entity(self.world.camera_id, CameraOrientation).up)

        # VBO
        gl.glBindVertexArray(self._pixel_vbo.vba_id)
        gl.glEnableVertexAttribArray(PixelVBA.INDEX_ARRAY_ATTR)

        for _id, emitter in self.world.get_component(ParticleEmitter):
            shader.load_emitter(emitter)
            gl.glDrawArrays(gl.GL_POINTS, 0, emitter.particle_count)

        # Unbind the thingies
        gl.glDisableVertexAttribArray(PixelVBA.INDEX_ARRAY_ATTR)
        gl.glBindVertexArray(0)
        shader.stop()