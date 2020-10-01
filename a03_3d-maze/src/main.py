import pygame
import esper
import glm
from OpenGL import GL as gl
import random
import math

from shader_program import StandardShaderProgram 
from vertex_buffer_array import StandardShaderVertexArray
import render_systems as rsys
import physic_systems as psys
import components as com

RESOLUTION = 720, 480
FPS = 60

class World(esper.World):
    def __init__(self, resolution):
        super().__init__()

        self.standard_shader = StandardShaderProgram()
        self.delta = 0.0
        self.resolution = resolution
        self.camera_id = 0

        #
        # Physics
        #
        self.add_processor(psys.CameraControlSystem(), priority=2100)
        self.add_processor(psys.MovementSystem(), priority=2000)
        
        #
        # Rendering
        #
        # Prepare
        self.add_processor(rsys.BuildViewMatrixSystem(), priority=1010)
        self.add_processor(rsys.BuildTranformationMatrixSystem(), priority=1009)
        self.add_processor(rsys.PrepareFrameSystem(), priority=1008)

        # Draw
        self.add_processor(rsys.StandardRenderSystem(), priority=1008)
        
        #finish
        self.add_processor(rsys.FinishFrameSystem(), priority=1007)

        self._populate()

        self.update_resolution(resolution)

    def cleanup(self):
        """
        cleanup... cleanup so what's the story behind this cleanup method why wouldn't I just use `__del__`?
        Well let me tell you the stupidest thing I've found in Python so far... Do you think that
        `del object` calls `object.__del__`? Well you would be kind of right because it does... but not right away.
        YES yes trust me. It queues the `__del__` call. This is usually fine but not here do you want to guess why?
        Well the `__del__` of the VBOs get called after the destruction of PyOpenGL. Now HOW, tell me HOW should I
        destruct a VBO if the OpenGL bindings are unavailable????

        Now calm down and be happy that you've solved this bug after 4 total hours of debugging...... 
        ~ xFrednet 
        """
        for _entity, vbo in self.get_component(StandardShaderVertexArray):
            vbo.cleanup()

        self.standard_shader.cleanup()

        print("World: Cleanup complete")
    
    def _populate(self):
        # Crappy mixed entity, OOP is a thing... well actually an object...
        # WTF. I'm always amazed by the comments I leave in my code. ~xFrednet 2020.09.23
        vba2 = StandardShaderVertexArray(6)
        vba2.load_position_data([
            -0.1,  0.1, 0.0,
            -0.1, -0.1, 0.0,
             0.1, -0.1, 0.0,
            -0.1,  0.1, 0.0,
             0.1, -0.1, 0.0,
             0.1,  0.1, 0.0])
        vba2.load_color_data([
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            1.0, 0.0, 0.0,
            0.0, 0.0, 1.0,
            0.0, 1.0, 0.0])

        floor = self.create_entity()
        self.add_component(floor, vba2)
        self.add_component(floor, com.Position(0, -2, 0))
        self.add_component(floor, com.Scale(100))
        self.add_component(floor, com.Rotation(math.pi / 2))
        self.add_component(floor, com.TransformationMatrix())

        for i in range(0, 10):
            entity = self.create_entity()
            self.add_component(entity, vba2)
            self.add_component(entity, com.Velocity(x=0.0, y=0.0))
            self.add_component(entity, com.Position(x=random.uniform(-1.0, 1.0), y=random.uniform(-1.0, 1.0), z=random.uniform(-1.0, 1.0)))
            self.add_component(entity, com.Scale())
            self.add_component(entity, com.Rotation(x=random.uniform(-1.0, 1.0), y=random.uniform(-1.0, 1.0), z=random.uniform(-1.0, 1.0)))
            self.add_component(entity, com.TransformationMatrix())
        
        
        camera = self.create_entity()
        self.add_component(camera, com.Position(x=0.0, y=0.0, z=5.0))
        self.add_component(camera, com.Velocity(0.0, 0.0))
        self.add_component(camera, com.CameraOrientation())
        self.add_component(camera, com.ViewMatrix())
        self.camera_id = camera
        

    def update_resolution(self, resolution):
        self.resolution = resolution

        self.standard_shader.update_projection_matrix(resolution)

def game_loop(world):
    clock = pygame.time.Clock()
    last_millis = pygame.time.get_ticks()

    while True:
        # Delta timing. See https://en.wikipedia.org/wiki/Delta_timing
        # Trust me, this gets important in larger games
        # Pygame implementation stolen from: https://stackoverflow.com/questions/24039804/pygame-current-time-millis-and-delta-time
        millis = pygame.time.get_ticks()
        world.delta = (millis - last_millis) / 1000.0
        last_millis = millis
        
        # Get events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.locals.K_ESCAPE:
                    return

        # Update
        world.process()

        clock.tick(FPS)

def main():
    pygame.init()
    pygame.display.init()
    pygame.display.set_mode(RESOLUTION, pygame.DOUBLEBUF|pygame.OPENGL)
    pygame.display.set_caption("Le 3D maze of time")

    world = World(glm.vec2(RESOLUTION))
    
    game_loop(world)

    world.cleanup()

if __name__ == '__main__':
    main()
    pygame.quit()
