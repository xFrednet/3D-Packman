#version 430 core
#define DEFAULT_MAX_VERTEX_COUNT 256

// v for vertex
layout(location = 0) in float in_id;

out vec3 v_color;

uniform mat4 u_transformation_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

void main() {
    int i_id = int(in_id);
    float f_id = float(i_id);
    v_color = vec3(f_id / 256.0, f_id / 256.0, f_id / 256.0);

    vec4 position = vec4(f_id, f_id, f_id, 1.0);
    gl_Position = u_projection_matrix * (u_view_matrix * position);
}