"""Objetos 3D reutilizáveis (glBegin/glEnd). Normais por face ou por vértice."""
import math
from OpenGL.GL import (
    GL_QUADS, GL_TRIANGLES, GL_LINES, GL_LINE_WIDTH,
    glBegin, glEnd, glVertex3f, glNormal3f, glColor3f, glLineWidth,
)
EDGE_LINE_WIDTH = 1.6
EDGE_COLOR = (0.0, 0.0, 0.0)


def draw_cube(size=0.5):
    """Cubo centrado na origem, lado 2*size. Normais por face (Flat)."""
    s = size
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-s, -s, s); glVertex3f(s, -s, s); glVertex3f(s, s, s); glVertex3f(-s, s, s)
    glNormal3f(0, 0, -1)
    glVertex3f(-s, -s, -s); glVertex3f(-s, s, -s); glVertex3f(s, s, -s); glVertex3f(s, -s, -s)
    glNormal3f(0, 1, 0)
    glVertex3f(-s, s, -s); glVertex3f(-s, s, s); glVertex3f(s, s, s); glVertex3f(s, s, -s)
    glNormal3f(0, -1, 0)
    glVertex3f(-s, -s, -s); glVertex3f(s, -s, -s); glVertex3f(s, -s, s); glVertex3f(-s, -s, s)
    glNormal3f(1, 0, 0)
    glVertex3f(s, -s, -s); glVertex3f(s, s, -s); glVertex3f(s, s, s); glVertex3f(s, -s, s)
    glNormal3f(-1, 0, 0)
    glVertex3f(-s, -s, -s); glVertex3f(-s, -s, s); glVertex3f(-s, s, s); glVertex3f(-s, s, -s)
    glEnd()


def draw_cube_edges(size=0.5):
    """Desenha as 12 arestas do cubo em preto (chamar após draw_cube/draw_cube_smooth)."""
    s = size
    verts = [(-s,-s,s),(s,-s,s),(s,s,s),(-s,s,s), (-s,-s,-s),(-s,s,-s),(s,s,-s),(s,-s,-s)]
    edges = [(0,1),(1,2),(2,3),(3,0), (4,5),(5,6),(6,7),(7,4), (0,4),(1,7),(2,6),(3,5)]
    glLineWidth(EDGE_LINE_WIDTH)
    glColor3f(*EDGE_COLOR)
    glBegin(GL_LINES)
    for i, j in edges:
        glVertex3f(*verts[i])
        glVertex3f(*verts[j])
    glEnd()
    glLineWidth(1.0)


def draw_pyramid_edges(size=0.5, height=0.7):
    """Desenha as 8 arestas da pirâmide em preto."""
    s = size
    h2 = height / 2
    apex = (0, h2, 0)
    base = [(-s,-h2,-s),(s,-h2,-s),(s,-h2,s),(-s,-h2,s)]
    glLineWidth(EDGE_LINE_WIDTH)
    glColor3f(*EDGE_COLOR)
    glBegin(GL_LINES)
    for i in range(4):
        j = (i + 1) % 4
        glVertex3f(*base[i])
        glVertex3f(*base[j])
    for i in range(4):
        glVertex3f(*apex)
        glVertex3f(*base[i])
    glEnd()
    glLineWidth(1.0)


def _norm(v):
    L = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
    return (v[0]/L, v[1]/L, v[2]/L) if L > 0 else v


def draw_cube_smooth(size=0.5):
    """Cubo com normais por vértice (Gouraud)."""
    s = size
    vertices = [
        ((-s, -s, s), (-1, -1, 1)), ((s, -s, s), (1, -1, 1)), ((s, s, s), (1, 1, 1)), ((-s, s, s), (-1, 1, 1)),
        ((-s, -s, -s), (-1, -1, -1)), ((-s, s, -s), (-1, 1, -1)), ((s, s, -s), (1, 1, -1)), ((s, -s, -s), (1, -1, -1)),
    ]
    quads = [(0, 1, 2, 3), (4, 5, 6, 7), (3, 2, 6, 5), (4, 7, 1, 0), (1, 7, 6, 2), (4, 0, 3, 5)]
    for quad in quads:
        glBegin(GL_QUADS)
        for i in quad:
            v, n = vertices[i]
            glNormal3f(*_norm(n))
            glVertex3f(*v)
        glEnd()


