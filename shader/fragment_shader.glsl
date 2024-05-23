#version 330 core
in vec2 v_texcoord;
out vec4 fragColor;

uniform sampler2D texture1;

void main() {
    fragColor = texture(texture1, v_texcoord);
}
