#version 430 core

#define MAX_LIGHT_COUNT 4u

in vec3 f_color;

out vec3 color;

void main() {
    color = f_color;
}