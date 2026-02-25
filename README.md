# Computação Gráfica — Projeto Prático (ANAMARANATOR 2000)

Projeto prático (6 pts) da disciplina Computação Gráfica — IFF Campus Bom Jesus do Itabapoana. Aplicativo **ANAMARANATOR 2000** com menu gráfico e quatro módulos: Transformações Geométricas, Projeção, ViewPort e Iluminação.

## Requisitos

- **Python 3** instalado (o único requisito manual; o resto o script instala).

## Como executar (Linux e Windows)

Abra o terminal (VS Code, Cmd, PowerShell ou terminal do sistema), entre na pasta do projeto e rode:

```bash
cd Computacao-Grafica
python run.py
```

Se no seu sistema o comando for `python3`:

```bash
python3 run.py
```

O **run.py** faz tudo sozinho em qualquer SO (Linux, Windows, macOS):

1. Cria a pasta `venv` (ambiente virtual) se ainda não existir  
2. Instala as dependências (`PyOpenGL`, `glfw`, `numpy`) dentro do venv  
3. Executa o programa (`main.py`)

Não é preciso ativar o venv nem instalar nada manualmente. Na primeira execução pode demorar um pouco por causa do `pip install`; nas seguintes sobe direto.

**No VS Code:** abra a pasta do projeto, abra o terminal integrado (Terminal → Novo Terminal) e execute `python run.py` ou `python3 run.py` nessa pasta.

No menu, clique na opção desejada (1–4) ou em "5 - Sair". Em cada módulo, use o botão **Voltar ao menu** para retornar.

## Estrutura

```
├── main.py              # Entrada: menu gráfico (ANAMARANATOR 2000)
├── run.py               # Instala dependências e executa (Linux/Windows)
├── run.sh               # Atalho de execução (Linux/macOS)
├── requirements.txt
├── README.md
├── documentacao.md       # Documentação detalhada do projeto
├── modulos/
│   ├── transformacoes.py   # Módulo 1 — Translação, escala, rotação, reflexão, cisalhamento
│   ├── projecao.py          # Módulo 2 — Projeção perspectiva/ortogonal, câmera LookAt
│   ├── viewport.py          # Módulo 3 — Três viewports, três câmeras, projeção ortogonal
│   └── iluminacao.py        # Módulo 4 — Cubo e pirâmide, Flat/Smooth (Gouraud)
└── utils/
    ├── shapes.py            # Cubo e pirâmide; arestas pretas (draw_*_edges)
    ├── hud.py               # Texto 2D (fonte em blocos 5x7)
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
