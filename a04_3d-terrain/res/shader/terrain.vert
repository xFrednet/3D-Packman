#version 430 core
#define MAX_LIGHT_COUNT 4

#define X_MAP_MUTIPLIER              250.0
#define Z_MAP_MUTIPLIER              250.0

#define HEIGHT_MAP_MULTIPLIER        10.0
#define HEIGHT_MAP_OFFSET           -100.0

// v for vertex
layout(location = 0) in vec2 in_tex_coords;

// f for fragment
out vec3 v_to_light[MAX_LIGHT_COUNT];
out vec3 v_color;
out vec3 v_world_position;

// u for uniform
uniform mat4 u_transformation_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec3 u_light_position[MAX_LIGHT_COUNT];
uniform uint u_light_count;

uniform sampler2D u_height_map;

void main() {
    vec3 tex_value = texture2D(u_height_map, in_tex_coords).xyz;
    float height = tex_value.x + tex_value.y + tex_value.z;
    vec4 position = vec4(
        in_tex_coords.x * X_MAP_MUTIPLIER,
        height * HEIGHT_MAP_MULTIPLIER + HEIGHT_MAP_OFFSET,
        in_tex_coords.y * Z_MAP_MUTIPLIER,
        1.0
    );

    vec4 world_position = u_transformation_matrix * position;
    v_world_position = world_position.xyz;

    for (int index = 0; index < MAX_LIGHT_COUNT; index++) {
        v_to_light[index] = u_light_position[index] - world_position.xyz;
    }

    // v_surface_normal = (u_transformation_matrix * vec4(in_normal, 0.0)).xyz;
    //v_color = vec3(in_tex_coords.x, in_tex_coords.y, 1.0);
    v_color = texture2D(u_height_map, in_tex_coords).xyz;

    gl_Position = u_projection_matrix * (u_view_matrix * world_position);
}