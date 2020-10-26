import ctypes
import numpy 

from OpenGL import GL as gl
from OpenGL.arrays import vbo

class VertexBufferArray:
    def __init__(self, vertex_count):
        self.vba_id = gl.glGenVertexArrays(1)
        self.vertex_count = vertex_count
        self._buffer = []

    def cleanup(self):
        for vb in self._buffer:
            gl.glDeleteBuffers(1, [vb])

        gl.glDeleteVertexArrays(1, [self.vertex_array_id])

    def _load_vertex_buffer(self, attr_id, data, items_per_vertex, gl_array_type, gl_type, type_size):
        gl.glBindVertexArray(self.vba_id)

        vertex_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
        self._buffer.append(vertex_buffer)

        array_type = (gl_array_type * len(data))
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            len(data) * type_size,
            array_type(*data),
            gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(
            attr_id,  
            items_per_vertex,
            gl_type,  # type
            False,  # to be normalized?
            0,  # stride
            None  # array buffer offset
        )

        gl.glBindVertexArray(0)

    def _load_vertex_buffer_f(self, attr_id, data, items_per_vertex):
        self._load_vertex_buffer(
            attr_id,
            data,
            items_per_vertex,
            gl.GLfloat,
            gl.GL_FLOAT,
            ctypes.sizeof(ctypes.c_float))


class IndexedVertexArrayBuffer(VertexBufferArray):
    
    def __init__(self, vertex_count):
        super().__init__(vertex_count)
        self.index_buffer = None
    
    def load_index_buffer(self, data):
        indices = numpy.array([data], dtype=numpy.int32)
        self.index_buffer = vbo.VBO(indices, target=gl.GL_ELEMENT_ARRAY_BUFFER)


class TerrainMesh(IndexedVertexArrayBuffer):
    TEX_COORDS_ATTR = 0

    def __init__(self, vertex_count, height_maps):
        super().__init__(vertex_count)
        self.height_maps = height_maps

    def load_tex_coords_data(self, data):
        self._load_vertex_buffer_f(TerrainMesh.TEX_COORDS_ATTR, data, 2)