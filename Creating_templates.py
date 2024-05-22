import glfw
import moderngl
import numpy as np
import cv2


def main():
    width, height = 800, 600

    if not glfw.init():
        return

    # Создание невидимого окна
    glfw.window_hint(glfw.VISIBLE, glfw.FALSE)
    window = glfw.create_window(width, height, "Rectangle Renderer", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    ctx = moderngl.create_context()

    prog = ctx.program(
        vertex_shader=open("shader/vertex_shader.glsl").read(),
        fragment_shader=open("shader/fragment_shader.glsl").read()
    )

    vbo = ctx.buffer(np.array([
        -0.5, -0.5,
         0.5, -0.5,
        -0.5,  0.5,
         0.5,  0.5,
    ], dtype='f4').tobytes())

    vao = ctx.simple_vertex_array(prog, vbo, 'in_position')

    rectangles = [
        {"offset": (0.0, 0.8), "size": (0.1, 0.05)},  # Rectangle 1
        {"offset": (0.5, -0.2), "size": (0.15, 0.1)},  # Rectangle 2
        {"offset": (0.0, 0.2), "size": (0.1, 0.05)},  # Rectangle 3
        {"offset": (-0.5, -0.2), "size": (0.1, 0.05)},  # Rectangle 4
        {"offset": (0.0, -0.6), "size": (0.15, 0.1)},  # Rectangle 5
    ]

    ctx.clear(0, 0, 0)

    for rect in rectangles:
        prog['offset'].value = rect['offset']
        prog['size'].value = rect['size']
        vao.render(moderngl.TRIANGLE_STRIP)

    # Чтение пикселей из буфера
    data = ctx.screen.read(components=3)
    image = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


   # Добавление номеров над прямоугольниками
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (150, 150, 150)
    font_thickness = 2

    for i, rect in enumerate(rectangles):
        text = str(i + 1)
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = int((rect['offset'][0] + 1) / 2 * width - text_size[0] / 2)
        text_y = int(((rect['offset'][1] - rect['size'][1] + 1) / 2) * height - text_size[1] / 2)
        cv2.putText(image, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

    # Сохранение изображения в файл
    cv2.imwrite("hash/output.png", image)

    glfw.terminate()


if __name__ == "__main__":
    main()
