import sys
import glfw
from OpenGL import GL as gl

class MouseLocation:
    pass
    # TODO rename file to ressources

class Application:

    def __init__(self):
        print("Application: init")
        self.window = None
        
        if not glfw.init():
            sys.exit(1)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        title = 'Title'
        self.window = glfw.create_window(500, 400, title, None, None)
        if not self.window:
            sys.exit(2)
        glfw.make_context_current(self.window)

        glfw.set_input_mode(self.window, glfw.STICKY_KEYS, True)
        gl.glClearColor(1.0, 0, 1.0, 0)
    
    def __del__(self):
        print("Application: del")
        glfw.terminate()