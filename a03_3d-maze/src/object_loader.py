from vertex_buffer_array import StandardShaderVertexArray


class ObjLoader:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.faces = []
        self.get_values(filename, swapyz)

    def get_values(self, filename, swapyz):
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = [v[0], v[2], v[1]]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = [v[0], v[2], v[1]]
                self.normals.append(v)
            elif values[0] == 'f':
                for v in values[1:]:
                    w = v.split('/')
                    self.faces.append([int(w[0]) - 1, int(w[2]) - 1])

    def get_obj(self):
        normals = []
        vertices = []
        for face in self.faces:
            for j in range(3):
                index = face[0]
                vertices.append(self.vertices[index][j])
            for j in range(3):
                normals.append(self.normals[face[1]][j])

        vba = StandardShaderVertexArray(len(self.faces))
        vba.load_position_data(vertices)
        vba.load_normal_data(normals)
        return vba


if __name__ == '__main__':
    filename = 'myObj.obj'
    fil = ObjLoader(filename)
    obj = fil.get_obj()
