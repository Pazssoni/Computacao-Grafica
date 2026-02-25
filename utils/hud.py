"""Texto 2D em tela (fonte 5x7 em blocos, sem GLUT)."""
from OpenGL.GL import (
    GL_PROJECTION, GL_MODELVIEW, GL_DEPTH_TEST,
    GL_QUADS, GL_LINES,
    glMatrixMode, glLoadIdentity, glOrtho,
    glPushMatrix, glPopMatrix, glDisable, glEnable,
    glColor3f, glBegin, glEnd, glVertex2f,
)

# Fonte 5x7: 7 linhas × 5 bits por caractere (1 = pixel aceso).
_FONT_5X7 = {
    " ": (0, 0, 0, 0, 0, 0, 0),
    "-": (0, 0, 0, 14, 0, 0, 0),
    "0": (14, 17, 19, 21, 25, 17, 14),
    "1": (4, 12, 4, 4, 4, 4, 14),
    "2": (14, 17, 1, 2, 4, 8, 31),
    "3": (14, 17, 1, 6, 1, 17, 14),
    "4": (2, 6, 10, 18, 31, 2, 2),
    "5": (31, 16, 30, 1, 1, 17, 14),
    "6": (14, 16, 30, 17, 17, 17, 14),
    "7": (31, 1, 2, 4, 8, 8, 8),
    "8": (14, 17, 17, 14, 17, 17, 14),
    "9": (14, 17, 17, 15, 1, 17, 14),
    "A": (14, 17, 17, 31, 17, 17, 17),
    "B": (30, 17, 17, 30, 17, 17, 30),
    "C": (14, 17, 16, 16, 16, 17, 14),
    "D": (30, 17, 17, 17, 17, 17, 30),
    "E": (31, 16, 16, 30, 16, 16, 31),
    "F": (31, 16, 16, 30, 16, 16, 16),
    "G": (14, 17, 16, 23, 17, 17, 14),
    "H": (17, 17, 17, 31, 17, 17, 17),
    "I": (14, 4, 4, 4, 4, 4, 14),
    "J": (7, 2, 2, 2, 2, 18, 12),
    "K": (17, 18, 20, 24, 20, 18, 17),
    "L": (16, 16, 16, 16, 16, 16, 31),
    "M": (17, 27, 21, 21, 17, 17, 17),
    "N": (17, 25, 25, 21, 19, 19, 17),
    "O": (14, 17, 17, 17, 17, 17, 14),
    "P": (30, 17, 17, 30, 16, 16, 16),
    "Q": (14, 17, 17, 17, 21, 18, 13),
    "R": (30, 17, 17, 30, 18, 17, 17),
    "S": (14, 17, 16, 14, 1, 17, 14),
    "T": (31, 4, 4, 4, 4, 4, 4),
    "U": (17, 17, 17, 17, 17, 17, 14),
    "V": (17, 17, 17, 17, 17, 10, 4),
    "W": (17, 17, 17, 21, 21, 21, 10),
    "X": (17, 17, 10, 4, 10, 17, 17),
    "Y": (17, 17, 10, 4, 4, 4, 4),
    "Z": (31, 1, 2, 4, 8, 16, 31),
    "?": (14, 17, 1, 2, 4, 0, 4),
    "a": (0, 0, 14, 1, 15, 17, 15),
    "c": (0, 0, 14, 16, 16, 17, 14),
    "e": (0, 0, 14, 17, 31, 16, 14),
    "i": (0, 4, 0, 4, 4, 4, 14),
    "l": (0, 12, 4, 4, 4, 4, 14),
    "m": (0, 0, 10, 21, 21, 17, 17),
    "n": (0, 0, 22, 25, 17, 17, 17),
    "o": (0, 0, 14, 17, 17, 17, 14),
    "r": (0, 0, 22, 24, 16, 16, 16),
    "t": (0, 4, 14, 4, 4, 4, 2),
    "u": (0, 0, 17, 17, 17, 19, 13),
    "v": (0, 0, 17, 17, 10, 10, 4),
}


def _get_glyph(c):
    """Tupla de 7 linhas (5 bits) para o caractere."""
    if c in _FONT_5X7:
        return _FONT_5X7[c]
    u = c.upper() if isinstance(c, str) and len(c) == 1 else c
    return _FONT_5X7.get(u, _FONT_5X7.get("?", _FONT_5X7[" "]))


def _draw_char_blocks(x, y, glyph, scale, r, g, b):
    glColor3f(r, g, b)
    for row, bits in enumerate(glyph):
        for col in range(5):
            if (bits >> (4 - col)) & 1:
                x1 = x + col * scale
                y1 = y - row * scale
                x2 = x1 + scale
                y2 = y1 + scale
                glBegin(GL_QUADS)
                glVertex2f(x1, y1)
                glVertex2f(x2, y1)
                glVertex2f(x2, y2)
                glVertex2f(x1, y2)
                glEnd()


def draw_text_blocks(x, y, text, scale=2, r=1, g=1, b=1):
    if not text:
        return
    _acc = {"ã": "a", "á": "a", "â": "a", "à": "a", "ç": "c", "é": "e", "ê": "e", "í": "i", "ó": "o", "ô": "o", "õ": "o", "ú": "u"}
    cx = x
    char_w = 6 * scale
    for c in text:
        draw_c = _acc.get(c, c)
        glyph = _get_glyph(draw_c)
        _draw_char_blocks(cx, y, glyph, scale, r, g, b)
        cx += char_w


def draw_text_2d(x, y, text, r=1, g=1, b=1):
    if not text:
        return
    draw_text_blocks(x, y, text, scale=2, r=r, g=g, b=b)


def text_width(text, scale=2):
    """Largura aproximada em pixels (para centralizar texto)."""
    return len(text) * 6 * scale


def draw_text_block(w, h, lines, line_height=18):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, w, 0, h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    yy = h - line_height
    for s in lines:
        if s:
            draw_text_2d(10, yy, s, 0.9, 0.9, 0.9)
        yy -= line_height
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_viewport_border(screen_w, screen_h, vx, vy, vw, vh, r=0.4, g=0.45, b=0.5):
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, screen_w, 0, screen_h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(r, g, b)
    glBegin(GL_LINES)
    glVertex2f(vx, vy)
    glVertex2f(vx + vw, vy)
    glVertex2f(vx + vw, vy)
    glVertex2f(vx + vw, vy + vh)
    glVertex2f(vx + vw, vy + vh)
    glVertex2f(vx, vy + vh)
    glVertex2f(vx, vy + vh)
    glVertex2f(vx, vy)
    glEnd()
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
