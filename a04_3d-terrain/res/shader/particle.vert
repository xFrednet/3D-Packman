#version 430 core
#define MAX_PARTICLE_COUNT 256

// v for vertex
layout(location = 0) in float in_id;

out int v_sprite_index;

uniform float u_world_time;

uniform float u_emit_times[MAX_PARTICLE_COUNT];
uniform vec3 u_emit_positions[MAX_PARTICLE_COUNT];
uniform int u_sprite_incices[MAX_PARTICLE_COUNT];

void main() {
    int particle_id = int(in_id);
    float life_time = u_world_time - u_emit_times[particle_id];

    v_sprite_index = u_sprite_incices[particle_id];

    gl_Position = vec4(u_emit_positions[particle_id], 1.0);
    gl_Position.y += life_time;
}