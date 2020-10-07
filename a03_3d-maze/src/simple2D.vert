#version 330 core

layout(location = 0) in vec3 position;

out vec3 to_camera;

uniform mat4 transformationMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;


void main(){
    vec4 world_position = transformationMatrix * (vec4(position, 1.0));

    // Lighting
    to_camera = u_camera_position - world_position.xyz;

    gl_Position = projectionMatrix * viewMatrix * world_position;
}