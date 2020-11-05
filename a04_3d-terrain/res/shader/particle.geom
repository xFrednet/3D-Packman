#version 430 core

layout(points) in;
layout(triangle_strip, max_vertices = 4) out;

in int v_sprite_index[];

out vec2 f_tex_coordinate;

uniform mat4 u_transformation_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec3 u_camera_position;
uniform vec3 u_camera_up;

uniform int u_sprite_sheet_rows;
uniform int u_sprite_sheet_columns;

vec2[4] get_tex_coords() {
    int row = v_sprite_index[0] / u_sprite_sheet_columns;
    int column = v_sprite_index[0] % u_sprite_sheet_columns;

    vec2 sprite_steps = vec2(1.0 / u_sprite_sheet_columns, 1.0 / u_sprite_sheet_rows);
    vec2 origin = vec2(sprite_steps.x * column, sprite_steps.y * row);

    // 0    2
    //
    // 1    3
    return vec2[4] (
        origin + sprite_steps * vec2(0.0, 0.0),
        origin + sprite_steps * vec2(0.0, 1.0),
        origin + sprite_steps * vec2(1.0, 0.0),
        origin + sprite_steps * vec2(1.0, 1.0)
    );
}

void main() {
    float size = 1.0;

    // 
    vec3 forward = normalize(u_camera_position - gl_in[0].gl_Position.xyz);
    vec3 right = normalize(cross(u_camera_up, forward));
    vec3 up = normalize(cross(forward, right));
    // ^        | 
    // |        | | := Up
    // |        | - := right
    // x----->  | 
    vec4 offset1 = vec4(right * 0.5 + up * 0.5, 0.0) * size;
    vec4 offset2 = vec4(right * 0.5 - up * 0.5, 0.0) * size;

    // 0       2   | --- := right vector like in the view matrix 
    //   \   /     | 
    //     x ---   | / := offset1 = right * 0.5 + up * 0.5
    //   /   \     | 
    // 1       3   | \ := offset2 = right * 0.5 - up * 0.5

    vec2 tex_coords[] = get_tex_coords();

    f_tex_coordinate = tex_coords[0];
    vec4 position = gl_in[0].gl_Position - offset2;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    f_tex_coordinate = tex_coords[1];
    position = gl_in[0].gl_Position - offset1;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    f_tex_coordinate = tex_coords[2];
    position = gl_in[0].gl_Position + offset1;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    f_tex_coordinate = tex_coords[3];
    position = gl_in[0].gl_Position + offset2;
    gl_Position = u_projection_matrix * (u_view_matrix * position);
    EmitVertex();

    EndPrimitive();
}