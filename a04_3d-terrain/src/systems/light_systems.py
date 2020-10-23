import esper

from resources import LightSetup
from components import Transformation, Light

class UpdateLightSetupSystem(esper.Processor):
    def process(self):
        light_setup: LightSetup = self.world.light_setup
        light_setup.camera_position = self.world.component_for_entity(self.world.camera_id, Transformation).position

        index = 0
        for _id, (light, transformation) in self.world.get_components(Light, Transformation):
            if light.enabled:
                light_setup.light_positions[index] = transformation.position
                light_setup.lights[index] = light
                index += 1
                if index >= LightSetup.MAX_LIGHT_COUNT: break

        light_setup.light_count = index