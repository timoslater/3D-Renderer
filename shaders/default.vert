#version 330 core

in vec3 in_position;
uniform mat4 model_mat;
uniform mat4 view_mat;
uniform mat4 projection_mat;

void main() {
  vec4 model_coords = vec4(in_position, 1.0); 
  mat4 a = view_mat * projection_mat;
  mat4 mvp = view_mat * model_mat;
  gl_Position = mvp * model_coords;
}
