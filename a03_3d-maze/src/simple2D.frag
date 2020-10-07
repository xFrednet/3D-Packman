#version 330 core


in vec3 surface_normal;

out vec3 color;

// One material per object
uniform vec3 u_color;

void main() {

    color = vec3(0.0, 0.0, 0.0);
}