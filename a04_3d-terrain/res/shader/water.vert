#version 430 core
#define PI                   3.1415926535897932384626433832795
#define WAVE_LENGTH            4.0
#define X_AMPLITUDE            0.2
#define Y_AMPLITUDE            0.2
#define Z_AMPLITUDE            0.2

#define X_MAP_MUTIPLIER              500.0
#define Z_MAP_MUTIPLIER              500.0

#define HEIGHT_MAP_MULTIPLIER        100.0
#define HEIGHT_MAP_OFFSET            -30.0

#define RGB(r, g, b) vec3(r/255.0, g/255.0, b/255.0)


// Water 10%

// v for vertex
layout(location = 0) in vec2 in_tex_coords;

// f for fragment
out vec3 v_diffuse;
out vec3 v_specular;
out float v_shininess;
out vec3 v_world_position;
out int v_visible;

// u for uniform
uniform mat4 u_transformation_matrix;

uniform float u_world_delta;
uniform sampler2D u_height_map;

float get_offset(float a, float b, float factor_1, float factor_2) {
    float a_in = (u_world_delta * 0.1) + (b + a * factor_1) * 117.0;
    float b_in = (u_world_delta * 0.1) + (a + b * factor_2) * 117.0;
    return sin(a_in * 2.0 * PI) + cos(b_in * 2.0 * PI);
}

void main() {
    vec3 tex_value = texture2D(u_height_map, in_tex_coords).xyz;
    float height = ((tex_value.x + tex_value.y + tex_value.z) / 3.0) * HEIGHT_MAP_MULTIPLIER + HEIGHT_MAP_OFFSET;
    vec4 position = vec4(
        (in_tex_coords.x - 0.5) * X_MAP_MUTIPLIER,
        0.0,
        (in_tex_coords.y - 0.5) * Z_MAP_MUTIPLIER,
        1.0
    );

    position.x += get_offset(in_tex_coords.x * 2.1, in_tex_coords.y * 2.3, 0.1, 0.2) * X_AMPLITUDE;
    position.y += get_offset(in_tex_coords.x * 2.3, in_tex_coords.y * 2.5, 0.3, 0.4) * Y_AMPLITUDE;
    position.z += get_offset(in_tex_coords.x * 2.7, in_tex_coords.y * 2.2, 0.2, 0.5) * Z_AMPLITUDE;

    v_diffuse = RGB(10.0, 10.0, 155.0);
    v_specular = RGB(12.0, 12.0, 12.0);
    v_shininess = 12;
    v_visible = (height > position.y + 1.0) ? 0 : 1;

    vec4 world_position = u_transformation_matrix * position;
    v_world_position = world_position.xyz;
}