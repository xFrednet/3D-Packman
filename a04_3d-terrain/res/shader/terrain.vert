#version 430 core
#define MAX_LIGHT_COUNT 4

#define X_MAP_MUTIPLIER              250.0
#define Z_MAP_MUTIPLIER              250.0

#define HEIGHT_MAP_MULTIPLIER         50.0
#define HEIGHT_MAP_OFFSET           -100.0

#define RGB(r, g, b) vec3(r/255.0, g/255.0, b/255.0)

struct Material {
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

// Water 10%
#define MATERIAL_COUNT 5
const Material TERRAIN_MATERIAL[MATERIAL_COUNT + 1] = Material[](
    Material(RGB(130.0,  11.0,  70.0), vec3(0.0, 0.0, 0.0), 1.0),
    Material(RGB(240.0, 218.0, 161.0), vec3(0.0, 0.0, 0.0), 1.0),
    Material(RGB( 86.0, 107.0,  52.0), vec3(0.0, 0.0, 0.0), 1.0),
    Material(RGB(100.0,  60.0,  60.0), vec3(0.0, 0.0, 0.0), 1.0),
    Material(RGB(221.0, 221.0, 221.0), vec3(0.0, 0.0, 0.0), 1.0),
    Material(RGB(  0.0,   0.0,   0.0), vec3(0.0, 0.0, 0.0), 0.0)
);

// v for vertex
layout(location = 0) in vec2 in_tex_coords;

// f for fragment
out vec3 v_diffuse;
out vec3 v_specular;
out float shininess;
out vec3 v_world_position;

// u for uniform
uniform mat4 u_transformation_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform sampler2D u_height_map;

void main() {
    vec3 tex_value = texture2D(u_height_map, in_tex_coords).xyz;
    float height = (tex_value.x + tex_value.y + tex_value.z) / 3.0;
    vec4 position = vec4(
        in_tex_coords.x * X_MAP_MUTIPLIER,
        height * HEIGHT_MAP_MULTIPLIER + HEIGHT_MAP_OFFSET,
        in_tex_coords.y * Z_MAP_MUTIPLIER,
        1.0
    );

    float material_selection = height * MATERIAL_COUNT;
    int index = int(floor(material_selection));
    float lerp = material_selection - floor(material_selection);
    Material mat_a = TERRAIN_MATERIAL[index];
    Material mat_b = TERRAIN_MATERIAL[index + 1];

    v_diffuse = mix(mat_a.diffuse, mat_b.diffuse, lerp);
    v_specular = mix(mat_a.specular, mat_b.specular, lerp);
    shininess = mix(mat_a.shininess, mat_b.shininess, lerp);

    vec4 world_position = u_transformation_matrix * position;
    v_world_position = world_position.xyz;

    gl_Position = u_projection_matrix * (u_view_matrix * world_position);
}