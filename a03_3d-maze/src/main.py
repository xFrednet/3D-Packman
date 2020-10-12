import glm
import pygame
from world import World

RESOLUTION = 1024, 720
FPS = 60
LEVEL = 1


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
            elif event.type == pygame.KEYDOWN and event.key == pygame.locals.K_ESCAPE:
                return

        # Update
        world.process()

        clock.tick(FPS)


def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Le 3D maze of time")
    running = True
    world = World(glm.vec2(RESOLUTION), LEVEL)

    game_loop(world)
    world.cleanup()


def choose_level():
    print('Please choose a level')
    global LEVEL
    while True:
        show = False
        val = 0
        try:
            val = int(input('Please enter a value: '))
        except ValueError:
            print('You should choose a number between 1, 2 or 3 inclusive!')
            show = False
        if 3 >= val > 0:
            LEVEL = val
            if val == 3:
                print('Excellent choice!')
                break
            break
        if val < 0 or val > 3:
            show = True
        if show:
            print('You should choose either 1, 2 or 3!')


if __name__ == '__main__':
    choose_level()
    main()
    pygame.quit()
