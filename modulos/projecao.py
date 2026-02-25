"""Módulo 2 — Projeção perspectiva/ortogonal e câmera LookAt. Teclas P, WASD, Q/E."""
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_PROJECTION, GL_MODELVIEW,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glEnable,
    glLightfv, glMaterialfv, glTranslatef, glPushMatrix, glPopMatrix,
)
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL import GL
from utils.shapes import draw_cube, draw_pyramid
from utils.hud import draw_text_2d
from utils.panel import draw_back_button, hit_test
from math import sqrt

CAM = {"eye_x": 4, "eye_y": 2.5, "eye_z": 5, "center_x": 0, "center_y": 0, "center_z": 0}
PROJ = {"perspective": True}
STEP = 0.5
MIN_DIST = 2.0
MAX_DIST = 25.0


def _dist_eye_center():
    dx = CAM["center_x"] - CAM["eye_x"]
    dy = CAM["center_y"] - CAM["eye_y"]
    dz = CAM["center_z"] - CAM["eye_z"]
    return sqrt(dx*dx + dy*dy + dz*dz)


def _move_camera(direction):
    dx = CAM["center_x"] - CAM["eye_x"]
    dy = CAM["center_y"] - CAM["eye_y"]
    dz = CAM["center_z"] - CAM["eye_z"]
    d = _dist_eye_center() or 1.0
    len_xz = sqrt(dx*dx + dz*dz) or 1.0
    ux, uz = -dz / len_xz, dx / len_xz

    if direction == "proj":
        PROJ["perspective"] = not PROJ["perspective"]
        return
    if direction == "frente":
        k = STEP * 0.6
        CAM["eye_x"] += dx * k / d
        CAM["eye_y"] += dy * k / d
        CAM["eye_z"] += dz * k / d
        CAM["center_x"] += dx * k / d
        CAM["center_y"] += dy * k / d
        CAM["center_z"] += dz * k / d
    elif direction == "tras":
        k = STEP * 0.6
        CAM["eye_x"] -= dx * k / d
        CAM["eye_y"] -= dy * k / d
        CAM["eye_z"] -= dz * k / d
        CAM["center_x"] -= dx * k / d
        CAM["center_y"] -= dy * k / d
        CAM["center_z"] -= dz * k / d
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

    dist = _dist_eye_center()
    if dist < MIN_DIST:
        f = MIN_DIST / dist
        CAM["eye_x"] = CAM["center_x"] + (CAM["eye_x"] - CAM["center_x"]) * f
        CAM["eye_y"] = CAM["center_y"] + (CAM["eye_y"] - CAM["center_y"]) * f
        CAM["eye_z"] = CAM["center_z"] + (CAM["eye_z"] - CAM["center_z"]) * f
    elif dist > MAX_DIST:
        f = MAX_DIST / dist
        CAM["eye_x"] = CAM["center_x"] + (CAM["eye_x"] - CAM["center_x"]) * f
        CAM["eye_y"] = CAM["center_y"] + (CAM["eye_y"] - CAM["center_y"]) * f
        CAM["eye_z"] = CAM["center_z"] + (CAM["eye_z"] - CAM["center_z"]) * f


def run():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(900, 600, "Projecao | P: tipo | WASD+QE: camera | Voltar ao menu", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glClearColor(0.1, 0.11, 0.16, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.35, 0.35, 0.35, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.9, 0.9, 0.9, 1.0))
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
            gluPerspective(45.0, aspect, 0.1, 100.0)
        else:
            dim = 5.0
            if aspect >= 1:
                glOrtho(-dim * aspect, dim * aspect, -dim, dim, 0.1, 100.0)
            else:
                glOrtho(-dim, dim, -dim / aspect, dim / aspect, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(
            CAM["eye_x"], CAM["eye_y"], CAM["eye_z"],
            CAM["center_x"], CAM["center_y"], CAM["center_z"],
            0, 1, 0,
        )
        glLightfv(GL_LIGHT0, GL_POSITION, (CAM["eye_x"] + 2, CAM["eye_y"] + 2, CAM["eye_z"] + 2, 1.0))

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.5, 0.6, 0.8, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.45, 0.45, 0.45, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (55.0,))
        draw_cube(0.5)

        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.85, 0.5, 0.25, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.4, 0.4, 0.4, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (40.0,))
        glPushMatrix()
        glTranslatef(1.8, 0.0, -0.8)
        draw_pyramid(0.4, 0.7)
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        modo = "Perspectiva" if PROJ["perspective"] else "Ortogonal"
        draw_text_2d(10, h - 20, "P: Perspectiva / Ortogonal | WASD: mover | Q/E: subir/descer", 0.9, 0.92, 0.96)
        draw_text_2d(10, 14, "Modo: " + modo + " | Cubo + Piramide", 0.75, 0.8, 0.88)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        back_rects = draw_back_button(w, h)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
