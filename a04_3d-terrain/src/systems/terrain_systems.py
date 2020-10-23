import esper

from OpenGL import GL as gl

from components import Transformation, TransformationMatrix, ObjectMaterial
from graphics.vba import TerrainVba
from graphics.shader_program import TerrainShader

class TerrainRenderer(esper.Processor):
    def process(self, *args, **kwargs):

        gl.glEnable(gl.GL_CULL_FACE)
        shader: TerrainShader = self.world.terrainShader
        shader.start()
        shader.load_view_matrix(self.world.view_matrix)
        shader.load_projection_matrix(self.world.projection_matrix)
        shader.load_light_setup(self.world.light_setup)

        for _id, (vba, transformation, material) in self.world.get_components(TerrainVba, TransformationMatrix, ObjectMaterial):
            # Bind buffers
            gl.glBindVertexArray(vba.vba_id)
            vba.index_buffer.bind()
            gl.glEnableVertexAttribArray(TerrainVba.POSITION_ATTR)
            gl.glEnableVertexAttribArray(TerrainVba.NORMAL_ATTR)

            # Draw the beautiful
            shader.load_transformation_matrix(transformation.value)
            shader.load_object_material(material)
            gl.glDrawElements(gl.GL_TRIANGLES, vba.vertex_count, gl.GL_UNSIGNED_INT, None)

            # Unbind the thingies
            gl.glDisableVertexAttribArray(TerrainVba.POSITION_ATTR)
            gl.glDisableVertexAttribArray(TerrainVba.NORMAL_ATTR)
            gl.glBindVertexArray(0)
        
        shader.stop()