import glm
import random

import shape
import entities as e
from entities import GolfBall
from entities import GolfHole

class World:
    """
    This class holds the data of the current world (like entities). It is
    used as a connector between objects
    """

    def __init__(self, ball, hole, boundaries):
        self.score = 0
        self.ball = ball
        self.hole = hole
        self.boundaries = boundaries
        self.entities = []
        self.load_next_level = True
        self.skip_next = True
    
    def update(self, delta):
        if (self.skip_next):
            self.skip_next = False
            # Skips to make delta come back to life
            return

        for e in self.entities:
            e.update(delta, self)

        if (self.load_next_level):
            self.load_next_level = False
            self.load_level()
            self.skip_next = True
        

    def draw(self):
        for e in self.entities:
            e.draw()

    def add(self, entity):
        self.entities.append(entity)

    def is_colliding(self, src_entity, motion_vector, return_colliding = False, hero_bounding_boxes_override = None) -> (bool, []):
        """
        This tests if the src_entity collides with any other entity in the world.
        (is_colliding_horizontal, is_colliding_vertical)

        src_entity is the entity calling this.
        """

        # Test if any of the bounding_boxes from src_entity.get_bounding_boxes() collides

        # Checking if src_entity rectangle is within other one's rectangles

        # a1 is the hero entity, b1 is the villain entity ~stefan
        # src_entity aka. a1 ~ xFrednet

        villains = []
        side = 'None'
        collsion = False

        hero_bounding_boxes = src_entity.get_bounding_boxes()
        collsion_area = src_entity.get_collsion_area()
        if (hero_bounding_boxes_override != None):
            hero_bounding_boxes = hero_bounding_boxes_override
            collsion_area = shape.create_case(hero_bounding_boxes)
        
        collsion_area = collsion_area.clone()
        collsion_area.position += motion_vector

        entity_queue = [e for e in self.entities if (collsion_area.is_overlapping(e.get_collsion_area()) and e != src_entity)]

        for box in hero_bounding_boxes:
            hero_bounding_box_prev = box
            hero_bounding_box = hero_bounding_box_prev.clone()
            hero_bounding_box.position += motion_vector
            
            for entity in entity_queue:

                if (entity == src_entity):
                    continue

                for villain_bounding_box in entity.get_bounding_boxes():
                    if (not hero_bounding_box.is_overlapping(villain_bounding_box)):
                        continue
                    
                    # At this point we can be sure that the hero and villan collide because:
                    #    1. hero.x is > than villan.x and less than villan.max_x
                    #    2. hero.y is > than villan.y and less than villan.max_y
                    # -> Now we have to find out where they are colliding

                    collsion =  True
                    diff_x = 0.0
                    diff_y = 0.0
                    if ((hero_bounding_box_prev.get_max_x() <= villain_bounding_box.get_min_x() and
                        hero_bounding_box.get_max_x() > villain_bounding_box.get_min_x())):
                        # hero has entered the villan from the left
                        side = 'right_side'
                        diff_x = hero_bounding_box.get_max_x() - villain_bounding_box.get_min_x()

                    elif ((hero_bounding_box_prev.get_min_x() >= villain_bounding_box.get_max_x() and
                        hero_bounding_box.get_min_x() < villain_bounding_box.get_max_x())):
                        # The hero attacks the villan from the right
                        side = 'left_side'
                        diff_x = hero_bounding_box.get_min_x() - villain_bounding_box.get_max_x()

                    elif ((hero_bounding_box_prev.get_min_y() >= villain_bounding_box.get_max_y() and
                        hero_bounding_box.get_min_y() < villain_bounding_box.get_max_y())):
                        # hero is above the villan if you know what i mean
                        side = 'bottom_side'
                        diff_y = hero_bounding_box.get_min_y() - villain_bounding_box.get_max_y()

                    elif ((hero_bounding_box_prev.get_max_y() <= villain_bounding_box.get_min_y() and
                        hero_bounding_box.get_max_y() > villain_bounding_box.get_min_y())):
                        # The hero is below the villan
                        # I won't make the same bad joke as before 
                        side = 'top_side'
                        diff_y = hero_bounding_box.get_max_y() - villain_bounding_box.get_min_y()

                    else:
                        # We should never reach this point unless we are allready in the villan. How does
                        # this happen... "Speed that's what it is!" I should stop listening to music while programming 
                        side = 'unknown'

                    villains.append((side, glm.vec2(diff_x, diff_y), entity))
                    
                    if (not return_colliding):
                        return collsion, villains

        return collsion, villains
    
    def add_score(self):
        self.score += 1
        self.load_next_level = True

        if (self.score >= 5):
            self.score = 0
    
    def load_level(self):
        hole_pos, entities = get_level_objects(self.score)
        self.hole.set_position(hole_pos)
        
        entities.append(self.ball)
        entities.append(self.hole)
        entities.append(self.boundaries)
        self.entities = entities

        self.load_next_score = False
    
    def get_new_hole_position(self):
        return glm.vec2(random.uniform(50, 1200 - 50), random.uniform(50, 700 - 50))

