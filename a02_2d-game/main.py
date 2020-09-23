import pygame
from pygame.locals import *

from OpenGL import GL as gl
import OpenGL.GLU as glu

import glm

from entities import GolfBall
from entities import GolfHole
from entities import ScreenBoundaries

from world import World

import shape

FPS = 60
RESOLUTION = glm.vec2(1200, 700)

world = None

def init_game():
    global world
    
    pygame.display.init()
    pygame.display.set_mode((int(RESOLUTION.x), int(RESOLUTION.y)), DOUBLEBUF|OPENGL)
    gl.glClearColor(0.1, 0.1, 0.1, 1.0)

    # mandatory objects
    ball = GolfBall(position=glm.vec2(100, 600))
    hole = GolfHole(ball, world)
    boundaries = ScreenBoundaries(RESOLUTION.x, RESOLUTION.y)    
    world = World(ball, hole, boundaries)

def update(delta):
    world.update(delta)

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    
    gl.glViewport(0, 0, int(RESOLUTION.x), int(RESOLUTION.y))
    glu.gluOrtho2D(0, int(RESOLUTION.x), int(RESOLUTION.y), 0)

    world.draw()
        
    pygame.display.flip()

def game_loop():
    
    clock = pygame.time.Clock()
    last_millis = pygame.time.get_ticks()

    while True:
        # Delta timing. See https://en.wikipedia.org/wiki/Delta_timing
        # Trust me, this gets important in larger games
        # Pygame implementation stolen from: https://stackoverflow.com/questions/24039804/pygame-current-time-millis-and-delta-time
        millis = pygame.time.get_ticks()
        delta = (millis - last_millis) / 1000.0
        last_millis = millis
        
        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    quit(0)

        # Update
        update(delta)
        display()

        clock.tick(FPS)

if __name__ == "__main__":
    init_game()
    game_loop()