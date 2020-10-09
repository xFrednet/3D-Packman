class ObjLoader:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.faces = []
        self.get_values(filename, swapyz)

    def get_values(self, filename, swapyz):
        faces = []
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'f':
                for v in values[1:]:
                    w = v.split('/')
                    arr = [int(w[0]), int(w[2])]
                    faces.append(arr)
        self.faces = faces

    def get_obj(self):
        return self.faces, self.vertices, self.normals


if __name__ == '__main__':
    filename = 'male.obj'
    fil = ObjLoader(filename)
    obj = fil.get_obj()

"""
v 1.405868 -0.033901 1.428365
v 2.629364 -0.033901 0.850164
v 3.629364 -1.033901 1.850164

vt 0.330000 0.000000
vt 0.663333 0.000000
vt 0.330000 0.250000

vn -0.132618 0.224532 0.965401
vn -0.132618 0.224532 0.965401
vn -0.152618 0.274532 0.965401

f 1/0/2 1/2/2 2/0/3
f 5/0/4 5/2/7 3/0/4
"""
