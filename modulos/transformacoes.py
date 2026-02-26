"""Modulo 1 - Transformacoes com selecao por opcoes (1-5)."""
import ctypes
import numpy as np
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE,
    GL_PROJECTION, GL_MODELVIEW, GL_LINES, GL_QUADS,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho, glTranslatef, glScalef, glRotatef, glMultMatrixf,
    glPushMatrix, glPopMatrix, glColor3f, glEnable, glDisable,
    glBegin, glEnd, glVertex2f, glLightfv, glMaterialfv,
)
from OpenGL import GL
from utils.shapes import draw_cube, draw_cube_edges
from utils.hud import draw_text_2d, text_width
from utils.panel import draw_back_button, hit_test, BACK_MARGIN, BACK_BUTTON_W


def matrix_to_gl(m):
    return (ctypes.c_float * 16)(*m.T.astype(np.float32).flatten())


def shear_matrix(shx=0.3, shy=0.0, shz=0.0):
    return np.array(
        [
            [1, shx, 0, 0],
            [shy, 1, 0, 0],
            [shz, 0, 1, 0],
            [0, 0, 0, 1],
        ],
        dtype=np.float32,
    )


def _clamp(v, lo, hi):
    return max(lo, min(hi, v))


OPTIONS = [
    "1 - Translacao",
    "2 - Escala",
    "3 - Rotacao",
    "4 - Reflexao",
    "5 - Cisalhamento",
]

DEFAULT_STATE = {
    "option": 0,
    "show_ref": True,
    "tx": 0.45,
    "ty": 0.18,
    "scale": 1.25,
    "rot_angle": 42.0,
    "reflection_axis": 0,
    "shx": 0.35,
    "shy": 0.12,
}
STATE = dict(DEFAULT_STATE)


def _reset_state():
    STATE.update(DEFAULT_STATE)


def _draw_quad(x1, y1, x2, y2):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def _draw_mode_tabs(w, h):
    tabs = []
    tab_w = 200
    tab_h = 44
    gap = 12
    total = len(OPTIONS) * tab_w + (len(OPTIONS) - 1) * gap
    x = (w - total) / 2
    y1 = h - 106
    y2 = y1 + tab_h
    for i, label in enumerate(OPTIONS):
        x1 = x + i * (tab_w + gap)
        x2 = x1 + tab_w
        active = i == STATE["option"]
        if active:
            glColor3f(0.30, 0.42, 0.64)
        else:
            glColor3f(0.18, 0.22, 0.30)
        _draw_quad(x1, y1, x2, y2)
        glColor3f(0.45, 0.5, 0.58)
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
        tabs.append((f"opt_{i}", x1, y1, x2, y2))
    return tabs


def _draw_hud_text(w, h):
    axis_names = ["X", "Y", "Z"]
    active_name = OPTIONS[STATE["option"]].split(" - ", 1)[1]
    info = ""
    keys = ""

    if STATE["option"] == 0:
        info = f"Translacao ativa | X={STATE['tx']:.2f} Y={STATE['ty']:.2f}"
        keys = "Setas: mover objeto no plano XY"
    elif STATE["option"] == 1:
        info = f"Escala ativa | Escala={STATE['scale']:.2f}"
        keys = "Seta Cima/Baixo: aumentar/diminuir escala"
    elif STATE["option"] == 2:
        info = f"Rotacao ativa | Angulo={STATE['rot_angle']:.1f} graus"
        keys = "Seta Esquerda/Direita: rotacionar no eixo Y"
    elif STATE["option"] == 3:
        info = f"Reflexao ativa | Eixo atual={axis_names[STATE['reflection_axis']]}"
        keys = "Teclas X, Y, Z: escolher eixo da reflexao"
    elif STATE["option"] == 4:
        info = f"Cisalhamento ativo | SHX={STATE['shx']:.2f} SHY={STATE['shy']:.2f}"
        keys = "Setas: ajustar SHX/SHY (esq-dir / baixo-cima)"

    ref_text = "ON" if STATE["show_ref"] else "OFF"
    hud_x = BACK_MARGIN + BACK_BUTTON_W + 16
    hud_y = BACK_MARGIN + 26
    draw_text_2d(18, h - 20, "TRANSFORMACOES GEOMETRICAS - selecione opcao por clique ou teclas 1..5", 0.90, 0.92, 0.96)
    draw_text_2d(18, h - 124, f"ATIVA: {active_name} | ESQUERDA: REFERENCIA | DIREITA: TRANSFORMADO", 0.82, 0.86, 0.92)
    draw_text_2d(hud_x, hud_y + 34, info, 0.82, 0.86, 0.92)
    draw_text_2d(hud_x, hud_y + 16, keys, 0.76, 0.81, 0.89)
    draw_text_2d(hud_x, hud_y - 2, f"TAB: mostrar referencia ({ref_text}) | BACKSPACE: resetar tudo", 0.72, 0.78, 0.86)


