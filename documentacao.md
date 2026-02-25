# Documentação do Software — Projeto Prático de Computação Gráfica

**Instituição:** Instituto Federal Fluminense — Campus Bom Jesus do Itabapoana  
**Disciplina:** Computação Gráfica  
**Projeto:** Projeto prático (6pts) — Integração de 4 módulos  
**Data:** Fevereiro/2025  

---

## 1. Resumo

Este documento descreve o programa desenvolvido para o projeto prático de Computação Gráfica. O sistema é um aplicativo com **menu interativo no terminal** que permite executar quatro módulos independentes, cada um demonstrando um tópico da disciplina: **Transformações Geométricas**, **Projeção**, **ViewPort** e **Iluminação**. O código foi escrito em **Python 3**, utilizando **PyOpenGL** para acesso à API OpenGL, **glfw** para criação de janelas e tratamento de eventos, e **numpy** para operações com matrizes (em especial no módulo de transformações). O desenho utiliza o **modo imediato** do OpenGL (`glBegin`/`glEnd`) para simplicidade e clareza didática.

---

## 2. Arquitetura do Projeto

A estrutura do repositório reflete a divisão do trabalho em quatro duplas (quatro módulos) e um conjunto de utilitários compartilhados:

```
Computacao-Grafica/
├── main.py              # Ponto de entrada: menu no terminal e disparo dos módulos
├── requirements.txt     # Dependências Python (PyOpenGL, glfw, numpy)
├── documentacao.md      # Este documento
├── modulos/
│   ├── __init__.py
│   ├── transformacoes.py   # Módulo 1 — Transformações Geométricas
│   ├── projecao.py         # Módulo 2 — Projeção e câmera (LookAt)
│   ├── viewport.py         # Módulo 3 — Três viewports com projeção ortogonal
│   └── iluminacao.py       # Módulo 4 — Dois modelos de iluminação
└── utils/
    ├── __init__.py
    └── shapes.py           # Objetos 3D reutilizáveis (cubo, pirâmide)
```

