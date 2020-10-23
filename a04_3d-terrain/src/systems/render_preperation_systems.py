import glm
import esper

from graphics import graphics_math
from components import Transformation, TransformationMatrix

class BuildTransformationMatrixSystem(esper.Processor):
    def process(self):
        for _id, (target, transformation) in self.world.get_components(
                TransformationMatrix,
                Transformation):
            target.value = graphics_math.build_transformation_matrix(
                transformation.position,
                transformation.rotation,
                transformation.scale)
