import glm
import pygame
import OpenGL.GL as gl

class Entity:
    def __init__(
            self, 
            position = glm.vec2(0, 0),
            color = glm.vec3(0.0, 0.0, 0.0),
            size = 10
        ):
        self.position = position
        self.color = color
        self.size = size
    
    def update(self, _delta):
        pass
    
    def draw(self):
        step = self.size / 2

        # 0      3---5
        # | \      \ |
        # 1---2      4

        gl.glColor3f(self.color.x, self.color.y, self.color.z)

        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex2f(self.position.x - step, self.position.y - step)
        gl.glVertex2f(self.position.x - step, self.position.y + step)
        gl.glVertex2f(self.position.x + step, self.position.y + step)

        gl.glVertex2f(self.position.x - step, self.position.y - step)
        gl.glVertex2f(self.position.x + step, self.position.y + step)
        gl.glVertex2f(self.position.x + step, self.position.y - step)
        gl.glEnd()

class BouncingBall(Entity):
    # Also known as ScreenSaverBall
    
    def __init__(
        self, 
        area,
        position = glm.vec2(0, 0), 
        velocity = glm.vec2(0, 0),
        color = glm.vec3(0.0, 0.0, 0.0),
        size = 10):
        Entity.__init__(
            self, 
            position=position,
            color=color,
            size=size)
            
        self.velocity = velocity
        self.area = area

    def update(self, delta):
        self.position = self.position + self.velocity * delta

        halve_size = self.size / 2
        if ((self.position.x - halve_size) < 0 or self.position.x + halve_size >= self.area.x):
            self.velocity.x *= -1
        if ((self.position.y - halve_size) < 0 or self.position.y + halve_size>= self.area.y):
            self.velocity.y *= -1

class ControlledBall(Entity):
    def __init__(
        self, 
        area,
        position = glm.vec2(0.0, 0.0), 
        speed = 100.0,
        color = glm.vec3(0.0, 0.0, 0.0),
        size = 10):
        Entity.__init__(
            self, 
            position=position,
            color=color,
            size=size)
            
        self.speed = speed
        self.area = area

    def update(self, delta):
        keys = pygame.key.get_pressed()

        movement = glm.vec2()
        if keys[pygame.locals.K_LEFT]:
            movement.x = -1.0
        if keys[pygame.locals.K_RIGHT]:
            movement.x = +1.0
        if keys[pygame.locals.K_UP]:
            movement.y = +1.0
        if keys[pygame.locals.K_DOWN]:
            movement.y = -1.0
        
        glm.normalize(movement)

        size_padding = glm.vec2(self.size / 2, self.size / 2)

        self.position = self.position + (movement * self.speed * delta)
        self.position = glm.clamp(self.position, size_padding, self.area- size_padding)