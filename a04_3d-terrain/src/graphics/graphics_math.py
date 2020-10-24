import glm
import math

def build_transformation_matrix(position, rotation, scale):
    mat = glm.mat4x4(1.0)
    
    mat = glm.translate(mat, position)
    mat = glm.rotate(mat, rotation.z, glm.vec3(1, 0, 0))
    mat = glm.rotate(mat, rotation.y, glm.vec3(0, 1, 0))
    mat = glm.rotate(mat, rotation.x, glm.vec3(0, 0, 1))
    mat = glm.scale(mat, scale)

    return mat

def build_view_matrix(position, look_at, up):
    forward = glm.normalize(position - look_at)
    right = glm.normalize(glm.cross(up, forward))
    up = glm.normalize(glm.cross(forward, right))

    mat = glm.mat4(1.0)
    mat[0][0] = right.x
    mat[1][0] = right.y
    mat[2][0] = right.z
    mat[0][1] = up.x
    mat[1][1] = up.y
    mat[2][1] = up.z
    mat[0][2] = forward.x
    mat[1][2] = forward.y
    mat[2][2] = forward.z

    mat[3][0] = -(glm.dot(right, position))
    mat[3][1] = -(glm.dot(up, position))
    mat[3][2] = -(glm.dot(forward, position))

    return mat

def build_projection_matrix(resolution, fov=(math.pi / 2), n=1.0, f=500.0):
    aspect = resolution.x / resolution.y

    top = n * math.tan(fov / 2)
    bottom = -top
    right = top * aspect
    left = -right

    mat = glm.mat4(0.0)
    mat[0][0] = (2 * n) / (right - left)
    mat[1][1] = (2 * n) / (top - bottom)
    mat[2][0] = (left + right) / (right - left)
    mat[2][1] = (top + bottom) / (top - bottom)
    mat[2][2] = (-(f + n)) / (f - n)
    mat[2][3] = -1
    mat[3][2] = (-(2 * f * n)) / (f - n)

    return mat