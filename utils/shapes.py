"""
Objetos 3D reutilizáveis para os módulos do projeto.
Desenho em modo imediato OpenGL (glBegin/glEnd).
"""
from OpenGL.GL import (
    GL_QUADS, GL_TRIANGLES,
    glBegin, glEnd, glVertex3f, glNormal3f,
)


def draw_cube(size=0.5):
    """
    Desenha um cubo centrado na origem com lado 2*size.
    Normais por face (adequado para iluminação Flat).
    """
    s = size
    # face +Z (frente)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, 1)
    glVertex3f(-s, -s, s)
    glVertex3f(s, -s, s)
    glVertex3f(s, s, s)
    glVertex3f(-s, s, s)
    glEnd()
    # face -Z (trás)
    glBegin(GL_QUADS)
    glNormal3f(0, 0, -1)
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, -s, -s)
    glEnd()
    # face +Y (topo)
    glBegin(GL_QUADS)
    glNormal3f(0, 1, 0)
    glVertex3f(-s, s, -s)
    glVertex3f(-s, s, s)
    glVertex3f(s, s, s)
    glVertex3f(s, s, -s)
    glEnd()
    # face -Y (baixo)
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(-s, -s, -s)
    glVertex3f(s, -s, -s)
    glVertex3f(s, -s, s)
    glVertex3f(-s, -s, s)
    glEnd()
    # face +X (direita)
    glBegin(GL_QUADS)
    glNormal3f(1, 0, 0)
    glVertex3f(s, -s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, s, s)
    glVertex3f(s, -s, s)
    glEnd()
    # face -X (esquerda)
    glBegin(GL_QUADS)
    glNormal3f(-1, 0, 0)
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, -s, s)
    glVertex3f(-s, s, s)
    glVertex3f(-s, s, -s)
    glEnd()


def draw_cube_smooth(size=0.5):
    """
    Cubo com normais por vértice (média das faces adjacentes).
    Adequado para iluminação Gouraud (GL_SMOOTH).
    """
    s = size
    # Vértices do cubo (8 vértices, cada um com normal normalizada da média das 3 faces)
    # Cada vértice: (x,y,z), (nx,ny,nz) onde n = normalize(face1+face2+face3)
    vertices = [
        ((-s, -s, s), (-1, -1, 1)),   # 0
        ((s, -s, s), (1, -1, 1)),     # 1
        ((s, s, s), (1, 1, 1)),       # 2
        ((-s, s, s), (-1, 1, 1)),     # 3
        ((-s, -s, -s), (-1, -1, -1)), # 4
        ((-s, s, -s), (-1, 1, -1)),   # 5
        ((s, s, -s), (1, 1, -1)),     # 6
        ((s, -s, -s), (1, -1, -1)),   # 7
    ]
    # Normalizar vetores (canto = média de 3 faces = (±1,±1,±1) já normalizado)
    import math
    def norm(v):
        L = math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])
        return (v[0]/L, v[1]/L, v[2]/L) if L > 0 else v
    quads = [
        (0, 1, 2, 3),   # +Z
        (4, 5, 6, 7),   # -Z
        (3, 2, 6, 5),   # +Y
        (4, 7, 1, 0),   # -Y
        (1, 7, 6, 2),   # +X
        (4, 0, 3, 5),   # -X
    ]
    for quad in quads:
        glBegin(GL_QUADS)
        for i in quad:
            v, n = vertices[i]
            n = norm(n)
            glNormal3f(*n)
            glVertex3f(*v)
        glEnd()


def draw_pyramid(size=0.5, height=0.7):
    """
    Pirâmide de base quadrada centrada na origem.
    Base no plano y=-height/2, ápice em y=+height/2.
    Normais por face (adequado para Flat).
    """
    s = size
    h2 = height / 2
    # Base (y = -h2)
    glBegin(GL_QUADS)
    glNormal3f(0, -1, 0)
    glVertex3f(-s, -h2, -s)
    glVertex3f(s, -h2, -s)
    glVertex3f(s, -h2, s)
    glVertex3f(-s, -h2, s)
    glEnd()
    # 4 faces triangulares (ápice em 0, h2, 0)
    apex = (0, h2, 0)
    base_verts = [(-s, -h2, -s), (s, -h2, -s), (s, -h2, s), (-s, -h2, s)]
    for i in range(4):
        v0 = base_verts[i]
        v1 = base_verts[(i + 1) % 4]
        # normal da face = cross(v1-v0, apex-v0)
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
    """
    Pirâmide com normais por vértice para Gouraud.
    Ápice: normal = média das 4 faces. Base: normal (0,-1,0). Vértices da base: normal da face + base.
    """
    s = size
    h2 = height / 2
    apex = (0, h2, 0)
    base_verts = [(-s, -h2, -s), (s, -h2, -s), (s, -h2, s), (-s, -h2, s)]
    # Normal do ápice (média das 4 normais das faces laterais)
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
    # Cada vértice da base: normal = (0,-1,0) para a base; para as laterais usamos a média das 2 faces
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
    # Vértice da base i: média de normal da base (0,-1,0) + face i + face i-1
    import math
    for i in range(4):
        n1 = normals_base[i]
        n2 = normals_base[(i - 1) % 4]
        nb = (0, -1, 0)
        nx = n1[0] + n2[0] + nb[0]
        ny = n1[1] + n2[1] + nb[1]
        nz = n1[2] + n2[2] + nb[2]
        L = math.sqrt(nx*nx+ny*ny+nz*nz) or 1
        normals_base[i] = (nx/L, ny/L, nz/L)
    # Base quad
    glBegin(GL_QUADS)
    for i in range(4):
        glNormal3f(0, -1, 0)
        glVertex3f(*base_verts[i])
    glEnd()
    # 4 triângulos com normais por vértice
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
