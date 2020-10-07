import glm


class Rectangle2D:
    def __init__(self, width, height):
        self.width = width
        self.height = height


class Position2D:
    def __init__(self, position=glm.vec2(0, 0)):
        self.position = position
