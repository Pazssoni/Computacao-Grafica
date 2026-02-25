"""Módulo 4 — Iluminação: cubo e pirâmide, projeção perspectiva. Space: Flat/Smooth (Gouraud)."""
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
    GL_QUADS, GL_TRIANGLES,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_FLAT, GL_SMOOTH,
    GL_PROJECTION, GL_MODELVIEW,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glEnable, glDisable, glShadeModel,
    glLightfv, glMaterialfv,
    glBegin, glEnd, glVertex3f, glNormal3f,
    glTranslatef, glRotatef, glPushMatrix, glPopMatrix,
)
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL import GL
from utils.hud import draw_text_2d
from utils.panel import draw_back_button, hit_test
from utils.shapes import draw_cube_edges, draw_pyramid_edges


def _draw_cube():
    """Cubo [-1,1] com normais por face."""
    glBegin(GL_QUADS)
    glNormal3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glNormal3f(0.0, 0.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glNormal3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glNormal3f(0.0, -1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glNormal3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(1.0, 1.0, -1.0)
    glVertex3f(1.0, 1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glNormal3f(-1.0, 0.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, -1.0)
    glEnd()


def _draw_pyramid():
    """Pirâmide com normais por face."""
    glBegin(GL_TRIANGLES)
    glNormal3f(0.0, 0.5, 0.5)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, 1.0)
    glNormal3f(0.5, 0.5, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, 1.0)
    glVertex3f(1.0, -1.0, -1.0)
    glNormal3f(-0.5, 0.5, 0.0)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, 1.0)
    glNormal3f(0.0, 0.5, -0.5)
    glVertex3f(0.0, 1.0, 0.0)
    glVertex3f(1.0, -1.0, -1.0)
    glVertex3f(-1.0, -1.0, -1.0)
    glEnd()


SHADING_MODES = [GL_FLAT, GL_SMOOTH]
STATE = {"shading_idx": 1}


def run():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(800, 600, "Iluminação | Space: Flat/Smooth | Voltar ao menu", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glClearColor(0.06, 0.07, 0.1, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.4, 0.4, 0.4, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.85, 0.85, 0.85, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))

    def on_key(window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_SPACE:
            STATE["shading_idx"] = (STATE["shading_idx"] + 1) % 2

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
        gluPerspective(45.0, aspect, 0.1, 50.0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 10.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

        glShadeModel(SHADING_MODES[STATE["shading_idx"]])
        t = glfw.get_time() * 0.05

        glPushMatrix()
        glTranslatef(-2.5, 0.0, 0.0)
        glRotatef(t * 360.0, 1.0, 1.0, 0.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.25, 0.5, 0.85, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (70.0,))
        _draw_cube()
        glDisable(GL_LIGHTING)
        draw_cube_edges(1.0)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(2.5, 0.0, 0.0)
        glRotatef(t * 360.0, 0.0, 1.0, 1.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.85, 0.45, 0.2, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SPECULAR, (0.6, 0.6, 0.6, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (80.0,))
        _draw_pyramid()
        glDisable(GL_LIGHTING)
        draw_pyramid_edges(1.0, 2.0)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        mode_name = "Smooth (Gouraud)" if STATE["shading_idx"] == 1 else "Flat"
        draw_text_2d(10, h - 20, "Space: Flat / Smooth | Cubo | Piramide", 0.9, 0.9, 0.95)
        draw_text_2d(10, 14, "Modo: " + mode_name, 0.75, 0.8, 0.85)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        back_rects = draw_back_button(w, h)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
