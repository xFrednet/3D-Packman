#version 330 core
#define MAX_LIGHT_COUNT 4

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

out vec3 vb_color;

uniform mat4 transformationMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform vec3 u_light_position[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_camera_position;

void main(){
    vb_color = vec3(1.0, 1.0, 1.0);
    vec4 position_o = transformationMatrix * (vec4(position, 1.0));
    gl_Position = projectionMatrix * viewMatrix * position_o;
}