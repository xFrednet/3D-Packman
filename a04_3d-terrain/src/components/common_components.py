import glm

#
# Object Translation
#
class Transformation:
    def __init__(
            self,
            position=glm.vec3(),
            scale=glm.vec3(1.0, 1.0, 1.0),
            rotation=glm.vec3()):
        self.position = position * 1.0
        self.scale = scale * 1.0
        self.rotation = rotation * 1.0


class TransformationMatrix:
    def __init__(self):
        self.value = glm.mat4x4(1.0)