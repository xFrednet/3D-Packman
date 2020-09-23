import contextlib, sys, ctypes
from OpenGL import GL as gl
import esper
import glfw
import glm

from vertex_buffer_array import StandardShaderVertexArray
from application import Application
import render_systems as rsys
import physic_systems as psys
import components as com

def main_loop(window, world):
    while (
        glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS and
        not glfw.window_should_close(window)
    ):
        world.process()
        glfw.swap_buffers(app.window)
        glfw.poll_events()

class World(esper.World):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = Application()
    world = World()

    # Systems
    world.add_processor(psys.MovementSystem(), priority=2000)
    world.add_processor(rsys.PrepareFrameSystem(), priority=1010)
    world.add_processor(rsys.TranslationMatricesSystem(), priority=1009)
    world.add_processor(rsys.StandardRenderSystem(), priority=1008)
    world.add_processor(rsys.FinishFrameSystem(), priority=1007)
    
    # Crappy mixed entity, OOP is a thing... well actually an object...
    vba = StandardShaderVertexArray(3)
    vba.load_position_data([-1, -1, 0, 1, -1, 0, 0,  1, 0])
    vba.load_color_data([
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0])

    vba2 = StandardShaderVertexArray(6)
    vba2.load_position_data([
        -0.1,  0.1, 0.1,
        -0.1, -0.1, 0.1,
         0.1, -0.1, 0.1,
        -0.1,  0.1, 0.1,
         0.1, -0.1, 0.1,
         0.1,  0.1, 0.1])
    vba2.load_color_data([
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,
        1.0, 0.0, 0.0,
        0.0, 0.0, 1.0,
        0.0, 1.0, 0.0])

    # entity = world.create_entity()
    # world.add_component(entity, vba)

    entity = world.create_entity()
    world.add_component(entity, vba2)
    world.add_component(entity, com.Position())
    world.add_component(entity, com.Velocity(0.001, 0.001))
    world.add_component(entity, com.Scale())
    world.add_component(entity, com.TransformationMatrix())

    main_loop(app.window, world)

    del vba
    del vba2
    del world
