import getopt
import sys

import pygame
import pygame.display
import pygame.locals

from world import World

RESOLUTION = 1024, 720
FPS = 60


def game_loop(world):
    clock = pygame.time.Clock()
    last_millis = pygame.time.get_ticks()
    while True:
        # Delta timing. See https://en.wikipedia.org/wiki/Delta_timing
        # Trust me, this gets important in larger games
        # Pygame implementation stolen from:
        # https://stackoverflow.com/questions/24039804/pygame-current-time-millis-and-delta-time
        millis = pygame.time.get_ticks()
        world.delta = min(max((millis - last_millis) / 1000.0, 0.00000001), 0.1)
        last_millis = millis

        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.locals.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                return

        # Update
        world.process()

        clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("3D Terrain - rendering smooth was yesterday")
    pygame.mouse.set_visible(True)
    world = World(RESOLUTION)

    game_loop(world)
    world.cleanup()


if __name__ == '__main__':
    main()
    pygame.quit()
    print('You quit the game!')
