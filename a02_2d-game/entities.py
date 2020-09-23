import glm
import pygame
import OpenGL.GL as gl
import copy
import math

import shape
from shape import Rectangle

class Entity:
    
    def __init__(
            self, 
            position = glm.vec2(0, 0),
            color = glm.vec3(0.0, 0.0, 0.0),
            rectangles = []
        ):
        self.position = position
        self.color = color
        self.rectangles = rectangles
        self.collsion_area = shape.create_case(rectangles)

    
    def update(self, _delta, _world):
        pass
    
    def draw(self):
        gl.glColor3f(self.color.x, self.color.y, self.color.z)

        gl.glBegin(gl.GL_TRIANGLES)
        
        for rect in self.rectangles: 
            for vertex in rect.get_vertices():
                gl.glVertex2f(vertex.x, vertex.y)

        gl.glEnd()

    def set_position(self, position):
        diff = position - self.position

        self.position += diff
        for rect in self.rectangles:
            rect.position += diff
        self.collsion_area.position += diff

    def get_bounding_boxes(self) -> []:
        """This method returns the bounding boxes of the entity"""
        return self.rectangles
    
    def get_collsion_area(self) -> shape.Rectangle:
        return self.collsion_area
    
    @staticmethod
    def bounce(velocity, side):
        if side == 'top_side' or side == 'bottom_side':
            velocity.y *= -1
        elif side == 'left_side' or side == 'right_side':
            velocity.x *= -1
        
        # This is more a guess, but what else am I suppose to do
        if side == 'unknown':
            if (velocity.x > velocity.y):
                velocity.x *= -1
            else:
                velocity.y *= -1

        return velocity

class CollisionTester(Entity):
    
    def __init__(self):
        Entity.__init__(
            self,
            position=glm.vec2(0, 0),
            color=glm.vec3(1.0, 0.0, 1.0),
            rectangles=[Rectangle(glm.vec2(0, 0), 10, 10)])
        
        self.last_pos = glm.vec2()
    
    def update(self, delta, level): # level = world

        (x, y) = pygame.mouse.get_pos()
        _w, h = pygame.display.get_surface().get_size()
        pos = glm.vec2(x, h - y)
        self.set_position(pos)

        colliding = level.is_colliding(self, glm.normalize(pos - self.last_pos) * 10.0)
        if (colliding[0]):
            print(colliding[1])

        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_e]:
            self.last_pos = pos
            
class GolfHole(Entity):
    def __init__(
            self,
            ball_instance,
            world,
            size=50):
        position = glm.vec2(0.0, 0.0)
        Entity.__init__(
                self, 
                position=position * 1,
                color=glm.vec3(0.7, 0.0, 0.0),
                rectangles=[Rectangle(position * 1, size, size)])
        self.ball_instance = ball_instance

    def update(self, delta, world):
        hole: Rectangle = self.rectangles[0]
        ball: Rectangle = self.ball_instance.rectangles[0]
        if (hole.get_min_x() <= ball.get_min_x() and
                hole.get_max_x() >= ball.get_max_x() and
                hole.get_min_y() <= ball.get_min_y() and
                hole.get_max_y() >= ball.get_max_y()):
            world.add_score()
            self.set_position(world.get_new_hole_position())

    def get_bounding_boxes(self) -> []:
        return []

class GolfBall(Entity):
    def __init__(
            self, 
            position = glm.vec2(400, 300), 
            force_per_px = 2.0,
            color = glm.vec3(1.0, 1.0, 1.0),
            world = None):
        size = 10
        Entity.__init__(
            self, 
            position=position,
            color=color,
            rectangles=[Rectangle(position, size, size)])

        self.is_pressed = False
        self.possible_velocity = glm.vec2()
        self.force_per_px = force_per_px
        self.velocity = glm.vec2()
        self.distance = 0
        self.prediction = []

    def update(self, delta, world): # level = world
        if (self.distance >= 4.0):
            self._process_physics(delta, world)
        else:
            self._process_input(delta, world)
    
    def _process_physics(self, delta, world):
        travel = (self.distance * 2.0) * (delta)

        position, velocity = self._simulate_movement(
            world,
            self.get_bounding_boxes(),
            self.velocity,
            travel,
            self.position
        )

        self.distance -= travel
        self.set_position(position)
        self.velocity = velocity
    
    def _simulate_movement(self, world, src_bounding_boxes, velocity, distance, position):
        bounding_boxes = []
        for box in src_bounding_boxes:
            bounding_boxes.append(box.clone())
        
        while (distance > 0.0001):
            travel = 7.5
            if distance < travel:
                travel = distance

            colliding, info_list = world.is_colliding(
                self,
                velocity * travel,
                hero_bounding_boxes_override = bounding_boxes)
            if colliding:
                for side, _diff, _entity in info_list:
                    if side == 'unknown':
                        # This is hacky and I don't want to talk about it
                        # The right solution would be to have it slide out to the side it entered 
                        # the villan bounding box. but computing this would be more work than this
                        # that works.
                        
                        new_pos = (position - velocity * travel * 0.5)
                        diff = new_pos - position
                        for box in bounding_boxes:
                            box.position += diff
                        position += diff
                    else:
                        velocity = Entity.bounce(velocity, side)
            else:
                new_pos = (position + velocity * travel)
                diff = new_pos - position
                for box in bounding_boxes:
                    box.position += diff
                position += diff
        
            distance -= travel
        
        return position, velocity

    def _process_input(self, _delta, world):
        (l, _m, _r) = pygame.mouse.get_pressed()
        (x, y) = pygame.mouse.get_pos()

        if (l):
            self.is_pressed = True

            # Relative mouse position
            self.possible_velocity = (self.position - glm.vec2(x, y)) * self.force_per_px
            self._recalc_prediciton(world)

        elif (self.is_pressed):
            self.is_pressed = False
            self.last_mouse_pos = glm.vec2()
            # world.score_system.decrement_score(1)
            
            self.velocity = glm.normalize(self.possible_velocity)
            self.distance = glm.length(self.possible_velocity) * 1.5

    def _recalc_prediciton(self, world):
        STEPS = 20
        
        self.prediction = []

        rect = self.rectangles[0].clone()
        start_width = rect.width
        start_height = rect.height
        position = self.position * 1
        velocity = glm.normalize(self.possible_velocity)
        length = glm.length(self.possible_velocity)
        
        for i in range(0, STEPS):
            travel = length / STEPS

            position, velocity = self._simulate_movement(
                world,
                [rect],
                velocity,
                travel,
                position
            )

            rect.position = position

            prediction_rect = rect.clone()
            prediction_rect.width = (start_width / float(STEPS)) * (STEPS - float(i))
            prediction_rect.height = (start_height / float(STEPS)) * (STEPS - float(i))
            self.prediction.append(prediction_rect)

    def get_collsion_area(self) -> shape.Rectangle:
        return shape.create_case(self.rectangles)
    
    def draw(self):
        if self.is_pressed:
            self._draw_prediction()

        Entity.draw(self)

    def _draw_prediction(self):
        gl.glColor3f(0.5, 0.5, 0.5)
        gl.glBegin(gl.GL_TRIANGLES)
        
        for rect in self.prediction: 
            for vertex in rect.get_vertices():
                gl.glVertex2f(vertex.x, vertex.y)

        gl.glEnd()

