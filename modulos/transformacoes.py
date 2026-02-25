"""
Módulo 1 - Transformações Geométricas
Objeto único (cubo) com as 5 transformações exibidas visualmente:
Translação, Escala, Rotação, Reflexão/Flip, Cisalhamento.
"""
import sys
import ctypes
import numpy as np
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_PROJECTION, GL_MODELVIEW,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glTranslatef, glScalef, glRotatef, glMultMatrixf,
    glPushMatrix, glPopMatrix, glColor3f, glEnable,
)
from utils.shapes import draw_cube


def matrix_to_gl(m):
    """Converte matriz 4x4 numpy (row-major) para formato OpenGL (column-major)."""
    return (ctypes.c_float * 16)(*m.T.astype(np.float32).flatten())


def shear_matrix(shx=0.3, shy=0.0, shz=0.0):
    """Matriz 4x4 de cisalhamento em X (xy, xz)."""
    return np.array([
        [1, shx, 0, 0],
        [shy, 1, 0, 0],
        [shz, 0, 1, 0],
        [0, 0, 0, 1],
    ], dtype=np.float32)


def run():
    if not glfw.init():
        print("Falha ao inicializar GLFW", file=sys.stderr)
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(1000, 600, "Módulo 1 - Transformações Geométricas", None, None)
    if not win:
        glfw.terminate()
        print("Falha ao criar janela", file=sys.stderr)
        return
    glfw.make_context_current(win)
    glClearColor(0.15, 0.15, 0.2, 1.0)
    glEnable(GL_DEPTH_TEST)

    angle = 0.0

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glViewport(0, 0, w, h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Projeção ortogonal: 5 colunas
        col_width = w / 5
        for col in range(5):
            x = int(col * col_width)
            width = int(col_width)
            glViewport(x, 0, width, h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-2, 2, -1.2, 1.2, -5, 5)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            # Câmera fixa
            glTranslatef(0, 0, -3)
            glRotatef(20, 1, 0, 0)
            glRotatef(angle * 0.5, 0, 1, 0)

            glPushMatrix()
            if col == 0:
                glTranslatef(0.4, 0.2, 0)
                glColor3f(1, 0.4, 0.4)
            elif col == 1:
                glScalef(1.4, 1.4, 1.4)
                glColor3f(0.4, 1, 0.4)
            elif col == 2:
                glRotatef(angle, 0, 1, 0)
                glColor3f(0.4, 0.4, 1)
            elif col == 3:
                glScalef(-1, 1, 1)  # Reflexão no eixo X
                glColor3f(1, 1, 0.4)
            else:
                glMultMatrixf(matrix_to_gl(shear_matrix(0.5, 0.2, 0)))
                glColor3f(1, 0.5, 1)
            draw_cube(0.35)
            glPopMatrix()

        glViewport(0, 0, w, h)
        angle += 0.8

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
    glfw.terminate()
