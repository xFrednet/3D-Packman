#version 330 core

layout(location = 0) in vec4 v_position;
layout(location = 1) in vec4 v_normal;

out vec4 frag_color;

uniform mat4 u_transformation_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

void main() {
    vec4 world_position = u_transformation_matrix * v_position;

    frag_color = v_normal;
    gl_Position = u_projection_matrix * (u_view_matrix * world_position);
}