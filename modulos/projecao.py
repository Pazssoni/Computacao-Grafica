"""Modulo 2 - Projecao com visual padronizado ao modulo de transformacoes."""
from math import sqrt
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_PROJECTION, GL_MODELVIEW, GL_QUADS, GL_LINES,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glDisable, glEnable,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho,
    glLightfv, glMaterialfv, glTranslatef, glPushMatrix, glPopMatrix,
    glBegin, glEnd, glVertex2f, glColor3f,
)
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL import GL
from utils.shapes import draw_cube, draw_pyramid, draw_cube_edges, draw_pyramid_edges
from utils.hud import draw_text_2d, text_width
from utils.panel import draw_back_button, hit_test, BACK_MARGIN, BACK_BUTTON_W


DEFAULT_CAM = {"eye_x": 4, "eye_y": 2.5, "eye_z": 5, "center_x": 0, "center_y": 0, "center_z": 0}
DEFAULT_PROJ = {"perspective": True}
DEFAULT_ORTHO = {"dim": 5.0}
CAM = dict(DEFAULT_CAM)
PROJ = dict(DEFAULT_PROJ)
ORTHO = dict(DEFAULT_ORTHO)
STEP = 0.5
MIN_DIST = 2.0
MAX_DIST = 25.0
OPTIONS = [("persp", "PERSPECTIVA"), ("ortho", "ORTOGONAL")]


def _draw_quad(x1, y1, x2, y2):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def _dist_eye_center():
    dx = CAM["center_x"] - CAM["eye_x"]
    dy = CAM["center_y"] - CAM["eye_y"]
    dz = CAM["center_z"] - CAM["eye_z"]
    return sqrt(dx * dx + dy * dy + dz * dz)


def _move_camera(direction):
    dx = CAM["center_x"] - CAM["eye_x"]
    dy = CAM["center_y"] - CAM["eye_y"]
    dz = CAM["center_z"] - CAM["eye_z"]
    d = _dist_eye_center() or 1.0
    len_xz = sqrt(dx * dx + dz * dz) or 1.0
    ux, uz = -dz / len_xz, dx / len_xz

    if direction == "proj":
        PROJ["perspective"] = not PROJ["perspective"]
        return
    if direction == "persp":
        PROJ["perspective"] = True
        return
    if direction == "ortho":
        PROJ["perspective"] = False
        return
    if direction == "frente":
        if not PROJ["perspective"]:
            ORTHO["dim"] = max(1.2, ORTHO["dim"] - 0.25)
            return
        k = STEP * 0.6
        CAM["eye_x"] += dx * k / d
        CAM["eye_y"] += dy * k / d
        CAM["eye_z"] += dz * k / d
        CAM["center_x"] += dx * k / d
        CAM["center_y"] += dy * k / d
        CAM["center_z"] += dz * k / d
    elif direction == "tras":
        if not PROJ["perspective"]:
            ORTHO["dim"] = min(16.0, ORTHO["dim"] + 0.25)
            return
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
    if dist <= 1e-6:
        CAM["eye_x"] = CAM["center_x"]
        CAM["eye_y"] = CAM["center_y"]
        CAM["eye_z"] = CAM["center_z"] + MIN_DIST
        return
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


def _draw_mode_tabs(w, h, hover_mode=None):
    tabs = _mode_tab_rects(w, h)
    active_mode = "persp" if PROJ["perspective"] else "ortho"
    for idx, (rid, x1, y1, x2, y2) in enumerate(tabs):
        mid = OPTIONS[idx][0]
        label = OPTIONS[idx][1]
        tab_w = x2 - x1
        tab_h = y2 - y1
        is_active = mid == active_mode
        is_hover = mid == hover_mode
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
        tx = x1 + (tab_w - tw) / 2
        ty = y1 + (tab_h / 2) + 5
        draw_text_2d(tx, ty, label, 1.0, 1.0, 1.0)
    return tabs


def _mode_tab_rects(w, h):
    tabs = []
    tab_w = 260
    tab_h = 44
    gap = 16
    total = len(OPTIONS) * tab_w + (len(OPTIONS) - 1) * gap
    x = (w - total) / 2
    y1 = h - 106
    y2 = y1 + tab_h
    for idx, (mid, _label) in enumerate(OPTIONS):
        x1 = x + idx * (tab_w + gap)
        x2 = x1 + tab_w
        tabs.append((f"proj_{mid}", x1, y1, x2, y2))
    return tabs


