#version 330 core
#define MAX_LIGHT_COUNT 4

in vec3 to_light[MAX_LIGHT_COUNT];
in vec3 to_camera;
in vec3 surface_normal;

out vec3 color;

// C++ naming conventions are fun *.*
// I actually like them and now I'm interested how a Rust shader language would look like
// Well that's a question for another time ~xFrednet 2020.10.05

// One material per object
uniform vec3 u_color;
uniform vec3 u_diffuse;
uniform vec3 u_specular;
uniform uint u_shininess;

uniform vec3 u_light_color[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_global_ambient;

void main() {
    
    color = vec3(0.0, 0.0, 0.0);

    for (int index = 0; index < MAX_LIGHT_COUNT; index++) {
        vec3 s = normalize(to_light[index]);
        float lambert = max(dot(surface_normal, s), 0);
        color += u_diffuse * u_light_color[index] * lambert;

        vec3 h = normalize(to_camera + to_light[index]);
        float phong = max(dot(surface_normal, h), 0);
        color += u_specular * u_light_color[index] * pow(phong, u_shininess);
    }

    //color = surface_normal;
    color += u_diffuse * u_global_ambient;
}