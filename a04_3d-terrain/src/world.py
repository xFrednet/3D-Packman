import esper
import glm

import terrain

from graphics import frame_system

class World(esper.World):
    def __init__(self, resolution):
        super().__init__()
        self.resolution = resolution
        self.delta = 0.00001
        self.terrain = terrain.Terrain()
        
        self._setup_systems()

        self.terrain.create_chunks(self)

        print("World was created")

    def _setup_systems(self):
        self.add_processor(frame_system.PrepareFrameSystem())
        self.add_processor(terrain.TerrainRenderer())
        self.add_processor(frame_system.FinishFrameSystem())

    def cleanup(self):
        print("World cleanup complete")
