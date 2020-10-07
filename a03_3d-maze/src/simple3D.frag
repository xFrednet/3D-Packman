#version 330 core
#define MAX_LIGHT_COUNT 4u

in vec3 to_light[MAX_LIGHT_COUNT];
in vec3 to_camera;
in vec3 surface_normal;

out vec3 color;

// C++ naming conventions are fun *.*
// I actually like them and now I'm interested how a Rust shader language would look like
// Well that's a question for another time ~xFrednet 2020.10.05
// Not that I'm working on this again I notice that this is a mixture of the c++
// and rust naming convention not pure c++... well who cares right? ~ xFrednet 2020.10.06

// One material per object
uniform vec3 u_diffuse;
uniform vec3 u_specular;
uniform uint u_shininess;

uniform vec3 u_light_color[MAX_LIGHT_COUNT];
uniform vec3 u_light_attenuation[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_global_ambient;

vec3 get_light_effect(uint index) {
    float d = length(to_light[index]);
    vec3 attenuation = u_light_attenuation[index];
    float att_factor = (
        attenuation.x * d * d + 
        attenuation.y * d +
        attenuation.z);
    
    vec3 s = normalize(to_light[index]);
    float lambert = max(dot(surface_normal, s), 0);
    vec3 color = u_diffuse * (u_light_color[index] * lambert) / att_factor;

    vec3 h = normalize(to_camera + to_light[index]);
    float phong = max(dot(surface_normal, h), 0);
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