- **main.py:** Loop contínuo que exibe o menu (opções 1 a 5), lê a escolha do usuário e, para as opções 1–4, importa dinamicamente o módulo correspondente e chama sua função `run()`. Essa função bloqueia até o usuário fechar a janela; ao retornar, o menu é exibido novamente. A opção 5 encerra o programa.
- **modulos/*.py:** Cada arquivo implementa uma função `run()` que inicializa o GLFW, cria uma janela, configura o contexto OpenGL e executa o loop de renderização até o fechamento da janela. Cada módulo é autocontido e não depende dos outros.
- **utils/shapes.py:** Contém as primitivas 3D usadas em todos os módulos: `draw_cube`, `draw_cube_smooth`, `draw_pyramid` e `draw_pyramid_smooth`, desenhadas com `glBegin`/`glEnd` e, quando necessário, normais por face ou por vértice para iluminação Flat e Gouraud.

---

## 3. Funcionalidade 1 — Transformações Geométricas

**Objetivo:** Exibir um objeto simples (cubo) e aplicar visualmente as cinco transformações exigidas: translação, escala, rotação, reflexão/espelhamento e cisalhamento.

**Implementação:** O módulo `modulos/transformacoes.py` divide a janela em **cinco colunas**. Em cada coluna é desenhado o mesmo cubo (de `utils/shapes.py`) com uma transformação diferente aplicada na matriz de modelagem (modelview), usando projeção ortogonal (`glOrtho`) e uma câmera fixa (translação em Z e rotação leve para melhor visualização).

- **a) Translação:** `glTranslatef(tx, ty, tz)` — desloca o cubo; no código, `(0.4, 0.2, 0)`. Corresponde à matriz de translação 4×4 com componentes (tx, ty, tz) na última coluna.
- **b) Escala:** `glScalef(sx, sy, sz)` — escala o cubo (ex.: 1.4 em todos os eixos). Equivale a uma matriz diagonal com sx, sy, sz na diagonal.
- **c) Rotação:** `glRotatef(ângulo, ax, ay, az)` — rotação em torno do eixo (ax, ay, az); no código, eixo (0, 1, 0) com ângulo animado. OpenGL implementa a rotação de Rodrigues via matriz 4×4.
- **d) Reflexão/Espelhamento (flip):** Reflexão no eixo X com `glScalef(-1, 1, 1)`. Matriz de reflexão em um plano (aqui, plano YZ): escala -1 na componente correspondente.
- **e) Cisalhamento:** Matriz 4×4 de cisalhamento construída com **numpy** (ex.: shear em xy e xz) e aplicada com `glMultMatrixf()`. A matriz é convertida para o formato column-major exigido pelo OpenGL (transposição e passagem como array de floats).

**Funções OpenGL utilizadas:** `glOrtho`, `glLoadIdentity`, `glTranslatef`, `glScalef`, `glRotatef`, `glMultMatrixf`, `glPushMatrix`, `glPopMatrix`, `glViewport`, `glMatrixMode` (GL_PROJECTION, GL_MODELVIEW), além do desenho do cubo em `utils/shapes.py` com `glBegin(GL_QUADS)`, `glVertex3f` e `glColor3f`.

---

## 4. Funcionalidade 2 — Projeção

**Objetivo:** Visualizar um objeto 3D permitindo alterar a **matriz de projeção** (genérica) e a **posição da câmera** (LookAt).

**Implementação:** O módulo `modulos/projecao.py` desenha um cubo central e oferece:
- **Matriz de projeção configurável:** Duas opções — (1) **perspectiva**, implementada com `glFrustum(left, right, bottom, top, near, far)`, formando a matriz genérica de projeção perspectiva (frustum de visão); (2) **ortogonal**, com `glOrtho(left, right, bottom, top, near, far)`. A troca é feita pela tecla **P**.
- **Posição da câmera (LookAt):** `gluLookAt(eye_x, eye_y, eye_z, center_x, center_y, center_z, up_x, up_y, up_z)` define a matriz de visualização: posição do olho (eye), ponto para onde a câmera olha (center) e vetor “para cima” (up). As teclas **W/S** movem a câmera para frente/trás na direção de visão; **A/D** movem à esquerda/direita no plano XZ; **Q/E** sobem/descem. O centro do olhar é deslocado junto com o olho para manter a mesma direção de visão.

**Funções PyOpenGL utilizadas:** `glFrustum`, `glOrtho`, `gluLookAt`, `glViewport`, `glMatrixMode`, `glLoadIdentity`, e o desenho do cubo em `utils/shapes.py`.

---

## 5. Funcionalidade 3 — ViewPort

**Objetivo:** Exibir **um** objeto tridimensional em **três** viewports, com **três posições de câmera** diferentes, usando **projeção ortogonal**.

**Implementação:** O módulo `modulos/viewport.py` divide a janela em três regiões iguais (três colunas). Para cada região:
1. `glViewport(x, y, width, height)` define a área de desenho (um terço da largura da janela).
2. A matriz de **projeção** é definida com `glOrtho(...)` (projeção ortogonal), com aspect ratio ajustado à largura da viewport.
3. A matriz de **modelview** é definida com `gluLookAt(...)` com uma das três câmeras:
   - **Viewport 1:** câmera em (0, 0, 4) olhando para a origem — vista de frente (eixo +Z).
   - **Viewport 2:** câmera em (4, 0, 0) olhando para a origem — vista lateral (eixo +X).
   - **Viewport 3:** câmera em (0, 4, 0) olhando para a origem, com vetor “up” (0, 0, -1) — vista de cima (eixo +Y).
4. O mesmo cubo (`draw_cube`) é desenhado em cada viewport.

Assim, o usuário vê o **mesmo objeto** nas **três** vistas (frente, lado, topo) simultaneamente, usando apenas projeção ortogonal.

**Funções OpenGL utilizadas:** `glViewport`, `glOrtho`, `gluLookAt`, `glLoadIdentity`, `glMatrixMode`, e o desenho do cubo.

---

## 6. Funcionalidade 4 — Iluminação

**Objetivo:** Exibir **dois** objetos tridimensionais com **projeção perspectiva** e **dois modelos de iluminação** diferentes (Flat e Gouraud).

**Implementação:** O módulo `modulos/iluminacao.py` usa projeção perspectiva (`glFrustum`) e uma câmera fixa com `gluLookAt`. Uma luz pontual (`GL_LIGHT0`) é configurada com `glLightfv` (posição, ambiente, difusa, especular). Dois objetos são desenhados lado a lado:

- **Objeto 1 — Cubo com iluminação Flat (constante por face):**  
  `glShadeModel(GL_FLAT)` e o cubo desenhado por `draw_cube`, que define **uma normal por face** com `glNormal3f` antes dos vértices de cada quad. O pipeline usa essa normal para calcular uma única cor por face (iluminação constante na face).

- **Objeto 2 — Pirâmide com iluminação Gouraud:**  
  `glShadeModel(GL_SMOOTH)` e a pirâmide desenhada por `draw_pyramid_smooth`, que define **normais por vértice** (média das normais das faces adjacentes, normalizada). O OpenGL interpola as cores calculadas nos vértices ao longo da face, produzindo o efeito Gouraud.

Materiais são definidos com `glMaterialfv` (GL_AMBIENT_AND_DIFFUSE, GL_SPECULAR, GL_SHININESS). O uso de `GL_NORMALIZE` garante que as normais escaladas pelas transformações sejam renormalizadas para o cálculo correto da iluminação.

**Funções OpenGL utilizadas:** `glEnable(GL_LIGHTING)`, `glLightfv`, `glMaterialfv`, `glShadeModel` (GL_FLAT, GL_SMOOTH), `glFrustum`, `gluLookAt`, além das funções de desenho em `utils/shapes.py` com `glNormal3f` e `glVertex3f`.

---

## 7. Como Executar

1. **Ambiente:** Linux (Debian) com Python 3 e pacotes de desenvolvimento OpenGL/GL (ex.: `libgl1-mesa-dev`, `libglfw3` ou `libglfw-dev`) se necessário.
2. **Criar e ativar o ambiente virtual:**
   ```bash
   cd Computacao-Grafica
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Executar o programa:**
   ```bash
   python main.py
   ```
5. No menu, digite **1**, **2**, **3** ou **4** para abrir o módulo desejado; feche a janela do módulo para voltar ao menu. Digite **5** para sair.

---

## 8. Referências

- Documento do projeto (PDF) — Instituto Federal Fluminense, Campus Bom Jesus do Itabapoana, Projeto prático (6pts).
- OpenGL Programming Guide (Red Book).
- Documentação PyOpenGL: https://pyopengl.sourceforge.io/
- GLFW: https://www.glfw.org/
- NumPy: https://numpy.org/
