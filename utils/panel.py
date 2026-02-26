"""Botão 'Voltar ao menu' e hit test de mouse (coordenadas OpenGL 2D; glfw y invertido)."""
from OpenGL.GL import (
    GL_PROJECTION, GL_MODELVIEW, GL_DEPTH_TEST, GL_LIGHTING,
    GL_QUADS, GL_LINES,
    glMatrixMode, glLoadIdentity, glOrtho,
    glPushMatrix, glPopMatrix, glDisable, glEnable,
    glBegin, glEnd, glVertex2f, glColor3f, glIsEnabled,
)
from utils.hud import draw_text_2d, text_width

BACK_BUTTON_W = 200
BACK_BUTTON_H = 44
BACK_MARGIN = 20


def _draw_quad(x1, y1, x2, y2):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def draw_back_button(w, h):
    """Desenha botão no canto inferior esquerdo. Retorna [(id, x1, y1, x2, y2)] para hit_test."""
    x1 = BACK_MARGIN
    y1 = BACK_MARGIN
    x2 = x1 + BACK_BUTTON_W
    y2 = y1 + BACK_BUTTON_H
    lighting_was_enabled = glIsEnabled(GL_LIGHTING)
    depth_was_enabled = glIsEnabled(GL_DEPTH_TEST)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, w, 0, h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(0.22, 0.24, 0.30)
    _draw_quad(x1, y1, x2, y2)
    glColor3f(0.45, 0.48, 0.55)
    glBegin(GL_LINES)
    glVertex2f(x1, y2)
    glVertex2f(x2, y2)
    glVertex2f(x2, y2)
    glVertex2f(x2, y1)
    glVertex2f(x2, y1)
    glVertex2f(x1, y1)
    glVertex2f(x1, y1)
    glVertex2f(x1, y2)
    glEnd()
    label = "Voltar ao menu"
    tw = text_width(label, 2)
    tx = x1 + (BACK_BUTTON_W - tw) / 2
    ty = y1 + (BACK_BUTTON_H / 2) + 5
    draw_text_2d(tx, ty, label, 0.95, 0.96, 1.0)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    if lighting_was_enabled:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)
    if depth_was_enabled:
        glEnable(GL_DEPTH_TEST)
    else:
        glDisable(GL_DEPTH_TEST)
    return [("back", x1, y1, x2, y2)]


def hit_test(mouse_x_glfw, mouse_y_glfw, w, h, rects):
    """rects: [(id, x1, y1, x2, y2)]. Retorna id do retângulo clicado ou None (y do glfw invertido)."""
    if not rects:
        return None
    y_flip = h - mouse_y_glfw
    for r in rects:
        bid, x1, y1, x2, y2 = r[0], r[1], r[2], r[3], r[4]
        if x1 <= mouse_x_glfw <= x2 and y1 <= y_flip <= y2:
            return bid
    return None
