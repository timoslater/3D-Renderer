#version 330 core

uniform vec3 render_color; 
out vec4 color;

void main() {
  color = vec4(render_color, 1);
}