def draw_pyramid(size=0.5, height=0.7):
    """Pirâmide base quadrada, normais por face."""
    s = size
    h2 = height / 2
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(-s, -h2, -s)
    glVertex3f(s, -h2, -s)
    glVertex3f(s, -h2, s)
    glVertex3f(-s, -h2, s)
    glEnd()
    apex = (0, h2, 0)
    base_verts = [(-s, -h2, -s), (s, -h2, -s), (s, -h2, s), (-s, -h2, s)]
    for i in range(4):
        v0 = base_verts[i]
        v1 = base_verts[(i + 1) % 4]
        dx1, dy1, dz1 = v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2]
        dx2, dy2, dz2 = apex[0]-v0[0], apex[1]-v0[1], apex[2]-v0[2]
        nx = dy1*dz2 - dz1*dy2
        ny = dz1*dx2 - dx1*dz2
        nz = dx1*dy2 - dy1*dx2
        length = (nx*nx + ny*ny + nz*nz) ** 0.5
        if length > 0:
            nx, ny, nz = nx/length, ny/length, nz/length
        glBegin(GL_TRIANGLES)
        glNormal3f(nx, ny, nz)
        glVertex3f(*v0)
        glVertex3f(*v1)
        glVertex3f(*apex)
        glEnd()


def draw_pyramid_smooth(size=0.5, height=0.7):
    """Pirâmide com normais por vértice (Gouraud)."""
    s = size
    h2 = height / 2
    apex = (0, h2, 0)
    base_verts = [(-s, -h2, -s), (s, -h2, -s), (s, -h2, s), (-s, -h2, s)]
    n_apex = (0, 0, 0)
    for i in range(4):
        v0 = base_verts[i]
        v1 = base_verts[(i + 1) % 4]
        dx1, dy1, dz1 = v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2]
        dx2, dy2, dz2 = apex[0]-v0[0], apex[1]-v0[1], apex[2]-v0[2]
        nx = dy1*dz2 - dz1*dy2
        ny = dz1*dx2 - dx1*dz2
        nz = dx1*dy2 - dy1*dx2
        n_apex = (n_apex[0]+nx, n_apex[1]+ny, n_apex[2]+nz)
    length = (n_apex[0]**2 + n_apex[1]**2 + n_apex[2]**2) ** 0.5
    if length > 0:
        n_apex = (n_apex[0]/length, n_apex[1]/length, n_apex[2]/length)

    def face_normal(i):
        v0 = base_verts[i]
        v1 = base_verts[(i + 1) % 4]
        dx1, dy1, dz1 = v1[0]-v0[0], v1[1]-v0[1], v1[2]-v0[2]
        dx2, dy2, dz2 = apex[0]-v0[0], apex[1]-v0[1], apex[2]-v0[2]
        nx = dy1*dz2 - dz1*dy2
        ny = dz1*dx2 - dx1*dz2
        nz = dx1*dy2 - dy1*dx2
        L = (nx*nx+ny*ny+nz*nz)**0.5
        return (nx/L, ny/L, nz/L) if L > 0 else (0, 1, 0)
    normals_base = [face_normal(i) for i in range(4)]
    for i in range(4):
        n1 = normals_base[i]
        n2 = normals_base[(i - 1) % 4]
        nb = (0, -1, 0)
        nx = n1[0] + n2[0] + nb[0]
        ny = n1[1] + n2[1] + nb[1]
        nz = n1[2] + n2[2] + nb[2]
        L = math.sqrt(nx*nx+ny*ny+nz*nz) or 1
        normals_base[i] = (nx/L, ny/L, nz/L)
    glBegin(GL_QUADS)
    for i in range(4):
        glNormal3f(0, -1, 0)
        glVertex3f(*base_verts[i])
    glEnd()
    for i in range(4):
        v0 = base_verts[i]
        v1 = base_verts[(i + 1) % 4]
        n0 = normals_base[i]
        n1 = normals_base[(i + 1) % 4]
        glBegin(GL_TRIANGLES)
        glNormal3f(*n0)
        glVertex3f(*v0)
        glNormal3f(*n1)
        glVertex3f(*v1)
        glNormal3f(*n_apex)
        glVertex3f(*apex)
        glEnd()
