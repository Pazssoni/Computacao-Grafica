# Computação Gráfica — Projeto Prático

Projeto prático (6 pts) da disciplina Computação Gráfica — IFF Campus Bom Jesus do Itabapoana. Aplicativo com menu gráfico e quatro módulos: Transformações Geométricas, Projeção, ViewPort e Iluminação.

## Requisitos

- Python 3
- PyOpenGL, glfw, numpy

## Instalação e execução

```bash
cd Computacao-Grafica
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python main.py
```

No menu, clique na opção desejada (1–4) ou em "5 - Sair". Em cada módulo, use o botão **Voltar ao menu** para retornar.

## Estrutura

```
├── main.py              # Entrada: menu gráfico (GLFW)
├── requirements.txt
├── README.md
├── documentacao.md       # Documentação detalhada do projeto
├── modulos/
│   ├── transformacoes.py   # Módulo 1 — Translação, escala, rotação, reflexão, cisalhamento
│   ├── projecao.py          # Módulo 2 — Projeção perspectiva/ortogonal, câmera LookAt
│   ├── viewport.py          # Módulo 3 — Três viewports, três câmeras, projeção ortogonal
│   └── iluminacao.py        # Módulo 4 — Cubo e pirâmide, Flat/Smooth (Gouraud)
└── utils/
    ├── shapes.py            # Cubo e pirâmide (normais por face e por vértice)
    ├── hud.py               # Texto 2D (fonte em blocos)
    ├── panel.py             # Botão "Voltar ao menu" e hit test
    └── axes.py              # Eixos X/Y/Z para referência
```

## Controles por módulo

| Módulo | Teclas | Outros |
|--------|--------|--------|
| 1 Transformações | Space (pausa), T/Y, E/D, R/V, F, C/X | Clique em "Voltar ao menu" |
| 2 Projeção | P (perspectiva/ortogonal), W/S, A/D, Q/E | Idem |
| 3 ViewPort | Z / Shift+Z (zoom), O (objeto), A (eixos) | Idem |
| 4 Iluminação | Space (Flat / Smooth) | Idem |

Documentação completa: [documentacao.md](documentacao.md).
