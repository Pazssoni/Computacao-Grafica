# Computação Gráfica — Projeto Prático

Projeto prático (6 pts) da disciplina Computação Gráfica — IFF Campus Bom Jesus do Itabapoana. Aplicativo com menu gráfico e quatro módulos: Transformações Geométricas, Projeção, ViewPort e Iluminação.

## Requisitos

- Python 3
- PyOpenGL, glfw, numpy

## Instalação e execução

**Primeira vez (criar ambiente):**
```bash
cd Computacao-Grafica
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

**Para rodar o programa** (escolha um):

1. **Script (recomendado)** — não precisa ativar o venv:
   ```bash
   ./run.sh
   ```
   (Se der "permission denied": `chmod +x run.sh` e tente de novo.)

2. **Com o venv ativado** — no mesmo terminal onde fez `source venv/bin/activate`:
   ```bash
   python main.py
   ```
   No Linux às vezes o comando é `python3` e não `python`. Dentro do venv, `python` costuma funcionar.

3. **Sem ativar o venv** — usar o interpretador do venv direto:
   ```bash
   ./venv/bin/python main.py
   ```

**Por que dá erro?** Se você rodar `python main.py` (ou `python3 main.py`) **fora** do venv, o sistema usa o Python global, que normalmente não tem `glfw` nem `PyOpenGL` instalados → aparece "No module named 'glfw'". Por isso use `run.sh` ou ative o venv antes.

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
