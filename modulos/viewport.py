"""
Módulo 3 - ViewPort
Um objeto 3D exibido em 3 viewports com 3 posições de câmera diferentes.
Projeção ortogonal obrigatória.
"""
import sys
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_PROJECTION, GL_MODELVIEW,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glEnable,
)
from OpenGL.GLU import gluLookAt
from utils.shapes import draw_cube

# Três câmeras: frente, lado direito, topo
CAMERAS = [
    {"eye": (0, 0, 4), "center": (0, 0, 0), "up": (0, 1, 0)},   # frente (+Z)
    {"eye": (4, 0, 0), "center": (0, 0, 0), "up": (0, 1, 0)},   # lado (+X)
    {"eye": (0, 4, 0), "center": (0, 0, 0), "up": (0, 0, -1)},   # topo (+Y, up = -Z)
]


def run():
    if not glfw.init():
        print("Falha ao inicializar GLFW", file=sys.stderr)
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(900, 300, "Módulo 3 - ViewPort (3 câmeras, projeção ortogonal)", None, None)
    if not win:
        glfw.terminate()
        print("Falha ao criar janela", file=sys.stderr)
        return
    glfw.make_context_current(win)
    glClearColor(0.1, 0.1, 0.15, 1.0)
    glEnable(GL_DEPTH_TEST)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        third = w // 3
        dim = 2.5
        for i in range(3):
            x = i * third
            glViewport(x, 0, third, h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            aspect = third / h if h else 1
            if aspect >= 1:
                glOrtho(-dim * aspect, dim * aspect, -dim, dim, -10, 10)
            else:
                glOrtho(-dim, dim, -dim / aspect, dim / aspect, -10, 10)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            cam = CAMERAS[i]
            gluLookAt(
                cam["eye"][0], cam["eye"][1], cam["eye"][2],
                cam["center"][0], cam["center"][1], cam["center"][2],
                cam["up"][0], cam["up"][1], cam["up"][2],
            )
            draw_cube(0.5)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
    glfw.terminate()
