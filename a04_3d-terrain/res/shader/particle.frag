#version 430 core

in vec2 f_tex_coordinate;

out vec4 color;

void main() {
    color = vec4(f_tex_coordinate.x, 0.0, f_tex_coordinate.y, 1.0);
}