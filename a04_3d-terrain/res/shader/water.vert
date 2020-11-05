#version 430 core
#define PI                             3.14159265358979
#define WAVE_LENGTH                    4.0
#define X_AMPLITUDE                    0.2
#define Y_AMPLITUDE                    0.2
#define Z_AMPLITUDE                    0.2

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

float get_offset(float a, float b, float factor_1, float factor_2, float factor_3) {
    float a_in = (u_world_delta * 0.1003 * factor_3) + (b + a * factor_1) * 117.0;
    float b_in = (u_world_delta * 0.1007 * factor_3) + (a + b * factor_2) * 117.0;
    return sin(a_in * 2.0 * PI) + cos(b_in * 2.0 * PI);
}

// Function(sin(((x * 0.1 * 0.97) + ((b * 2.3) + (a * 2.1) * 0.1) * 117.0) * 2.0 * pi) + cos(((x * 0.1 * 0.97) + ((a * 2.1) + (b * 2.3) * 0.2) * 117.0) * 2.0 * pi), 0, 100)
// Function(sin(((x * 0.1 * 0.99) + ((b * 2.5) + (a * 2.3) * 0.3) * 117.0) * 2.0 * pi) + cos(((x * 0.1 * 0.99) + ((a * 2.3) + (b * 2.5) * 0.4) * 117.0) * 2.0 * pi), 0, 100)
// Function(sin(((x * 0.1 * 1.04) + ((b * 2.2) + (a * 2.7) * 0.2) * 117.0) * 2.0 * pi) + cos(((x * 0.1 * 1.04) + ((a * 2.7) + (b * 2.2) * 0.5) * 117.0) * 2.0 * pi), 0, 100)

void main() {
    vec3 tex_value = texture2D(u_height_map, in_tex_coords).xyz;
    float height = ((tex_value.x + tex_value.y + tex_value.z) / 3.0) * HEIGHT_MAP_MULTIPLIER + HEIGHT_MAP_OFFSET;
    vec4 position = vec4(
        (in_tex_coords.x - 0.5) * X_MAP_MUTIPLIER,
        0.0,
        (in_tex_coords.y - 0.5) * Z_MAP_MUTIPLIER,
        1.0
    );

    position.x += get_offset(in_tex_coords.x * 2.1, in_tex_coords.y * 2.3, 0.1, 0.2, 0.97) * X_AMPLITUDE;
    position.y += get_offset(in_tex_coords.x * 2.3, in_tex_coords.y * 2.5, 0.3, 0.4, 0.99) * Y_AMPLITUDE;
    position.z += get_offset(in_tex_coords.x * 2.7, in_tex_coords.y * 2.2, 0.2, 0.5, 1.04) * Z_AMPLITUDE;

    v_diffuse = RGB(10.0, 10.0, 155.0);
    v_specular = RGB(12.0, 12.0, 12.0);
    v_shininess = 12;
    v_visible = (height > position.y + 1.0) ? 0 : 1;

    vec4 world_position = u_transformation_matrix * position;
    v_world_position = world_position.xyz;
}