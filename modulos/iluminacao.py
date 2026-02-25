"""
Módulo 4 - Iluminação
Dois objetos 3D com projeção perspectiva.
Objeto 1: iluminação Flat (constante por face).
Objeto 2: iluminação Gouraud (interpolação por vértice - GL_SMOOTH).
"""
import sys
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_FLAT, GL_SMOOTH,
    GL_PROJECTION, GL_MODELVIEW,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_SPECULAR as GL_MAT_SPECULAR,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glFrustum,
    glEnable, glDisable,
    glLightfv, glMaterialfv, glShadeModel,
    glTranslatef,
)
from OpenGL.GLU import gluLookAt
from OpenGL import GL
from utils.shapes import draw_cube, draw_pyramid_smooth

# Posição da luz (homogênea: 1 = pontual, 0 = direcional)
LIGHT_POS = [2, 3, 4, 1.0]


def run():
    if not glfw.init():
        print("Falha ao inicializar GLFW", file=sys.stderr)
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(800, 600, "Módulo 4 - Iluminação (Flat + Gouraud)", None, None)
    if not win:
        glfw.terminate()
        print("Falha ao criar janela", file=sys.stderr)
        return
    glfw.make_context_current(win)
    glClearColor(0.08, 0.08, 0.12, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)

    # Luz
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.6, 0.6, 0.6, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POS)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glViewport(0, 0, w, h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h else 1
        near, far = 0.1, 100
        top = 0.5
        right = top * aspect
        glFrustum(-right, right, -top, top, near, far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(2, 1.5, 4, 0, 0, 0, 0, 1, 0)
        glLightfv(GL_LIGHT0, GL_POSITION, LIGHT_POS)

        # Objeto 1: Cubo com iluminação Flat
        glShadeModel(GL_FLAT)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.2, 0.5, 0.8, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_MAT_SPECULAR, (0.4, 0.4, 0.4, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (40.0,))
        glTranslatef(-0.8, 0, 0)
        draw_cube(0.4)

        # Objeto 2: Pirâmide com iluminação Gouraud (SMOOTH)
        glShadeModel(GL_SMOOTH)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.8, 0.4, 0.2, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_MAT_SPECULAR, (0.5, 0.5, 0.5, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (50.0,))
        glTranslatef(1.6, 0, 0)
        draw_pyramid_smooth(0.4, 0.6)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
    glfw.terminate()
