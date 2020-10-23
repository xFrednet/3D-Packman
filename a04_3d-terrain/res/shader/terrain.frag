#version 330 core

#define MAX_LIGHT_COUNT 4u

in vec3 f_to_light[MAX_LIGHT_COUNT];
in vec3 f_to_camera;
in vec3 f_surface_normal;

out vec3 color;

uniform vec3 u_diffuse;
uniform vec3 u_specular;
uniform uint u_shininess;

uniform vec3 u_light_color[MAX_LIGHT_COUNT];
uniform vec3 u_light_attenuation[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_global_ambient;

vec3 get_light_effect(uint index) {
    float d = length(f_to_light[index]);
    vec3 attenuation = u_light_attenuation[index];
    float att_factor = (
        attenuation.x * d * d + 
        attenuation.y * d +
        attenuation.z);
    
    vec3 s = normalize(f_to_light[index]);
    float lambert = max(dot(f_surface_normal, s), 0);
    vec3 color = u_diffuse * (u_light_color[index] * lambert) / att_factor;

    vec3 h = normalize(f_to_camera + f_to_light[index]);
    float phong = max(dot(f_surface_normal, h), 0);
    color += u_specular * (u_light_color[index] * pow(phong, u_shininess)) / att_factor;

    return color;
}

void main() {
    
    color = vec3(0.0, 0.0, 0.0);

    for (uint index = 0u; index < MAX_LIGHT_COUNT ; index++) {
        if (index < u_light_count) {
            color += get_light_effect(index);
        }
    }

    color += u_diffuse * u_global_ambient;
}