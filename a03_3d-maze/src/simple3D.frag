#version 330 core
#define MAX_LIGHT_COUNT 4

in vec3 vb_color;

out vec3 color;

// C++ naming conventions are fun *.*
// I actually like them and now I'm interested how a Rust shader language would look like
// Well that's a question for another time ~xFrednet 2020.10.05

// One material per object
uniform vec3 u_color;
uniform vec3 u_diffuse;
uniform vec3 u_specular;
uniform int  u_shininess;

uniform vec3 u_light_color[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_global_ambient;

void main(){
    color = u_color * u_global_ambient;
}