"""Eixos 3D (X vermelho, Y verde, Z azul) para referência."""
from OpenGL.GL import (
    GL_LINES, GL_LINE_WIDTH,
    glBegin, glEnd, glVertex3f, glColor3f, glLineWidth,
)


def draw_axes(size=1.0, line_width=2.0):
    """Três linhas na origem: X vermelho, Y verde, Z azul."""
    glLineWidth(line_width)
    glBegin(GL_LINES)
    glColor3f(1, 0, 0); glVertex3f(0, 0, 0); glVertex3f(size, 0, 0)
    glColor3f(0, 1, 0); glVertex3f(0, 0, 0); glVertex3f(0, size, 0)
    glColor3f(0, 0, 1); glVertex3f(0, 0, 0); glVertex3f(0, 0, size)
    glEnd()
    glLineWidth(1.0)
