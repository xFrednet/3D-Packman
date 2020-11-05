#version 430 core

layout(points) in;
layout(triangle_strip, max_vertices = 4) out;

in vec3 v_color[];

out vec3 f_color;

uniform mat4 u_transformation_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec3 u_camera_position;
uniform vec3 u_camera_up;

void main() {
    f_color = v_color[0];
    float size = 1.0;

    vec3 forward = normalize(u_camera_position - gl_in[0].gl_Position.xyz);
    vec3 right = normalize(cross(u_camera_up, forward));
    vec3 up = normalize(cross(forward, right));
    // ^        | 
    // |        | | := Up
    // |        | - := right
    // x----->  | 
    vec4 offset1 = vec4(right * 0.5 + up * 0.5, 0.0) * size;
    vec4 offset2 = vec4(right * 0.5 - up * 0.5, 0.0) * size;

    // 0       2   | --- := right vector like in the view matrix 
    //   \   /     | 
    //     x ---   | / := offset1 = right * 0.5 + up * 0.5
    //   /   \     | 
    // 1       3   | \ := offset2 = right * 0.5 - up * 0.5

    vec4 position = gl_in[0].gl_Position - offset2;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    position = gl_in[0].gl_Position - offset1;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    position = gl_in[0].gl_Position + offset1;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    position = gl_in[0].gl_Position + offset2;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    EndPrimitive();
}