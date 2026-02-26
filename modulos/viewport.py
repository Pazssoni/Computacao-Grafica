"""Modulo 3 - Viewport com visual padronizado aos modulos corrigidos."""
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE, GL_SMOOTH,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_PROJECTION, GL_MODELVIEW, GL_QUADS, GL_LINES,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glColor3f,
    glEnable, glDisable, glPushMatrix, glPopMatrix,
    glLightfv, glMaterialfv, glShadeModel, glRotatef,
    glBegin, glEnd, glVertex2f,
)
from OpenGL.GLU import gluLookAt
from OpenGL import GL
from utils.shapes import draw_cube_smooth, draw_pyramid, draw_cube_edges, draw_pyramid_edges
from utils.axes import draw_axes
from utils.hud import draw_text_2d, draw_viewport_border, text_width
from utils.panel import draw_back_button, hit_test, BACK_MARGIN, BACK_BUTTON_W


DEFAULT_STATE = {"dim": 1.6, "object_index": 1, "show_axes": True}
STATE = dict(DEFAULT_STATE)
DIM_MIN, DIM_MAX = 0.6, 3.0
DIST = 5.0
OBJECTS = [
    ("CUBO", lambda: draw_cube_smooth(0.5)),
    ("PIRAMIDE", lambda: draw_pyramid(0.5, 0.8)),
]
VIEW_LABELS = ["FRENTE", "LADO", "TOPO"]


def _draw_quad(x1, y1, x2, y2):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def _cameras(dist):
    return [
        {"eye": (0, 0, dist), "center": (0, 0, 0), "up": (0, 1, 0)},
        {"eye": (dist, 0, 0), "center": (0, 0, 0), "up": (0, 1, 0)},
        {"eye": (0, dist, 0), "center": (0, 0, 0), "up": (0, 0, -1)},
    ]


def _tab_rects(w, h):
    tabs = []
    tab_w = 230
    tab_h = 44
    gap = 14
    total = 3 * tab_w + 2 * gap
    x = (w - total) / 2
    y1 = h - 106
    y2 = y1 + tab_h
    tabs.append(("obj_0", x, y1, x + tab_w, y2))
    x2 = x + tab_w + gap
    tabs.append(("obj_1", x2, y1, x2 + tab_w, y2))
    x3 = x2 + tab_w + gap
    tabs.append(("axes", x3, y1, x3 + tab_w, y2))
    return tabs


def _draw_tabs(w, h, hover_id=None):
    tabs = _tab_rects(w, h)
    for tid, x1, y1, x2, y2 in tabs:
        label = ""
        active = False
        if tid == "obj_0":
            label = "OBJETO: CUBO"
            active = STATE["object_index"] == 0
        elif tid == "obj_1":
            label = "OBJETO: PIRAMIDE"
            active = STATE["object_index"] == 1
        elif tid == "axes":
            label = "EIXOS: ON" if STATE["show_axes"] else "EIXOS: OFF"
            active = STATE["show_axes"]

        is_hover = tid == hover_id
        if active:
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
    obj_name = OBJECTS[STATE["object_index"]][0]
    hud_x = BACK_MARGIN + BACK_BUTTON_W + 16
    hud_y = BACK_MARGIN + 26
    draw_text_2d(18, h - 20, "VIEWPORT - altere objeto, eixos e zoom", 0.90, 0.92, 0.96)
    draw_text_2d(18, h - 124, f"ATIVA: {obj_name} | EIXOS {'ON' if STATE['show_axes'] else 'OFF'}", 0.82, 0.86, 0.92)
    draw_text_2d(hud_x, hud_y + 34, "Z: zoom in  SHIFT+Z: zoom out", 0.82, 0.86, 0.92)
    draw_text_2d(hud_x, hud_y + 16, "O: alternar objeto  A: alternar eixos", 0.76, 0.81, 0.89)
    draw_text_2d(hud_x, hud_y - 2, f"ZOOM: {STATE['dim']:.2f}", 0.72, 0.78, 0.86)


def _draw_scene(w, h):
    glViewport(0, 0, w, h)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    third = w // 3
    dim = STATE["dim"]
    cameras = _cameras(DIST)
    draw_obj = OBJECTS[STATE["object_index"]][1]
    light_pos = (3.0, 3.0, 3.0, 1.0)

    for i in range(3):
        x = i * third
        glViewport(x, 0, third, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = third / h if h else 1
        if aspect >= 1:
            glOrtho(-dim * aspect, dim * aspect, -dim, dim, -12, 12)
        else:
            glOrtho(-dim, dim, -dim / aspect, dim / aspect, -12, 12)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        cam = cameras[i]
        gluLookAt(
            cam["eye"][0], cam["eye"][1], cam["eye"][2],
            cam["center"][0], cam["center"][1], cam["center"][2],
            cam["up"][0], cam["up"][1], cam["up"][2],
        )
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.65, 0.7, 0.75, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.3, 0.3, 0.3, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (40.0,))
        glShadeModel(GL_SMOOTH)
        glPushMatrix()
        glRotatef(18, 0, 1, 0)
        glRotatef(8, 1, 0, 0)
        draw_obj()
        glDisable(GL_LIGHTING)
        if STATE["object_index"] == 0:
            draw_cube_edges(0.5)
        else:
            draw_pyramid_edges(0.5, 0.8)
        glEnable(GL_LIGHTING)
        glPopMatrix()
        if STATE["show_axes"]:
            draw_axes(0.8, 2.0)

    glViewport(0, 0, w, h)
    for i in range(3):
        vx = i * third
        draw_viewport_border(w, h, vx, 0, third, h)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, w, 0, h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    for i in range(3):
        cx = i * third + (third / 2) - (text_width(VIEW_LABELS[i], 2) / 2)
        draw_text_2d(cx, h - 170, VIEW_LABELS[i], 0.95, 0.95, 0.90)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def run():
    STATE.update(DEFAULT_STATE)

    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(1180, 650, "ViewPort | Visual padronizado | Voltar ao menu", None, None)
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

    tab_rects = []
    back_rects = []

    def on_key(window, key, scancode, action, mods):
        if action != glfw.PRESS:
            return
        if key == glfw.KEY_Z:
            if mods & glfw.MOD_SHIFT:
                STATE["dim"] = min(DIM_MAX, STATE["dim"] + 0.25)
            else:
                STATE["dim"] = max(DIM_MIN, STATE["dim"] - 0.25)
        elif key == glfw.KEY_O:
            STATE["object_index"] = (STATE["object_index"] + 1) % len(OBJECTS)
        elif key == glfw.KEY_A:
            STATE["show_axes"] = not STATE["show_axes"]

    def on_mouse(window, button, action, mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x, y = glfw.get_cursor_pos(window)
        fw, fh = glfw.get_framebuffer_size(window)
        clicked = hit_test(x, y, fw, fh, tab_rects + back_rects)
        if clicked == "back":
            glfw.set_window_should_close(window, True)
            return
        if clicked == "obj_0":
            STATE["object_index"] = 0
        elif clicked == "obj_1":
            STATE["object_index"] = 1
        elif clicked == "axes":
            STATE["show_axes"] = not STATE["show_axes"]

    glfw.set_key_callback(win, on_key)
    glfw.set_mouse_button_callback(win, on_mouse)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        _draw_scene(w, h)

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
