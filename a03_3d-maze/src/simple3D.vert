#version 330 core
            
layout(location = 0) in vec3 position;

out vec3 vb_color;

uniform mat4 transformationMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;
uniform vec3 object_color;

void main(){
    vb_color = object_color;
    vec4 position_o = transformationMatrix * (vec4(position, 1.0));
    gl_Position = projectionMatrix * viewMatrix * position_o;
}