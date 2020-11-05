#version 430 core
#define MAX_PARTICLE_COUNT 256

// v for vertex
layout(location = 0) in float in_id;

out vec3 v_color;

uniform float u_world_time;

uniform float u_emit_times[MAX_PARTICLE_COUNT];
uniform vec3 u_emit_positions[MAX_PARTICLE_COUNT];
uniform int u_sprite_incices[MAX_PARTICLE_COUNT];

void main() {
    int i_id = int(in_id);
    float f_id = float(i_id);
    v_color = vec3(f_id / 256.0, f_id / 256.0, f_id / 256.0);

    gl_Position = vec4(f_id, f_id, f_id, 1.0);
}