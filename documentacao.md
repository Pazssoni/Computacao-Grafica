# Documentação do Projeto — Computação Gráfica

**Instituição:** Instituto Federal Fluminense — Campus Bom Jesus do Itabapoana  
**Disciplina:** Computação Gráfica  
**Projeto:** Projeto prático (6 pts) — Integração de 4 módulos  
**Data:** Fevereiro/2025  

---

## 1. Resumo

Sistema com **menu gráfico** (janela GLFW): o usuário escolhe o módulo com o mouse. Cada módulo abre em janela própria; ao fechar ou clicar em "Voltar ao menu", retorna ao menu. Desenvolvido em **Python 3** com **PyOpenGL** (modo imediato), **glfw** e **numpy** (módulo de transformações).

---

## 2. Arquitetura

```
Computacao-Grafica/
├── main.py              # Menu gráfico; dispara run() de cada módulo
├── requirements.txt
├── documentacao.md
├── modulos/
│   ├── transformacoes.py   # Módulo 1
│   ├── projecao.py         # Módulo 2
│   ├── viewport.py         # Módulo 3
│   └── iluminacao.py       # Módulo 4
└── utils/
    ├── shapes.py           # Cubo e pirâmide (Flat e Gouraud)
    ├── hud.py              # Texto 2D (fonte em blocos 5x7, sem GLUT)
    ├── panel.py            # Botão "Voltar ao menu" e hit test de mouse
    └── axes.py             # Eixos X/Y/Z (referência visual)
```

- **main.py:** Loop do menu: desenha botões, trata clique, importa o módulo e chama `run()`. Ao retornar, restaura contexto e exibe o menu de novo. Opção 5 encerra.
- **modulos/*.py:** Cada um exporta `run()`: cria janela GLFW, configura OpenGL e loop de renderização; não chama `glfw.terminate()` ao sair.
- **utils/shapes.py:** `draw_cube`, `draw_cube_smooth`, `draw_pyramid`, `draw_pyramid_smooth` (glBegin/glEnd; normais por face ou por vértice).
- **utils/hud.py:** Texto em tela com fonte 5x7 em blocos (quads), sem dependência de GLUT.
- **utils/panel.py:** Desenho do botão e retângulos para clique; `hit_test` converte coordenadas do mouse (y de cima para baixo) para coordenadas OpenGL.

---

## 3. Módulo 1 — Transformações Geométricas

Objetivo: cubo com as cinco transformações (translação, escala, rotação, reflexão, cisalhamento).

Janela dividida em **cinco colunas**. Em cada coluna: projeção ortogonal (`glOrtho`), câmera fixa (translação em Z, rotação leve). Cubo de `utils/shapes.draw_cube(0.35)` com uma transformação por coluna:

- **Translação:** `glTranslatef(tx, ty, 0)` — teclas T (aumentar) / Y (diminuir).
- **Escala:** `glScalef(s, s, s)` — E / D.
- **Rotação:** `glRotatef(ângulo, 0, 1, 0)` — R / V (velocidade).
- **Reflexão:** `glScalef(-1,1,1)` ou (1,-1,1) ou (1,1,-1) — F (cicla eixo).
- **Cisalhamento:** matriz 4×4 com numpy, aplicada com `glMultMatrixf` (column-major via transposição).

Tecla Space pausa a animação. Rótulos e status em texto 2D (hud); botão "Voltar ao menu" (panel).

---

## 4. Módulo 2 — Projeção

Objetivo: objeto 3D com projeção configurável e câmera (LookAt).

- **Projeção:** tecla P alterna entre perspectiva (`glFrustum`) e ortogonal (`glOrtho`).
- **Câmera:** `gluLookAt(eye, center, up)`. W/S (frente/trás), A/D (esquerda/direita no plano XZ), Q/E (cima/baixo). Eye e center deslocados juntos para manter a direção.

Cubo de `utils/shapes.draw_cube(0.5)`. Luz e material para realce. Botão "Voltar ao menu".

---

## 5. Módulo 3 — ViewPort

Objetivo: um objeto em **três** viewports com **três** câmeras e projeção ortogonal.

Para cada terço da janela: `glViewport`; `glOrtho` com aspect ratio da viewport; `gluLookAt` com uma das três câmeras (frente: eye em (0,0,d); lado: (d,0,0); topo: (0,d,0) com up (0,0,-1)). Mesmo objeto (cubo ou pirâmide de `utils/shapes`) desenhado nas três vistas. Teclas: Z / Shift+Z (zoom), O (troca objeto), A (liga/desliga eixos). Bordas das viewports e rótulos via hud; eixos via `utils/axes.draw_axes`.

---

## 6. Módulo 4 — Iluminação

Objetivo: dois objetos 3D com projeção perspectiva e alternância entre Flat e Gouraud.

Geometria própria no módulo (cubo e pirâmide do formato original do grupo): cubo -1 a 1 com normais por face; pirâmide com quatro triângulos e normais por face. Projeção: `gluPerspective(45, aspect, 0.1, 50)`; câmera em (0, 0, 10) olhando para a origem. Cubo à esquerda (-2.5, 0, 0), pirâmide à direita (2.5, 0, 0), ambos com rotação contínua.

Tecla **Space** alterna `glShadeModel(GL_FLAT)` e `glShadeModel(GL_SMOOTH)`. Luz direcional `GL_LIGHT0`; materiais com ambiente/difuso e especular. HUD e botão "Voltar ao menu" como nos demais módulos.

---

## 7. Como executar

1. Ambiente: Python 3; dependências OpenGL/GL (ex.: `libgl1-mesa-dev`, `libglfw-dev`) se necessário.
2. `python3 -m venv venv` → `source venv/bin/activate` (Linux/macOS).
3. `pip install -r requirements.txt`
4. `python main.py`
5. No menu, clicar em 1, 2, 3 ou 4 para abrir o módulo; fechar a janela ou clicar em "Voltar ao menu" para voltar; 5 para sair.

---

## 8. Referências

- Enunciado do projeto — IFF, Campus Bom Jesus do Itabapoana.
- OpenGL Programming Guide (Red Book).
- PyOpenGL: https://pyopengl.sourceforge.io/
- GLFW: https://www.glfw.org/