def _draw_hud(w, h):
    mode_name = "PERSPECTIVA" if PROJ["perspective"] else "ORTOGONAL"
    hud_x = BACK_MARGIN + BACK_BUTTON_W + 16
    hud_y = BACK_MARGIN + 26
    draw_text_2d(18, h - 20, "PROJECAO - selecione modo por clique ou tecla P", 0.90, 0.92, 0.96)
    draw_text_2d(18, h - 124, f"ATIVA: {mode_name}", 0.82, 0.86, 0.92)
    draw_text_2d(hud_x, hud_y + 34, "SETAS: navegar (cima/baixo/esquerda/direita)", 0.82, 0.86, 0.92)
    draw_text_2d(hud_x, hud_y + 16, "PAGEUP/PAGEDOWN: subir/descer  |  P: alternar perspectiva/ortogonal", 0.76, 0.81, 0.89)
    if not PROJ["perspective"]:
        draw_text_2d(hud_x, hud_y - 2, f"ZOOM ORTHO: {ORTHO['dim']:.2f}", 0.72, 0.78, 0.86)
        return
    draw_text_2d(
        hud_x,
        hud_y - 2,
        f"CAM EYE ({CAM['eye_x']:.1f}, {CAM['eye_y']:.1f}, {CAM['eye_z']:.1f})",
        0.72,
        0.78,
        0.86,
    )


def _draw_scene(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = w / h if h else 1
    if PROJ["perspective"]:
        gluPerspective(45.0, aspect, 0.1, 100.0)
    else:
        dim = ORTHO["dim"]
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

    glPushMatrix()
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.18, 0.20, 0.25, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.14, 0.14, 0.18, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (22.0,))
    draw_cube(0.5)
    glDisable(GL_LIGHTING)
    glColor3f(0.36, 0.40, 0.48)
    draw_cube_edges(0.5)
    glEnable(GL_LIGHTING)
    glPopMatrix()

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.38, 0.63, 0.92, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.42, 0.42, 0.42, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (62.0,))
    glPushMatrix()
    glTranslatef(1.8, 0.0, -0.8)
    draw_pyramid(0.55, 1.0)
    glDisable(GL_LIGHTING)
    draw_pyramid_edges(0.55, 1.0)
    glEnable(GL_LIGHTING)
    glPopMatrix()


def run():
    CAM.update(DEFAULT_CAM)
    PROJ.update(DEFAULT_PROJ)
    ORTHO.update(DEFAULT_ORTHO)

    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(1180, 650, "Projecao | Visual padronizado | Voltar ao menu", None, None)
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
        if action not in (glfw.PRESS, glfw.REPEAT):
            return
        if key == glfw.KEY_P:
            _move_camera("proj")
        elif key == glfw.KEY_UP:
            _move_camera("frente")
        elif key == glfw.KEY_DOWN:
            _move_camera("tras")
        elif key == glfw.KEY_LEFT:
            _move_camera("esq")
        elif key == glfw.KEY_RIGHT:
            _move_camera("dir")
        elif key == glfw.KEY_PAGE_UP:
            _move_camera("cima")
        elif key == glfw.KEY_PAGE_DOWN:
            _move_camera("baixo")

    def on_mouse(window, button, action, mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x, y = glfw.get_cursor_pos(window)
        fw, fh = glfw.get_framebuffer_size(window)
        clicked = hit_test(x, y, fw, fh, tab_rects + back_rects)
        if clicked == "back":
            glfw.set_window_should_close(window, True)
            return
        if clicked == "proj_persp":
            _move_camera("persp")
        elif clicked == "proj_ortho":
            _move_camera("ortho")

    glfw.set_key_callback(win, on_key)
    glfw.set_mouse_button_callback(win, on_mouse)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        _draw_scene(w, h)

        mx, my = glfw.get_cursor_pos(win)
        hover_bid = hit_test(mx, my, w, h, _mode_tab_rects(w, h))
        hover_mode = None
        if hover_bid == "proj_persp":
            hover_mode = "persp"
        elif hover_bid == "proj_ortho":
            hover_mode = "ortho"

        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        tab_rects = _draw_mode_tabs(w, h, hover_mode=hover_mode)
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
