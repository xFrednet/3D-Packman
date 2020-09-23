import glm

class Rectangle:
    """This class represents a rectangle in the game. The position represents
    the center of the object"""

    #             width
    #        +------------+
    #        |            |
    #  position -> x      | height
    #        |            |
    #        +------------+

    def __init__(self, position: glm.vec2, width, height):
        """
        This initializes the rectangle.w
        Parameters
        ----------
        position : glm.vec2
            The position of center
        width : 
            The width of the rectangle
        height : 
            The height of the rectangle
        """

        assert(width > 0)
        assert(height > 0)
        
        self.position = position
        self.width = float(width)
        self.height = float(height)

    def get_vertices(self) -> []:
        """This method restuns an Array of vertices to draw this rectangle"""

        # 1---2      4
        # | /      / |
        # 0      3---5
        # IDK why this works with clockwise vertices but I suggest leaving it untouched

        return [
            glm.vec2(self.get_min_x(), self.get_min_y()),
            glm.vec2(self.get_min_x(), self.get_max_y()),
            glm.vec2(self.get_max_x(), self.get_max_y()),

            glm.vec2(self.get_min_x(), self.get_min_y()),
            glm.vec2(self.get_max_x(), self.get_max_y()),
            glm.vec2(self.get_max_x(), self.get_min_y()),
        ]

    def clone(self):
        #[derive(copy, clone)] wait this isn't Rust -.-
        # I can still leave this in as a comment ^^
        return Rectangle(self.position * 1, self.width, self.height)

    def is_overlapping(self, other) -> bool:
        if (self.get_max_x() < other.get_min_x() or
                self.get_min_x() >= other.get_max_x()):
            return False
        if (self.get_max_y() < other.get_min_y() or
                self.get_min_y() >= other.get_max_y()):
            return False
        
        return True

    def get_min_x(self):
        return self.position.x - self.width / 2

    def get_min_y(self):
        return self.position.y - self.height / 2

    def get_max_x(self):
        return self.position.x + self.width / 2
    
    def get_max_y(self):
        return self.position.y + self.height / 2

    def get_center(self):
        return self.position

def create_cross(position, size = 100, thickness = 10):
    return [
        Rectangle(position * 1, size, thickness),
        Rectangle(position * 1, thickness, size)
    ]

def create_h(position, size=100, thickness=10):
    side_offset = size / 2.0 - thickness / 2.0
    return [
        Rectangle(position * 1, size, thickness),
        Rectangle(glm.vec2(position.x + side_offset, position.y), thickness, size),
        Rectangle(glm.vec2(position.x - side_offset, position.y), thickness, size)
    ]

def create_spiral(position, wall_count = 5, path_tickness = 50.0, wall_thickness = 10.0):
    recs = []

    wall_offset = path_tickness / 2.0
    slide_offset = path_tickness / 2.0
    wall_length = path_tickness + wall_thickness
    
    for wall_id in range(wall_count):
        if wall_id % 4 == 0:
            if (wall_id != 0):
                wall_length += path_tickness
            recs.append(
                Rectangle(
                    glm.vec2(position.x - wall_offset, position.y),
                    wall_thickness,
                    wall_length))
        elif wall_id % 4 == 1:
            recs.append(
                Rectangle(
                    glm.vec2(position.x              , position.y - wall_offset),
                    wall_length,
                    wall_thickness))
        elif wall_id % 4 == 2:
            wall_length += path_tickness
            recs.append(
                Rectangle(
                    glm.vec2(position.x + wall_offset, position.y + slide_offset),
                    wall_thickness,
                    wall_length))
        elif wall_id % 4 == 3:
            wall_offset += path_tickness
            recs.append(
                Rectangle(
                    glm.vec2(position.x - slide_offset, position.y + wall_offset),
                    wall_length,
                    wall_thickness))
    
    return recs

def create_case(rectangles):
    """
    Creates a rectangle that incases all rectangles
    """

    if len(rectangles) == 0:
        return Rectangle(glm.vec2(-1, -1), 1, 1)
    
    min_x = rectangles[0].get_min_x()
    max_x = rectangles[0].get_max_x()
    min_y = rectangles[0].get_min_y()
    max_y = rectangles[0].get_max_y()

    for rect in rectangles:
        min_x = min(rect.get_min_x(), min_x)
        max_x = max(rect.get_max_x(), max_x)
        min_y = min(rect.get_min_y(), min_y)
        max_y = max(rect.get_max_y(), max_y)

    width = max_x - min_x
    height = max_y - min_y
    return Rectangle(glm.vec2(min_x + width / 2, min_y + height / 2), width, height)
