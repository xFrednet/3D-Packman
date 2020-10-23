#version 430 core
#define MAX_LIGHT_COUNT 4

layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;

in vec3 v_to_light[][MAX_LIGHT_COUNT];
in vec3 v_surface_normal[];
in vec3 v_world_position[];

out vec3 f_to_light[MAX_LIGHT_COUNT];
out vec3 f_surface_normal;
out vec3 f_to_camera;

uniform vec3 u_camera_position;

void main() {

    vec3 a = v_world_position[1] - v_world_position[0];
    vec3 b = v_world_position[2] - v_world_position[0];
    vec3 normal = cross(a, b);
    
    vec3 pos = (v_world_position[0] + v_world_position[1] + v_world_position[2]) / 3;
    f_to_camera = u_camera_position - pos;

    f_to_light = v_to_light[0];
    f_surface_normal = normalize(normal);

    for (int index = 0; index < 3; index++) {
        gl_Position = gl_in[index].gl_Position;
        EmitVertex();
    }

    EndPrimitive();
}