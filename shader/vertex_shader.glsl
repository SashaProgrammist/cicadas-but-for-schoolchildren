#version 330 core
layout(location = 0) in vec2 in_position;
uniform vec2 offset;
uniform vec2 size;

void main() {
    gl_Position = vec4(in_position * size + offset, 0.0, 1.0);
}