# 1200, 700
def get_level_objects(level: int): 
    if (level == 0):
        return (
            glm.vec2(100, 100), 
            [
                e.StaticObstacle(glm.vec2(550, 350), [shape.Rectangle(glm.vec2(550, 350), 1100, 10)])
            ]
        )
    elif (level == 1):
        return (
            glm.vec2(1100, 100),
            [
                e.MovingSinObstacle(glm.vec2(600,  25), [shape.Rectangle(glm.vec2(600,  25), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 1),
                e.MovingSinObstacle(glm.vec2(600,  75), [shape.Rectangle(glm.vec2(600,  75), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 2),
                e.MovingSinObstacle(glm.vec2(600, 125), [shape.Rectangle(glm.vec2(600, 125), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 3),
                e.MovingSinObstacle(glm.vec2(600, 175), [shape.Rectangle(glm.vec2(600, 175), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 4),
                e.MovingSinObstacle(glm.vec2(600, 225), [shape.Rectangle(glm.vec2(600, 225), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 5),
                e.MovingSinObstacle(glm.vec2(600, 275), [shape.Rectangle(glm.vec2(600, 275), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 6),
                e.MovingSinObstacle(glm.vec2(600, 325), [shape.Rectangle(glm.vec2(600, 325), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 7),
                e.MovingSinObstacle(glm.vec2(600, 375), [shape.Rectangle(glm.vec2(600, 375), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 8),
                e.MovingSinObstacle(glm.vec2(600, 425), [shape.Rectangle(glm.vec2(600, 425), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 9),
                e.MovingSinObstacle(glm.vec2(600, 475), [shape.Rectangle(glm.vec2(600, 475), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 10),
                e.MovingSinObstacle(glm.vec2(600, 525), [shape.Rectangle(glm.vec2(600, 525), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 11),
                e.MovingSinObstacle(glm.vec2(600, 575), [shape.Rectangle(glm.vec2(600, 575), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 12),
                e.MovingSinObstacle(glm.vec2(600, 625), [shape.Rectangle(glm.vec2(600, 625), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 13),
                e.MovingSinObstacle(glm.vec2(600, 675), [shape.Rectangle(glm.vec2(600, 675), 10, 50)], glm.vec2(400, 0), delta_total=(6.28 / 14) * 14),
            ]
        )
    elif (level == 2):
        return (
            glm.vec2(100, 650),
            [
                e.StaticObstacle(glm.vec2(200, 595), [shape.Rectangle(glm.vec2(200, 595), 400, 10)]),
                e.StaticObstacle(glm.vec2(400, 300), [shape.Rectangle(glm.vec2(400, 300), 10, 600)]),
                e.StaticObstacle(glm.vec2(500, 400), [shape.Rectangle(glm.vec2(500, 400), 10, 600)]),
                e.StaticObstacle(glm.vec2(600, 300), [shape.Rectangle(glm.vec2(600, 300), 10, 600)]),

                e.MovingSinObstacle(glm.vec2(650, 350), [
                    shape.Rectangle(glm.vec2(650, 350 + 25), 100 - 12, 10),
                    shape.Rectangle(glm.vec2(650, 350 - 25), 100 - 12, 10)
                ], glm.vec2(0, 300), delta_multiplier=0.5),

                e.StaticObstacle(glm.vec2(700, 400), [shape.Rectangle(glm.vec2(700, 400), 10, 600)]),
                e.StaticObstacle(glm.vec2(800, 300), [shape.Rectangle(glm.vec2(800, 300), 10, 600)]),
                e.StaticObstacle(glm.vec2(900, 400), [shape.Rectangle(glm.vec2(900, 400), 10, 600)])
            ]
        )
    elif (level == 3):
        return (
            glm.vec2(100, 350 / 2),
            [
                e.StaticObstacle(glm.vec2(550, 350), [shape.Rectangle(glm.vec2(550, 350), 1100, 10)]),
                e.MovingSinObstacle(glm.vec2(1150, 350), shape.create_cross(glm.vec2(1150, 350), 100), glm.vec2(0.0, 100.0)),
                # h, h
                e.MovingCircleObstacle(glm.vec2(550, 350 / 2), shape.create_h(glm.vec2(550, 350 / 2), 50), (350 / 2) - 25),
                e.MovingCircleObstacle(glm.vec2(550, 350 / 2), shape.create_h(glm.vec2(550, 350 / 2), 50), (350 / 4) - 25),
                # h h h h h h h h
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 1),
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 2),
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 3),
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 4),
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 5),
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 6),
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 7),
                e.MovingCircleObstacle(glm.vec2(550, 350 + 350 / 2), shape.create_h(glm.vec2(550, 350 + 350 / 2), 50), (350 / 2) - 25, delta_total=(6.28 / 8) * 8),
            ]
        )
    else:
        return (
            glm.vec2(550, 600),
            []
        )