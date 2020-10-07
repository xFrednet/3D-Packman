#version 330 core
#define MAX_LIGHT_COUNT 4

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

out vec3 to_light[MAX_LIGHT_COUNT];
out vec3 to_camera;
out vec3 surface_normal;

uniform mat4 transformationMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform vec3 u_light_position[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_camera_position;

void main(){
    vec4 world_position = transformationMatrix * (vec4(position, 1.0));
    
    // Lighting
    to_camera = u_camera_position - world_position.xyz;
    for (int index = 0; index < MAX_LIGHT_COUNT; index++) {
        to_light[index] = u_light_position[index] - world_position.xyz;
    }
    surface_normal = normalize((transformationMatrix * vec4(normal, 0.0)).xyz);

    gl_Position = projectionMatrix * viewMatrix * world_position;
}