def _draw_scene(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-3.4, 3.4, -1.8, 1.8, -12, 12)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glTranslatef(0.0, -0.05, -5.2)
    glRotatef(20.0, 1, 0, 0)
    glRotatef(-28.0, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (3.2, 3.3, 3.0, 1.0))

    # Eixos de referencia
    glDisable(GL_LIGHTING)
    glBegin(GL_LINES)
    glColor3f(0.75, 0.28, 0.28)
    glVertex2f(-3.0, 0.0)
    glVertex2f(3.0, 0.0)
    glColor3f(0.28, 0.75, 0.28)
    glVertex2f(0.0, -1.5)
    glVertex2f(0.0, 1.5)
    glEnd()
    glEnable(GL_LIGHTING)

    def draw_asymmetric_object():
        glPushMatrix()
        draw_cube(0.46)
        glDisable(GL_LIGHTING)
        draw_cube_edges(0.46)
        glEnable(GL_LIGHTING)
        glPopMatrix()

        glPushMatrix()
        # Bloco deslocado para quebrar a simetria e evidenciar espelhamento
        glTranslatef(0.62, 0.34, 0.22)
        glScalef(0.48, 0.48, 0.48)
        draw_cube(0.46)
        glDisable(GL_LIGHTING)
        draw_cube_edges(0.46)
        glEnable(GL_LIGHTING)
        glPopMatrix()

    # Objeto de referencia (esquerda)
    if STATE["show_ref"]:
        glPushMatrix()
        glTranslatef(-1.8, 0.0, 0.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.18, 0.2, 0.25, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.15, 0.15, 0.2, 1.0))
        glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (20.0,))
        if STATE["option"] == 3:
            draw_asymmetric_object()
        else:
            draw_cube(0.5)
            glDisable(GL_LIGHTING)
            glColor3f(0.36, 0.4, 0.48)
            draw_cube_edges(0.5)
            glEnable(GL_LIGHTING)
        glPopMatrix()

    # Objeto transformado (direita)
    glPushMatrix()
    glTranslatef(1.2, 0.0, 0.0)

    if STATE["option"] == 0:
        glTranslatef(STATE["tx"], STATE["ty"], 0.0)
    elif STATE["option"] == 1:
        glScalef(STATE["scale"], STATE["scale"], STATE["scale"])
    elif STATE["option"] == 2:
        glRotatef(STATE["rot_angle"], 0, 1, 0)
    elif STATE["option"] == 3:
        axis = STATE["reflection_axis"]
        if axis == 0:
            glScalef(-1, 1, 1)
        elif axis == 1:
            glScalef(1, -1, 1)
        else:
            glScalef(1, 1, -1)
    elif STATE["option"] == 4:
        glMultMatrixf(matrix_to_gl(shear_matrix(STATE["shx"], STATE["shy"], 0.0)))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, (0.38, 0.63, 0.92, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (0.42, 0.42, 0.42, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL.GL_SHININESS, (70.0,))
    if STATE["option"] == 3:
        draw_asymmetric_object()
    else:
        draw_cube(0.5)
        glDisable(GL_LIGHTING)
        draw_cube_edges(0.5)
        glEnable(GL_LIGHTING)
    glPopMatrix()


def run():
    _reset_state()

    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(1180, 650, "Transformacoes | Opcoes 1-5 | Voltar ao menu", None, None)
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

    clickable_rects = []
    back_rects = []

    def on_key(window, key, scancode, action, mods):
        if action not in (glfw.PRESS, glfw.REPEAT):
            return

        if key == glfw.KEY_1:
            STATE["option"] = 0
            return
        if key == glfw.KEY_2:
            STATE["option"] = 1
            return
        if key == glfw.KEY_3:
            STATE["option"] = 2
            return
        if key == glfw.KEY_4:
            STATE["option"] = 3
            return
        if key == glfw.KEY_5:
            STATE["option"] = 4
            return
        if key == glfw.KEY_TAB and action == glfw.PRESS:
            STATE["show_ref"] = not STATE["show_ref"]
            return
        if key == glfw.KEY_BACKSPACE and action == glfw.PRESS:
            _reset_state()
            return

        step_move = 0.08
        step_scale = 0.06
        step_rot = 3.0
        step_shear_x = 0.06
        step_shear_y = 0.04

        if STATE["option"] == 0:
            if key == glfw.KEY_UP:
                STATE["ty"] = _clamp(STATE["ty"] + step_move, -1.2, 1.2)
            elif key == glfw.KEY_DOWN:
                STATE["ty"] = _clamp(STATE["ty"] - step_move, -1.2, 1.2)
            elif key == glfw.KEY_LEFT:
                STATE["tx"] = _clamp(STATE["tx"] - step_move, -1.5, 1.5)
            elif key == glfw.KEY_RIGHT:
                STATE["tx"] = _clamp(STATE["tx"] + step_move, -1.5, 1.5)
        elif STATE["option"] == 1:
            if key == glfw.KEY_UP:
                STATE["scale"] = _clamp(STATE["scale"] + step_scale, 0.35, 2.8)
            elif key == glfw.KEY_DOWN:
                STATE["scale"] = _clamp(STATE["scale"] - step_scale, 0.35, 2.8)
        elif STATE["option"] == 2:
            if key == glfw.KEY_RIGHT:
                STATE["rot_angle"] = _clamp(STATE["rot_angle"] + step_rot, -180.0, 180.0)
            elif key == glfw.KEY_LEFT:
                STATE["rot_angle"] = _clamp(STATE["rot_angle"] - step_rot, -180.0, 180.0)
        elif STATE["option"] == 3:
            if key == glfw.KEY_X and action == glfw.PRESS:
                STATE["reflection_axis"] = 0
            elif key == glfw.KEY_Y and action == glfw.PRESS:
                STATE["reflection_axis"] = 1
            elif key == glfw.KEY_Z and action == glfw.PRESS:
                STATE["reflection_axis"] = 2
        elif STATE["option"] == 4:
            if key == glfw.KEY_LEFT:
                STATE["shx"] = _clamp(STATE["shx"] - step_shear_x, -1.2, 1.2)
            elif key == glfw.KEY_RIGHT:
                STATE["shx"] = _clamp(STATE["shx"] + step_shear_x, -1.2, 1.2)
            elif key == glfw.KEY_UP:
                STATE["shy"] = _clamp(STATE["shy"] + step_shear_y, -0.9, 0.9)
            elif key == glfw.KEY_DOWN:
                STATE["shy"] = _clamp(STATE["shy"] - step_shear_y, -0.9, 0.9)

    def on_mouse(window, button, action, mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x, y = glfw.get_cursor_pos(window)
        fw, fh = glfw.get_framebuffer_size(window)
        clicked = hit_test(x, y, fw, fh, clickable_rects + back_rects)
        if clicked == "back":
            glfw.set_window_should_close(window, True)
            return
        if clicked and clicked.startswith("opt_"):
            idx = int(clicked.split("_")[1])
            STATE["option"] = idx

    glfw.set_key_callback(win, on_key)
    glfw.set_mouse_button_callback(win, on_mouse)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        _draw_scene(w, h)

        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, w, 0, h, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        clickable_rects = _draw_mode_tabs(w, h)
        _draw_hud_text(w, h)
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
