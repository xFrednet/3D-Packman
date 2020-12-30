import ctypes

from OpenGL import GL as gl
from shader_program import StandardShaderProgram


class VertexBufferArray:
    def __init__(self, vertex_count):
        self.vertex_array_id = gl.glGenVertexArrays(1)
        self.vertex_count = vertex_count
        self.__vertex_buffer = []
        self.__obj_vertex_buffer = []

    def cleanup(self):
        for vb in self.__vertex_buffer:
            gl.glDeleteBuffers(1, [vb])

        gl.glDeleteVertexArrays(1, [self.vertex_array_id])

    def _load_vertex_buffer(self, attr_id, data, items_per_vertex, gl_array_type, gl_type, type_size):
        gl.glBindVertexArray(self.vertex_array_id)

        vertex_buffer = gl.glGenBuffers(1)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vertex_buffer)
        self.__vertex_buffer.append(vertex_buffer)

        array_type = (gl_array_type * len(data))
        gl.glBufferData(
            gl.GL_ARRAY_BUFFER,
            len(data) * type_size,
            array_type(*data),
            gl.GL_STATIC_DRAW)
        gl.glVertexAttribPointer(
            attr_id,  # attribute 0.
            items_per_vertex,  # components per vertex attribute
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


class StandardShaderVertexArray(VertexBufferArray):
    def __init__(self, vertex_count):
        VertexBufferArray.__init__(self, vertex_count)

    def load_position_data(self, data):
        self._load_vertex_buffer_f(StandardShaderProgram.POSITION_ATTR, data, 3)

    def load_normal_data(self, data):
        self._load_vertex_buffer_f(StandardShaderProgram.NORMAL_ATTR, data, 3)

    @staticmethod
    def create_cube():
        # vertices:
        # | Top:    | Bottom: |
        # | ------- | ------- |
        # | ´4   5` | `0   1` |
        # | ´6   7` | `2   3` |
        points = [
            [-0.5, 0.5, -0.5],
            [0.5, 0.5, -0.5],
            [-0.5, -0.5, -0.5],
            [0.5, -0.5, -0.5],

            [-0.5, 0.5, 0.5],
            [0.5, 0.5, 0.5],
            [-0.5, -0.5, 0.5],
            [0.5, -0.5, 0.5]
        ]
        side_normals = [
            [0.0, 0.0, -1.0],  # Bottom
            [0.0, 0.0, 1.0],  # Top
            [0.0, -1.0, 0.0],  # Front
            [0.0, 1.0, 0.0],  # Back
            [-1.0, 0.0, 0.0],  # Left
            [1.0, 0.0, 0.0]  # Right
        ]

        # Mapping indices
        sides = [
            [2, 0, 1, 2, 1, 3],  # Bottom
            [4, 6, 5, 5, 6, 7],  # Top
            [2, 3, 7, 6, 2, 7],  # Front
            [4, 5, 0, 0, 5, 1],  # Back
            [6, 4, 0, 0, 2, 6],  # Left
            [5, 7, 3, 5, 3, 1]   # Right
        ]

        # Mapping
        vertices = []
        normals = []
        for side_no in range(6):
            for point_no in range(6):
                point = points[sides[side_no][point_no]]
                vertices.append(point[0])
                vertices.append(point[1])
                vertices.append(point[2])

                n = side_normals[side_no]
                normals.append(n[0])
                normals.append(n[1])
                normals.append(n[2])

                # Creation
        vba = StandardShaderVertexArray(6 * 6)
        vba.load_position_data(vertices)
        vba.load_normal_data(normals)
        return vba
