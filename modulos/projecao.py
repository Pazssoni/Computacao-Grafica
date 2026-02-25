"""Módulo 2 — Projeção perspectiva/ortogonal e câmera LookAt. Teclas P, WASD, Q/E."""
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_PROJECTION, GL_MODELVIEW,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glFrustum, glEnable,
    glLightfv, glMaterialfv,
)
from OpenGL.GLU import gluLookAt
from OpenGL import GL
from utils.shapes import draw_cube
from utils.panel import draw_back_button, hit_test
from math import sqrt

CAM = {"eye_x": 3, "eye_y": 2, "eye_z": 4, "center_x": 0, "center_y": 0, "center_z": 0}
PROJ = {"perspective": True}
STEP = 0.4


def _move_camera(direction):
    dx = CAM["center_x"] - CAM["eye_x"]
    dy = CAM["center_y"] - CAM["eye_y"]
    dz = CAM["center_z"] - CAM["eye_z"]
    len_xz = sqrt(dx*dx + dz*dz) or 1
    ux, uz = -dz / len_xz, dx / len_xz
    if direction == "proj":
        PROJ["perspective"] = not PROJ["perspective"]
    elif direction == "frente":
        CAM["eye_x"] += dx * STEP / 2
        CAM["eye_y"] += dy * STEP / 2
        CAM["eye_z"] += dz * STEP / 2
        CAM["center_x"] += dx * STEP / 2
        CAM["center_y"] += dy * STEP / 2
        CAM["center_z"] += dz * STEP / 2
    elif direction == "tras":
        CAM["eye_x"] -= dx * STEP / 2
        CAM["eye_y"] -= dy * STEP / 2
        CAM["eye_z"] -= dz * STEP / 2
        CAM["center_x"] -= dx * STEP / 2
        CAM["center_y"] -= dy * STEP / 2
        CAM["center_z"] -= dz * STEP / 2
    elif direction == "cima":
        CAM["eye_y"] += STEP
        CAM["center_y"] += STEP
    elif direction == "baixo":
        CAM["eye_y"] -= STEP
        CAM["center_y"] -= STEP
    elif direction == "esq":
        CAM["eye_x"] += ux * STEP
        CAM["eye_z"] += uz * STEP
        CAM["center_x"] += ux * STEP
        CAM["center_z"] += uz * STEP
    elif direction == "dir":
        CAM["eye_x"] -= ux * STEP
        CAM["eye_z"] -= uz * STEP
        CAM["center_x"] -= ux * STEP
        CAM["center_z"] -= uz * STEP


def run():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(800, 600, "Projeção | WASD+QE P | Voltar ao menu", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glClearColor(0.12, 0.12, 0.18, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.3, 0.3, 0.3, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.85, 0.85, 0.85, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))

    def on_key(window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_P:
            _move_camera("proj")
        elif key == glfw.KEY_W:
            _move_camera("frente")
        elif key == glfw.KEY_S:
            _move_camera("tras")
        elif key == glfw.KEY_A:
            _move_camera("esq")
        elif key == glfw.KEY_D:
            _move_camera("dir")
        elif key == glfw.KEY_Q:
            _move_camera("cima")
        elif key == glfw.KEY_E:
            _move_camera("baixo")

    back_rects = []

    def on_mouse(window, button, action, mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x, y = glfw.get_cursor_pos(window)
        fw, fh = glfw.get_framebuffer_size(window)
        if hit_test(x, y, fw, fh, back_rects) == "back":
            glfw.set_window_should_close(window, True)

    glfw.set_key_callback(win, on_key)
    glfw.set_mouse_button_callback(win, on_mouse)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glViewport(0, 0, w, h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h else 1
        if PROJ["perspective"]:
            near, far = 0.1, 100
            top = near * 0.5
            right = top * aspect
            glFrustum(-right, right, -top, top, near, far)
        else:
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
        glLightfv(GL_LIGHT0, GL_POSITION, (3, 3, 3, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.6, 0.65, 0.75, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.4, 0.4, 0.4, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (50.0,))
        draw_cube(0.5)

        back_rects = draw_back_button(w, h)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
