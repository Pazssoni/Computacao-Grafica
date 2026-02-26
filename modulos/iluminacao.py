"""Modulo 4 - Iluminacao com visual padronizado aos demais modulos."""
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
    GL_QUADS, GL_TRIANGLES, GL_LINES,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_FLAT, GL_SMOOTH,
    GL_PROJECTION, GL_MODELVIEW,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glEnable, glDisable, glShadeModel,
    glLightfv, glMaterialfv, glColor3f,
    glBegin, glEnd, glVertex2f, glVertex3f, glNormal3f,
    glTranslatef, glRotatef, glPushMatrix, glPopMatrix,
)
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL import GL
from utils.hud import draw_text_2d, text_width
from utils.panel import draw_back_button, hit_test, BACK_MARGIN, BACK_BUTTON_W
from utils.shapes import (
    draw_cube_edges, draw_pyramid_edges,
    draw_cube_smooth, draw_pyramid_smooth,
)


def _draw_cube_flat():
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


def _draw_pyramid_flat():
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


SHADING_MODES = [("flat", GL_FLAT, "FLAT"), ("smooth", GL_SMOOTH, "SMOOTH")]
DEFAULT_STATE = {"shading_idx": 1}
STATE = dict(DEFAULT_STATE)


def _draw_quad(x1, y1, x2, y2):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def _tab_rects(w, h):
    tabs = []
    tab_w = 260
    tab_h = 44
    gap = 16
    total = len(SHADING_MODES) * tab_w + (len(SHADING_MODES) - 1) * gap
    x = (w - total) / 2
    y1 = h - 106
    y2 = y1 + tab_h
    for i, (mid, _gl, _label) in enumerate(SHADING_MODES):
        x1 = x + i * (tab_w + gap)
        x2 = x1 + tab_w
        tabs.append((f"shade_{mid}", x1, y1, x2, y2))
    return tabs


def _draw_tabs(w, h, hover_id=None):
    tabs = _tab_rects(w, h)
    active_id = SHADING_MODES[STATE["shading_idx"]][0]
    for i, (tid, x1, y1, x2, y2) in enumerate(tabs):
        mode_id, _gl_mode, label = SHADING_MODES[i]
        is_active = mode_id == active_id
        is_hover = tid == hover_id
        if is_active:
            glColor3f(0.30, 0.42, 0.64)
            border_color = (0.74, 0.84, 0.98)
        elif is_hover:
            glColor3f(0.24, 0.32, 0.47)
            border_color = (0.62, 0.70, 0.84)
        else:
            glColor3f(0.18, 0.22, 0.30)
            border_color = (0.42, 0.48, 0.58)
        _draw_quad(x1, y1, x2, y2)
        glColor3f(*border_color)
        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y1)
        glVertex2f(x2, y2)
        glVertex2f(x2, y2)
        glVertex2f(x1, y2)
        glVertex2f(x1, y2)
        glVertex2f(x1, y1)
        glEnd()
        tw = text_width(label, 2)
        tx = x1 + ((x2 - x1) - tw) / 2
        ty = y1 + ((y2 - y1) / 2) + 5
        draw_text_2d(tx, ty, label, 1.0, 1.0, 1.0)
    return tabs


def _draw_hud(w, h):
    smooth_mode = STATE["shading_idx"] == 1
    mode_name = "SMOOTH (GOURAUD)" if smooth_mode else "FLAT"
    mode_color = (0.50, 0.92, 0.68) if smooth_mode else (0.96, 0.76, 0.38)
    hud_x = BACK_MARGIN + BACK_BUTTON_W + 16
    hud_y = BACK_MARGIN + 26
    draw_text_2d(18, h - 20, "ILUMINACAO - alterne entre FLAT e SMOOTH", 0.90, 0.92, 0.96)
    draw_text_2d(18, h - 124, f"ATIVA: {mode_name}", mode_color[0], mode_color[1], mode_color[2])
    draw_text_2d(hud_x, hud_y + 34, "SPACE: alternar modo", 0.82, 0.86, 0.92)
    draw_text_2d(hud_x, hud_y + 16, "Clique nas abas superiores para trocar", 0.76, 0.81, 0.89)
    draw_text_2d(hud_x, hud_y - 2, "Objetos: cubo e piramide", 0.72, 0.78, 0.86)


def run():
    STATE.update(DEFAULT_STATE)

    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(1180, 650, "Iluminacao | Visual padronizado | Voltar ao menu", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glClearColor(0.08, 0.10, 0.14, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.30, 0.30, 0.34, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.88, 0.88, 0.90, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.58, 0.58, 0.60, 1.0))
    glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))

    tab_rects = []
    back_rects = []

    def on_key(window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_SPACE:
            STATE["shading_idx"] = (STATE["shading_idx"] + 1) % len(SHADING_MODES)

    def on_mouse(window, button, action, mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x, y = glfw.get_cursor_pos(window)
        fw, fh = glfw.get_framebuffer_size(window)
        clicked = hit_test(x, y, fw, fh, tab_rects + back_rects)
        if clicked == "back":
            glfw.set_window_should_close(window, True)
            return
        if clicked == "shade_flat":
            STATE["shading_idx"] = 0
        elif clicked == "shade_smooth":
            STATE["shading_idx"] = 1

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

        _mode_id, gl_mode, _label = SHADING_MODES[STATE["shading_idx"]]
        glShadeModel(gl_mode)
        t = glfw.get_time() * 0.05
        smooth_mode = STATE["shading_idx"] == 1

        glPushMatrix()
        glTranslatef(-2.5, 0.0, 0.0)
        glRotatef(t * 360.0, 1.0, 1.0, 0.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.25, 0.5, 0.85, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (70.0,))
        if smooth_mode:
            draw_cube_smooth(1.0)
        else:
            _draw_cube_flat()
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
        if smooth_mode:
            draw_pyramid_smooth(1.0, 2.0)
        else:
            _draw_pyramid_flat()
        glDisable(GL_LIGHTING)
        draw_pyramid_edges(1.0, 2.0)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        mx, my = glfw.get_cursor_pos(win)
        hover_id = hit_test(mx, my, w, h, _tab_rects(w, h))

        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        tab_rects = _draw_tabs(w, h, hover_id=hover_id)
        _draw_hud(w, h)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

        back_rects = draw_back_button(w, h)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
