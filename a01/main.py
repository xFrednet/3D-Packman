import pygame
from pygame.locals import *

from OpenGL import GL as gl
import OpenGL.GLU as glu

import random

import glm

import entities
from entities import BouncingBall
from entities import ControlledBall

BOUNCING_BALL_COUNT = 100
CONTROLLED_BALL_COUNT = 100

FPS = 60
RESOLUTION = glm.vec2(800, 600)

entities = []

def init_game():
    pygame.display.init()
    pygame.display.set_mode((int(RESOLUTION.x), int(RESOLUTION.y)), DOUBLEBUF|OPENGL)
    gl.glClearColor(0.1, 0.1, 0.1, 1.0)

    for _ in range(0, BOUNCING_BALL_COUNT):
        entities.append(
            BouncingBall(
                RESOLUTION,
                position=glm.vec2(random.uniform(10.0, RESOLUTION.x - 10.0), random.uniform(10.0, RESOLUTION.y - 10.0)),
                velocity=glm.vec2(random.uniform(-100.0, 100.0), random.uniform(-100.0, 100.0)),
                color=glm.vec3(1.0, 0.0, 0.0)))

    for _ in range(0, CONTROLLED_BALL_COUNT):
        entities.append(
            ControlledBall(
                RESOLUTION,
                position=glm.vec2(random.uniform(10.0, RESOLUTION.x - 10.0), random.uniform(10.0, RESOLUTION.y - 10.0)),
                speed=100,
                color=glm.vec3(0.0, 1.0, 0.0)))

def update(delta):
    for e in entities:
        e.update(delta)

def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    
    gl.glViewport(0, 0, int(RESOLUTION.x), int(RESOLUTION.y))
    glu.gluOrtho2D(0, int(RESOLUTION.x), 0, int(RESOLUTION.y))

    for e in entities:
        e.draw()
        
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
            elif event.type == pygame.locals.MOUSEBUTTONDOWN:
                entities.append(
                    BouncingBall(
                        RESOLUTION,
                        position=glm.vec2(float(event.pos[0]), RESOLUTION.y - float(event.pos[1])),
                        velocity=glm.vec2(),
                        color=glm.vec3(0.0, 0.0, 1.0)))

        # Update
        update(delta)
        display()

        clock.tick(FPS)

if __name__ == "__main__":
    init_game()
    game_loop()