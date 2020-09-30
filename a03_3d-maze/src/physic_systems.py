import glm
import esper

import components as com

class MovementSystem(esper.Processor):
    def process(self):
        for _id, (position, velocity, rotation) in self.world.get_components(com.Position, com.Velocity, com.Rotation):
            position.value = position.value + velocity.value * self.world.delta
            rotation.value.z += 1.0 * self.world.delta