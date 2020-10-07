# Lighting

## Lighting components
The required lighting information is stored within the game as a part of the [ECT](.docs/ecs.md). The main components needed for the lighting setup are:

| Component      | Responsibility                                                          |
| -------------- | ----------------------------------------------------------------------- |
| Position       | Used by lights and objects to determine their position.                 |
| ObjectMaterial | Stores the diffuse and specular values of the object.                   |
| Light          | Stores the color of the light and the attenuation values for the shader |

There are other components like the `VBA` and `TransformationMatrix` that are also required for drawing objects. However these are not described in this file because they are not directly a part of the lighting model. 

## Shader layout
The lighting calculations are done in two stages. The first calculations are done in the vertex shader and then passed to the fragment shader where the final lighting value is determined.

### Preparation
We need to do some preparation before drawing the actual object it self. The position and normal vector of a vertex is stored in the VBO and is passed to the vertex shader.

Model and scene specific data is stored in [OpenGL uniform](https://www.khronos.org/opengl/wiki/Uniform_(GLSL)) variables. The scene specific information like the light `positioning`, `color`, `attenuation` values and the camera position are uploaded at the start of the frame by the `PrepareFrameSystem`.

### Vertex shader
The vertex shader calculates the vector S in our lighting calculations. It is a `vec3` value called `to_light` in our shaders. 

### Fragment shader
The pixel shader calculates the lighting with the formula we had in lecture 8. An addition we added was the attenuation of the light. 



### Lighting formula
![Awesome lighting formula](res/fs_lighting_formula.png)

### Q&A about this layout
* Why do we calculate lambert, phong and other values in the pixel shader?

### 

## Multiple light setup

## attenuation
