"""
Módulo 2 - Projeção
Visualização de um objeto 3D com:
- Matriz de projeção configurável (perspectiva / ortogonal)
- Posição da câmera (LookAt) alterável por teclado
"""
import sys
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_PROJECTION, GL_MODELVIEW,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glFrustum, glEnable,
)
from OpenGL.GLU import gluLookAt
from utils.shapes import draw_cube

# Estado da câmera e projeção
CAM = {"eye_x": 3, "eye_y": 2, "eye_z": 4, "center_x": 0, "center_y": 0, "center_z": 0}
PROJ = {"perspective": True}  # True = perspectiva, False = ortogonal
STEP = 0.4


def run():
    if not glfw.init():
        print("Falha ao inicializar GLFW", file=sys.stderr)
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(800, 600, "Módulo 2 - Projeção (WASD+QE câmera, P=troca projeção)", None, None)
    if not win:
        glfw.terminate()
        print("Falha ao criar janela", file=sys.stderr)
        return
    glfw.make_context_current(win)
    glClearColor(0.12, 0.12, 0.18, 1.0)
    glEnable(GL_DEPTH_TEST)

    def on_key(window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_P:
            PROJ["perspective"] = not PROJ["perspective"]
            return
        # Vetor direção da câmera (eye -> center)
        dx = CAM["center_x"] - CAM["eye_x"]
        dy = CAM["center_y"] - CAM["eye_y"]
        dz = CAM["center_z"] - CAM["eye_z"]
        # Normalizar no plano XZ para movimento horizontal
        from math import sqrt
        len_xz = sqrt(dx*dx + dz*dz) or 1
        ux = -dz / len_xz
        uz = dx / len_xz
        if key == glfw.KEY_W:
            CAM["eye_x"] += dx * STEP / 2
            CAM["eye_y"] += dy * STEP / 2
            CAM["eye_z"] += dz * STEP / 2
            CAM["center_x"] += dx * STEP / 2
            CAM["center_y"] += dy * STEP / 2
            CAM["center_z"] += dz * STEP / 2
        elif key == glfw.KEY_S:
            CAM["eye_x"] -= dx * STEP / 2
            CAM["eye_y"] -= dy * STEP / 2
            CAM["eye_z"] -= dz * STEP / 2
            CAM["center_x"] -= dx * STEP / 2
            CAM["center_y"] -= dy * STEP / 2
            CAM["center_z"] -= dz * STEP / 2
        elif key == glfw.KEY_A:
            CAM["eye_x"] += ux * STEP
            CAM["eye_z"] += uz * STEP
            CAM["center_x"] += ux * STEP
            CAM["center_z"] += uz * STEP
        elif key == glfw.KEY_D:
            CAM["eye_x"] -= ux * STEP
            CAM["eye_z"] -= uz * STEP
            CAM["center_x"] -= ux * STEP
            CAM["center_z"] -= uz * STEP
        elif key == glfw.KEY_Q:
            CAM["eye_y"] += STEP
            CAM["center_y"] += STEP
        elif key == glfw.KEY_E:
            CAM["eye_y"] -= STEP
            CAM["center_y"] -= STEP

    glfw.set_key_callback(win, on_key)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glViewport(0, 0, w, h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h else 1
        if PROJ["perspective"]:
            # Matriz genérica de projeção perspectiva (frustum)
            fov_y = 50
            near, far = 0.1, 100
            top = near * 0.5  # aproximação
            right = top * aspect
            glFrustum(-right, right, -top, top, near, far)
        else:
            # Projeção ortogonal
            dim = 4
            if aspect >= 1:
                glOrtho(-dim * aspect, dim * aspect, -dim, dim, 0.1, 100)
            else:
                glOrtho(-dim, dim, -dim / aspect, dim / aspect, 0.1, 100)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            CAM["eye_x"], CAM["eye_y"], CAM["eye_z"],
            CAM["center_x"], CAM["center_y"], CAM["center_z"],
            0, 1, 0,
        )
        draw_cube(0.5)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
    glfw.terminate()
