import esper

from OpenGL import GL as gl

from components import Transformation, TransformationMatrix
from graphics.vba import TerrainVba
from graphics.shader_program import TerrainShader

class Terrain:
    def __init__(self):
        pass
    
    def create_chunks(self, world):
        vba = TerrainVba(3)
        vba.load_position_data([
            -0.5,  0.5, 0.0, 
            -0.5, -0.5, 0.0, 
             0.5,  0.5, 0.0 
        ])
        vba.load_normal_data([
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0
        ])

        world.create_entity(
            vba,
            Transformation(),
            TransformationMatrix())


class TerrainRenderer(esper.Processor):
    def process(self, *args, **kwargs):

        shader: TerrainShader = self.world.terrainShader
        shader.start()
        shader.load_view_matrix(self.world.view_matrix)
        shader.load_projection_matrix(self.world.projection_matrix)

        for _id, (vba, transformation) in self.world.get_components(TerrainVba, TransformationMatrix):
            # Bind buffers
            gl.glBindVertexArray(vba.vba_id)
            gl.glEnableVertexAttribArray(TerrainVba.POSITION_ATTR)
            gl.glEnableVertexAttribArray(TerrainVba.NORMAL_ATTR)

            # Draw the beautiful
            shader.load_transformation_matrix(transformation.value)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, vba.vertex_count)

            # Unbind the thingies
            gl.glDisableVertexAttribArray(TerrainVba.POSITION_ATTR)
            gl.glDisableVertexAttribArray(TerrainVba.NORMAL_ATTR)
            gl.glBindVertexArray(0)
        
        shader.stop()