import esper

from OpenGL import GL as gl

from graphics.vba import TerrainVba

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
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0
        ])

        world.create_entity(vba)


class TerrainRenderer(esper.Processor):
    def process(self, *args, **kwargs):
        for _id, vba in self.world.get_component(TerrainVba):
            # Bind buffers
            gl.glBindVertexArray(vba.vba_id)
            gl.glEnableVertexAttribArray(TerrainVba.POSITION_ATTR)
            gl.glEnableVertexAttribArray(TerrainVba.NORMAL_ATTR)

            # Draw the beautiful
            # shader.set_transformation_matrix(translation.value)
            # shader.set_object_material(material)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, vba.vertex_count)

            # Unbind the thingies
            gl.glDisableVertexAttribArray(TerrainVba.POSITION_ATTR)
            gl.glDisableVertexAttribArray(TerrainVba.NORMAL_ATTR)
            gl.glBindVertexArray(0)