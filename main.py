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
from utils.hud import draw_text_2d, text_width
from utils.panel import hit_test

MENU_BUTTONS = [
    ("1", "1 - Transformações Geométricas"),
    ("2", "2 - Projeção"),
    ("3", "3 - ViewPort"),
    ("4", "4 - Iluminação"),
    ("5", "5 - Sair"),
]
BTN_WIDTH = 460
BTN_HEIGHT = 52
BTN_MARGIN = 18
MENU_W = 560
MENU_H = 400
TOP_PAD = 80
BOTTOM_PAD = 28


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
    y = h - TOP_PAD
    for bid, _ in MENU_BUTTONS:
        if y < BOTTOM_PAD + BTN_HEIGHT:
            break
        rects.append((bid, cx, y - BTN_HEIGHT, cx + BTN_WIDTH, y))
        y -= BTN_HEIGHT + BTN_MARGIN
    return rects


def _draw_menu(menu_win, hover_bid=None):
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
    y = h - TOP_PAD
    for bid, label in MENU_BUTTONS:
        if y < BOTTOM_PAD + BTN_HEIGHT:
            break
        if bid == hover_bid:
            glColor3f(0.30, 0.42, 0.62)
            border_color = (0.72, 0.82, 0.98)
        else:
            glColor3f(0.2, 0.22, 0.28)
            border_color = (0.4, 0.43, 0.5)
        _draw_quad(cx, y - BTN_HEIGHT, cx + BTN_WIDTH, y)
        glColor3f(*border_color)
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
        tw = text_width(label, 2)
        tx = cx + (BTN_WIDTH - tw) / 2
        ty = (y - BTN_HEIGHT) + (BTN_HEIGHT / 2) + 5
        draw_text_2d(tx, ty, label, 0.94, 0.96, 1.0)
        rects.append((bid, cx, y - BTN_HEIGHT, cx + BTN_WIDTH, y))
        y -= BTN_HEIGHT + BTN_MARGIN
    title = "ANAMARANATOR 2000 - Escolha o modulo"
    tw = text_width(title, 2)
    draw_text_2d((w - tw) / 2, h - 28, title, 0.88, 0.9, 0.98)
    glEnable(GL_DEPTH_TEST)
    return rects


def main():
    if not glfw.init():
        print("Falha ao inicializar GLFW", file=sys.stderr)
        sys.exit(1)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    menu_win = glfw.create_window(MENU_W, MENU_H, "ANAMARANATOR 2000 - Menu", None, None)
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
        mx, my = glfw.get_cursor_pos(menu_win)
        fw, fh = glfw.get_framebuffer_size(menu_win)
        hover_bid = hit_test(mx, my, fw, fh, _menu_rects(fw, fh))
        rects = _draw_menu(menu_win, hover_bid=hover_bid)
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
