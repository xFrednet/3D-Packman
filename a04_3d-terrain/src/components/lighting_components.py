import glm

class ObjectMaterial:
    def __init__(self,
                 diffuse=glm.vec3(0, 0, 0),
                 specular=glm.vec3(0, 0, 0),
                 shininess=5):
        self.diffuse = diffuse * 1.0
        self.specular = specular * 1.0
        self.shininess = shininess


class Light:
    def __init__(
            self,
            color=glm.vec3(),
            attenuation=glm.vec3(0.0, 0.0, 1.0),
            enabled=True):
        self.color = color * 1.0
        self.attenuation = attenuation * 1.0
        self.enabled = enabled
        # The attenuation is calculates like: 
        #   d := distance
        #   attenuation.x * d^2 + attenuation.y * d + attenuation.z