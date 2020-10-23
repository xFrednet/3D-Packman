#version 330 core
#define MAX_LIGHT_COUNT 4

// v for vertex
layout(location = 0) in vec3 v_position;
layout(location = 1) in vec3 v_normal;

// f for fragment
out vec3 f_to_light[MAX_LIGHT_COUNT];
out vec3 f_surface_normal;
out vec3 f_to_camera;

// u for uniform
uniform mat4 u_transformation_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec3 u_light_position[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_camera_position;

void main() {
    vec4 world_position = u_transformation_matrix * vec4(v_position, 1.0);

    f_to_camera = u_camera_position - world_position.xyz;
    for (int index = 0; index < MAX_LIGHT_COUNT; index++) {
        f_to_light[index] = u_light_position[index] - world_position.xyz;
    }

    f_surface_normal = (u_transformation_matrix * vec4(v_normal, 0.0)).xyz;

    gl_Position = u_projection_matrix * (u_view_matrix * world_position);
}