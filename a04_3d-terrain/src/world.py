import esper
import glm

class World(esper.World):
    def __init__(self, resolution):
        super().__init__()
        self.resolution = resolution
        self.delta = 0.00001
        print("World was created")

    def cleanup(self):
        print("World cleanup complete")
