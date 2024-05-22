#version 330 core

in vec3 in_position;
uniform mat4 model_mat;

void main() {
  vec4 model_coords = vec4(in_position, 1.0); 
  gl_Position = model_mat * model_coords;
}
