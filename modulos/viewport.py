"""Módulo 3 — Três viewports com três câmeras (frente, lado, topo). Projeção ortogonal. Z/O/A."""
import glfw
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST,
    GL_LIGHTING, GL_LIGHT0, GL_NORMALIZE, GL_SMOOTH,
    GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_PROJECTION, GL_MODELVIEW,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    glClear, glClearColor, glLoadIdentity, glMatrixMode,
    glViewport, glOrtho,
    glEnable, glPushMatrix, glPopMatrix,
    glLightfv, glMaterialfv, glShadeModel,
    glRotatef,
)
from OpenGL.GLU import gluLookAt
from OpenGL import GL
from utils.shapes import draw_cube_smooth, draw_pyramid
from utils.axes import draw_axes
from utils.hud import draw_text_2d, draw_viewport_border
from utils.panel import draw_back_button, hit_test

STATE = {"dim": 1.6, "object_index": 1, "show_axes": True}
DIM_MIN, DIM_MAX = 0.6, 3.0
DIST = 5.0
OBJECTS = [
    ("Cubo", lambda: draw_cube_smooth(0.5)),
    ("Pirâmide", lambda: draw_pyramid(0.5, 0.8)),
]
LABELS = ["Frente", "Lado", "Topo"]


def _cameras(dist):
    return [
        {"eye": (0, 0, dist), "center": (0, 0, 0), "up": (0, 1, 0)},
        {"eye": (dist, 0, 0), "center": (0, 0, 0), "up": (0, 1, 0)},
        {"eye": (0, dist, 0), "center": (0, 0, 0), "up": (0, 0, -1)},
    ]


def run():
    if not glfw.init():
        return
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 2)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    win = glfw.create_window(1000, 400, "ViewPort | Z/O/A teclado | Voltar ao menu", None, None)
    if not win:
        glfw.terminate()
        return
    glfw.make_context_current(win)
    glClearColor(0.1, 0.12, 0.16, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.35, 0.35, 0.35, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.85, 0.85, 0.85, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.5, 0.5, 0.5, 1.0))
    light_pos = [3, 3, 3, 1.0]

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

    back_rects = []

    def on_mouse(window, button, action, mods):
        if button != glfw.MOUSE_BUTTON_LEFT or action != glfw.PRESS:
            return
        x, y = glfw.get_cursor_pos(window)
        w, h = glfw.get_framebuffer_size(window)
        if hit_test(x, y, w, h, back_rects) == "back":
            glfw.set_window_should_close(window, True)

    glfw.set_key_callback(win, on_key)
    glfw.set_mouse_button_callback(win, on_mouse)

    while not glfw.window_should_close(win):
        w, h = glfw.get_framebuffer_size(win)
        glViewport(0, 0, w, h)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        third = w // 3
        dim = STATE["dim"]
        cameras = _cameras(DIST)
        obj_name, draw_obj = OBJECTS[STATE["object_index"]]

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
            cx = i * third + third // 2 - 25
            draw_text_2d(cx, h - 22, LABELS[i], 0.95, 0.95, 0.9)
        draw_text_2d(10, 12, f"Objeto: {obj_name} | Zoom: {STATE['dim']:.2f}", 0.75, 0.8, 0.85)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        back_rects = draw_back_button(w, h)

        glfw.swap_buffers(win)
        glfw.poll_events()

    glfw.destroy_window(win)