class ScreenBoundaries(Entity):
    def __init__(self, width, height):
        center_x = width / 2.0
        center_y = height / 2.0  
        thicccckness = 100.0 # I'm sorry, I really am!
        halve_thicck = thicccckness / 2.0 - 1 # This -1 makes one pixel of the borders visible
        rects = [
            Rectangle(glm.vec2(center_x            , 0      - halve_thicck), width + thicccckness, thicccckness),
            Rectangle(glm.vec2(center_x            , height + halve_thicck), width + thicccckness, thicccckness),
            Rectangle(glm.vec2(0     - halve_thicck, center_y)             , thicccckness        , height + thicccckness),
            Rectangle(glm.vec2(width + halve_thicck, center_y)             , thicccckness        , height + thicccckness)
        ]
        
        Entity.__init__(
            self, 
            position=glm.vec2(0, 0),
            color=glm.vec3(1.0, 1.0, 1.0),
            rectangles=rects)
        
    def set_position(self, position):
        # The walls have to be static even if this looks super funny xD
        pass

class StaticObstacle(Entity):
    # this is the point where I miss an Entity Component System
    # I deciced to use this architecture because it is a bit more intuitive at the start
    # and therefor better for teamwork. Some overhead is the price for this -.-

    def __init__(self, position, shape):
        Entity.__init__(
           self, 
           position=position,
           color=glm.vec3(1.0, 1.0, 1.0),
           rectangles=shape)

    def set_position(self, position):
        # The walls have to be static even if this looks super funny xD
        pass

class MovingSinObstacle(Entity):
    def __init__(self, position, shapes, velocity, delta_multiplier = 1.0, delta_total = 0.0):
        Entity.__init__(
           self, 
           position=position,
           color=glm.vec3(1.0, 1.0, 1.0),
           rectangles=shapes)
        self.center = position * 1
        self.variation = glm.length(velocity)
        self.direction = glm.normalize(velocity)
        self.dm = delta_multiplier
        self.delta_total = delta_total

    def update(self, delta, world):
        self.delta_total += delta
        target = self.center + (self.direction * (self.variation * (math.sin(self.delta_total * self.dm))))

        difference = target - self.position
        distance = glm.length(difference)
        direction = glm.normalize(difference)
        
        # Move in steps to prevent clipping
        while (distance > 0.0):
            travel = 7.5
            if (distance < travel):
                travel = distance
            
            motion = direction * travel
            _, entities = world.is_colliding(self, motion, True)
            for _side, dis, e in entities:
                e.set_position(e.position + dis * 1.01)
            self.set_position(self.position + motion)

            distance -= travel

class MovingCircleObstacle(Entity):
    def __init__(self, position, shapes, radius, delta_multiplier = 1.0, delta_total = 0.0):
        Entity.__init__(
           self, 
           position=position,
           color=glm.vec3(1.0, 1.0, 1.0),
           rectangles=shapes)
        self.center = position * 1
        self.radius = radius
        self.dm = delta_multiplier
        self.delta_total = delta_total
        self.set_position(self._get_target())

    def update(self, delta, world):
        self.delta_total += delta
        target = self._get_target()

        difference = target - self.position
        distance = glm.length(difference)
        direction = glm.normalize(difference)
        
        # Move in steps to prevent clipping
        while (distance > 0.0):
            travel = 7.5
            if (distance < travel):
                travel = distance
            
            motion = direction * travel
            _, entities = world.is_colliding(self, motion, True)
            for _side, dis, e in entities:
                e.set_position(e.position + dis * 1.01)
            self.set_position(self.position + motion)

            distance -= travel
    
    def _get_target(self):
        direction = glm.vec2(
            math.sin(self.delta_total * self.dm),
            math.cos(self.delta_total * self.dm))

        return self.center + direction * self.radius