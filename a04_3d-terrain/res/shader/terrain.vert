#version 330 core

layout(location = 0) in vec4 v_position;
layout(location = 1) in vec4 v_normal;

out vec4 frag_color;

void main() {
    frag_color = v_normal;
    gl_Position = v_position;
}