import glm
import esper

import components as com

class MovementSystem(esper.Processor):
    def process(self):
        for _id, (position, velocity) in self.world.get_components(com.Position, com.Velocity):
            position.value = position.value + velocity.value