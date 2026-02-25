"""Módulo 1 — Transformações: translação, escala, rotação, reflexão, cisalhamento. Space T/E/R/F/C."""
import ctypes
import numpy as np
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LIGHTING,
    GL_PROJECTION, GL_MODELVIEW, GL_LINES,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glTranslatef, glScalef, glRotatef, glMultMatrixf,
    glPushMatrix, glPopMatrix, glColor3f, glEnable, glDisable,
    glBegin, glEnd, glVertex2f,
)
from utils.shapes import draw_cube, draw_cube_edges
from utils.hud import draw_text_2d
from utils.panel import draw_back_button, hit_test


def matrix_to_gl(m):
    return (ctypes.c_float * 16)(*m.T.astype(np.float32).flatten())


def shear_matrix(shx=0.3, shy=0.0, shz=0.0):
    """Matriz 4x4 de cisalhamento (aplicada com glMultMatrixf em column-major)."""
    return np.array([
        [1, shx, 0, 0],
        [shy, 1, 0, 0],
        [shz, 0, 1, 0],
        [0, 0, 0, 1],
    ], dtype=np.float32)


PARAMS = {
    "paused": False,
    "tx": 0.4,
    "ty": 0.2,
    "scale": 1.4,
    "rotation_speed": 1.0,
    "reflection_axis": 0,
    "shx": 0.4,
    "shy": 0.15,
}
LABELS = ["Translação", "Escala", "Rotação", "Reflexão", "Cisalhamento"]


def run():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(1000, 600, "Transformações | Space T/E/R/F/C | Voltar ao menu", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glClearColor(0.12, 0.14, 0.18, 1.0)
    glEnable(GL_DEPTH_TEST)

    angle = 0.0

    def on_key(window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_SPACE:
            PARAMS["paused"] = not PARAMS["paused"]
        elif key == glfw.KEY_T:
            PARAMS["tx"] = min(1.2, PARAMS["tx"] + 0.1)
            PARAMS["ty"] = min(1.0, PARAMS["ty"] + 0.05)
        elif key == glfw.KEY_Y:
            PARAMS["tx"] = max(-0.5, PARAMS["tx"] - 0.1)
            PARAMS["ty"] = max(-0.5, PARAMS["ty"] - 0.05)
        elif key == glfw.KEY_E:
            PARAMS["scale"] = min(2.5, PARAMS["scale"] + 0.1)
        elif key == glfw.KEY_D:
            PARAMS["scale"] = max(0.4, PARAMS["scale"] - 0.1)
        elif key == glfw.KEY_R:
            PARAMS["rotation_speed"] = min(3.0, PARAMS["rotation_speed"] + 0.2)
        elif key == glfw.KEY_V:
            PARAMS["rotation_speed"] = max(0.1, PARAMS["rotation_speed"] - 0.2)
        elif key == glfw.KEY_F:
            PARAMS["reflection_axis"] = (PARAMS["reflection_axis"] + 1) % 3
        elif key == glfw.KEY_C:
            PARAMS["shx"] = min(1.2, PARAMS["shx"] + 0.1)
            PARAMS["shy"] = min(0.8, PARAMS["shy"] + 0.05)
        elif key == glfw.KEY_X:
            PARAMS["shx"] = max(-0.5, PARAMS["shx"] - 0.1)
            PARAMS["shy"] = max(-0.3, PARAMS["shy"] - 0.05)

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
        glDisable(GL_LIGHTING)

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
            glTranslatef(0, 0, -3)
            glRotatef(20, 1, 0, 0)
            if not PARAMS["paused"]:
                angle += 0.6 * (0.5 if col != 2 else PARAMS["rotation_speed"] * 0.5)
            glRotatef(angle * 0.5, 0, 1, 0)

            glPushMatrix()
            if col == 0:
                glTranslatef(PARAMS["tx"], PARAMS["ty"], 0)
                glColor3f(0.95, 0.45, 0.45)
            elif col == 1:
                glScalef(PARAMS["scale"], PARAMS["scale"], PARAMS["scale"])
                glColor3f(0.4, 0.88, 0.5)
            elif col == 2:
                glRotatef(angle, 0, 1, 0)
                glColor3f(0.45, 0.5, 0.95)
            elif col == 3:
                ax = PARAMS["reflection_axis"]
                if ax == 0:
                    glScalef(-1, 1, 1)
                elif ax == 1:
                    glScalef(1, -1, 1)
                else:
                    glScalef(1, 1, -1)
                glColor3f(0.95, 0.9, 0.45)
            else:
                glMultMatrixf(matrix_to_gl(shear_matrix(PARAMS["shx"], PARAMS["shy"], 0)))
                glColor3f(0.9, 0.55, 0.9)
            draw_cube(0.35)
            draw_cube_edges(0.35)
            glPopMatrix()

        glViewport(0, 0, w, h)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glColor3f(0.35, 0.4, 0.45)
        glBegin(GL_LINES)
        for i in range(1, 5):
            vx = int(i * col_width)
            glVertex2f(vx, 0)
            glVertex2f(vx, h)
        glEnd()
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        for i in range(5):
            cx = int(i * col_width + col_width * 0.5) - 40
            draw_text_2d(cx, h - 20, LABELS[i], 0.9, 0.92, 0.95)
        ref_names = ["X", "Y", "Z"]
        draw_text_2d(10, 14, f"Reflexao: {ref_names[PARAMS['reflection_axis']]} | Cisalh: {PARAMS['shx']:.2f}", 0.75, 0.8, 0.85)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        back_rects = draw_back_button(w, h)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
