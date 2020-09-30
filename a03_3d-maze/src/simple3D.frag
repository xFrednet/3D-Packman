#version 330 core
            
in vec3 vb_color;

out vec3 color;

void main(){
    color = vec3((vb_color.x + 1) / 2, (vb_color.y + 1) / 2, (vb_color.z + 1) / 2);
}