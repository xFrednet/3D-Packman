#version 430 core
#define MAX_LIGHT_COUNT 4

#define FRESNEL_REFLECTIVE 0.5

#define AVG_INPUT(v) ((v[0] + v[1] + v[2]) / 3.0)

layout(triangles) in;
layout(triangle_strip, max_vertices = 3) out;

in vec3 v_diffuse[];
in vec3 v_specular[];
in float v_shininess[];
in vec3 v_world_position[];

out vec4 f_color;

// Light setup
uniform vec3 u_light_position[MAX_LIGHT_COUNT];
uniform vec3 u_light_color[MAX_LIGHT_COUNT];
uniform vec3 u_light_attenuation[MAX_LIGHT_COUNT];
uniform uint u_light_count;
uniform vec3 u_camera_position;
uniform vec3 u_global_ambient;

// Frasel
// https://en.wikipedia.org/wiki/Fresnel_equations
// It has come to the point where the main part of creating shaders is understanding
// the formulas. The implementation is very logical by now. That's good I guess ~xFrednet 2020.10.24
// https://en.wikipedia.org/wiki/Refractive_index
// Why, Why do I know such words now? ~xFrednet 2020.10.24
// > The equations assume the interface between the media is flat and that the media are homogeneous and isotropic.
// Holy Fuck no! We just assume that they are because the should be and I don't have the time for this! ~xFrednet 2020.10.24
// Well I just coppied it for now and it works, me happy ~xFrednet 2020.10.24
float calculate_fresnel(vec3 normal, vec3 to_camera) {
    vec3 view_vector = normalize(to_camera);
    float refractive_factor = dot(view_vector, normal);
    refractive_factor = pow(refractive_factor, FRESNEL_REFLECTIVE);
    return clamp(refractive_factor, 0.0, 1.0);
}

vec3 calculate_normal() {
    vec3 a = v_world_position[1] - v_world_position[0];
    vec3 b = v_world_position[2] - v_world_position[0];
    vec3 normal = cross(a, b);
    return normalize(normal);
}

vec3 calculate_light_effect(uint index, vec3 normal, vec3 world_position, vec3 to_camera, vec3 diffuse, vec3 specular, float shininess) {
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
    color += specular * (u_light_color[index] * pow(phong, shininess)) / att_factor;

    return color;
}

void main() {
    vec3 world_position = AVG_INPUT(v_world_position);
    vec3 diffuse = AVG_INPUT(v_diffuse);
    vec3 specular = AVG_INPUT(v_specular);
    float shininess = AVG_INPUT(v_shininess);
    vec3 normal = calculate_normal();
    vec3 to_camera = u_camera_position - world_position;

    vec3 color = vec3(0.0, 0.0, 0.0);
    for (int index = 0; index < MAX_LIGHT_COUNT; index++) {
        if (index >= u_light_count) {
            break;
        }
        color += calculate_light_effect(index, normal, world_position, to_camera, diffuse, specular, shininess);
    }


    float a = 0.6 * calculate_fresnel(normal, to_camera);
    f_color = vec4(color + diffuse * u_global_ambient, a);
    for (int index = 0; index < 3; index++) {
        gl_Position = gl_in[index].gl_Position;
        EmitVertex();
    }

    EndPrimitive();
}