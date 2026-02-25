#!/usr/bin/env python3
"""Projeto prático Computação Gráfica (6 pts). Menu gráfico GLFW; escolha do módulo por clique."""
import sys
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_TEST,
    GL_PROJECTION, GL_MODELVIEW,
    GL_QUADS, GL_LINES,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho,
    glDisable, glEnable,
    glBegin, glEnd, glVertex2f, glColor3f,
)
from utils.hud import draw_text_2d
from utils.panel import hit_test

MENU_BUTTONS = [
    ("1", "1 - Transformações Geométricas"),
    ("2", "2 - Projeção"),
    ("3", "3 - ViewPort"),
    ("4", "4 - Iluminação"),
    ("5", "5 - Sair"),
]
BTN_WIDTH = 420
BTN_HEIGHT = 44
BTN_MARGIN = 12
MENU_W = 480
MENU_H = 320


def _draw_quad(x1, y1, x2, y2):
    glBegin(GL_QUADS)
    glVertex2f(x1, y1)
    glVertex2f(x2, y1)
    glVertex2f(x2, y2)
    glVertex2f(x1, y2)
    glEnd()


def _menu_rects(w, h):
    cx = (w - BTN_WIDTH) / 2
    rects = []
    y = h - 50
    for bid, _ in MENU_BUTTONS:
        if y < 30:
            break
        rects.append((bid, cx, y - BTN_HEIGHT, cx + BTN_WIDTH, y))
        y -= BTN_HEIGHT + BTN_MARGIN
    return rects


def _draw_menu(menu_win):
    w, h = glfw.get_framebuffer_size(menu_win)
    glViewport(0, 0, w, h)
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, 0, h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    cx = (w - BTN_WIDTH) / 2
    rects = []
    y = h - 50
    for bid, label in MENU_BUTTONS:
        if y < 30:
            break
        glColor3f(0.18, 0.2, 0.26)
        _draw_quad(cx, y - BTN_HEIGHT, cx + BTN_WIDTH, y)
        glColor3f(0.35, 0.38, 0.45)
        glBegin(GL_LINES)
        glVertex2f(cx, y)
        glVertex2f(cx + BTN_WIDTH, y)
        glVertex2f(cx + BTN_WIDTH, y)
        glVertex2f(cx + BTN_WIDTH, y - BTN_HEIGHT)
        glVertex2f(cx + BTN_WIDTH, y - BTN_HEIGHT)
        glVertex2f(cx, y - BTN_HEIGHT)
        glVertex2f(cx, y - BTN_HEIGHT)
        glVertex2f(cx, y)
        glEnd()
        draw_text_2d(cx + 20, y - 28, label, 0.92, 0.94, 1.0)
        rects.append((bid, cx, y - BTN_HEIGHT, cx + BTN_WIDTH, y))
        y -= BTN_HEIGHT + BTN_MARGIN
    draw_text_2d(cx, h - 22, "Computação Gráfica - Escolha o módulo", 0.85, 0.88, 0.95)
    glEnable(GL_DEPTH_TEST)
    return rects


def main():
    if not glfw.init():
        print("Falha ao inicializar GLFW", file=sys.stderr)
        sys.exit(1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    menu_win = glfw.create_window(MENU_W, MENU_H, "Computação Gráfica - Menu", None, None)
    if not menu_win:
        glfw.terminate()
        print("Falha ao criar janela do menu", file=sys.stderr)
        sys.exit(1)
    glfw.make_context_current(menu_win)
    glClearColor(0.12, 0.13, 0.18, 1.0)

    pending_click = [None]

    def on_mouse(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            fw, fh = glfw.get_framebuffer_size(window)
            rects = _menu_rects(fw, fh)
            bid = hit_test(x, y, fw, fh, rects)
            if bid:
                pending_click[0] = bid

    glfw.set_mouse_button_callback(menu_win, on_mouse)

    while not glfw.window_should_close(menu_win):
        rects = _draw_menu(menu_win)
        glfw.swap_buffers(menu_win)
        glfw.poll_events()

        bid = pending_click[0]
        if bid is not None:
            pending_click[0] = None
            if bid == "5":
                break
            if bid == "1":
                from modulos.transformacoes import run
                run()
                glfw.make_context_current(menu_win)
            elif bid == "2":
                from modulos.projecao import run
                run()
                glfw.make_context_current(menu_win)
            elif bid == "3":
                from modulos.viewport import run
                run()
                glfw.make_context_current(menu_win)
            elif bid == "4":
                from modulos.iluminacao import run
                run()
                glfw.make_context_current(menu_win)

    glfw.destroy_window(menu_win)
    glfw.terminate()


if __name__ == "__main__":
    main()
