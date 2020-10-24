#version 430 core
#define MAX_LIGHT_COUNT 4

#define AVG_INPUT(v) ((v[0] + v[1] + v[2]) / 3.0)

layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;

in vec3 v_diffuse[];
in vec3 v_specular[];
in vec3 v_world_position[];

out vec3 f_color;

// Light setup
uniform vec3 u_light_position[MAX_LIGHT_COUNT];
uniform vec3 u_light_color[MAX_LIGHT_COUNT];
uniform vec3 u_light_attenuation[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_camera_position;
uniform vec3 u_global_ambient;

// Material
uniform vec3 u_diffuse;
uniform vec3 u_specular;
uniform uint u_shininess;

vec3 calculate_normal() {
    vec3 a = v_world_position[1] - v_world_position[0];
    vec3 b = v_world_position[2] - v_world_position[0];
    vec3 normal = cross(a, b);
    return normalize(normal);
}

vec3 calculate_light_effect(uint index, vec3 normal, vec3 world_position, vec3 to_camera, vec3 diffuse, vec3 specular) {
    vec3 to_light = u_light_position[index] - world_position;
    
    // Attenuation
    float d = length(to_light);
    vec3 attenuation = u_light_attenuation[index];
    float att_factor = (
        attenuation.x * d * d + 
        attenuation.y * d +
        attenuation.z);
    
    vec3 s = normalize(to_light);
    float lambert = max(dot(normal, s), 0);
    vec3 color = diffuse * (u_light_color[index] * lambert) / att_factor;

    vec3 h = normalize(to_camera + to_light);
    float phong = max(dot(normal, h), 0);
    color += specular * (u_light_color[index] * pow(phong, u_shininess)) / att_factor;

    return color;
}

void main() {
    vec3 world_position = AVG_INPUT(v_world_position);
    vec3 diffuse = AVG_INPUT(v_diffuse);
    vec3 specular = AVG_INPUT(v_specular);
    vec3 normal = calculate_normal();
    vec3 to_camera = u_camera_position - world_position;

    vec3 color = vec3(0.0, 0.0, 0.0);
    for (int index = 0; index < MAX_LIGHT_COUNT; index++) {
        if (index >= u_light_count) {
            break;
        }
        color += calculate_light_effect(index, normal, world_position, to_camera, diffuse, specular);
    }

    f_color = color + u_diffuse * u_global_ambient;
    for (int index = 0; index < 3; index++) {
        gl_Position = gl_in[index].gl_Position;
        EmitVertex();
    }

    EndPrimitive();
}