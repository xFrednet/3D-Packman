import esper

from OpenGL import GL as gl

from components import Transformation, TransformationMatrix, ObjectMaterial
from graphics.vba import TerrainMesh
from graphics.shader_program import TerrainShader

class TerrainRenderer(esper.Processor):
    def process(self, *args, **kwargs):

        gl.glEnable(gl.GL_CULL_FACE)
        shader: TerrainShader = self.world.terrainShader
        shader.start()
        shader.load_view_matrix(self.world.view_matrix)
        shader.load_projection_matrix(self.world.projection_matrix)
        shader.load_light_setup(self.world.light_setup)

        for _id, (mesh, transformation, material) in self.world.get_components(TerrainMesh, TransformationMatrix, ObjectMaterial):
            # Bind buffers
            gl.glBindVertexArray(mesh.vba_id)
            mesh.index_buffer.bind()
            gl.glEnableVertexAttribArray(TerrainMesh.TEX_COORDS_ATTR)

            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, mesh.height_map.texture)
            gl.glUniform1i(shader.u_tex_map, 0)

            # Draw the beautiful
            shader.load_transformation_matrix(transformation.value)
            shader.load_object_material(material)
            gl.glDrawElements(gl.GL_TRIANGLES, mesh.vertex_count, gl.GL_UNSIGNED_INT, None)

            # Unbind the thingies
            gl.glDisableVertexAttribArray(TerrainMesh.TEX_COORDS_ATTR)
            gl.glBindVertexArray(0)
        
        shader.stop()