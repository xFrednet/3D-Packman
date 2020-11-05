#version 430 core

in vec2 f_tex_coordinate;

out vec4 color;

uniform sampler2D u_sprite_sheet;

void main() {
    color = texture2D(u_sprite_sheet, f_tex_coordinate);
}