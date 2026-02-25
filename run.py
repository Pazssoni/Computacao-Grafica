#!/usr/bin/env python3
"""
Script único para qualquer SO (Linux/Windows): cria o venv, instala dependências e executa o programa.
Uso no terminal ou VS Code:  python run.py   ou   python3 run.py
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    base = Path(__file__).resolve().parent
    venv_dir = base / "venv"
    is_win = sys.platform.startswith("win")
    python_exe = venv_dir / ("Scripts" if is_win else "bin") / ("python.exe" if is_win else "python")
    requirements = base / "requirements.txt"
    main_py = base / "main.py"

    if not requirements.exists():
        print("Arquivo requirements.txt nao encontrado.", file=sys.stderr)
        sys.exit(1)
    if not main_py.exists():
        print("Arquivo main.py nao encontrado.", file=sys.stderr)
        sys.exit(1)

    if not venv_dir.exists():
        print("Criando ambiente virtual (venv)...")
        r = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], cwd=str(base))
        if r.returncode != 0:
            print("Erro ao criar venv.", file=sys.stderr)
            sys.exit(r.returncode)

    if not python_exe.exists():
        print("Python do venv nao encontrado.", file=sys.stderr)
        sys.exit(1)

    print("Instalando dependencias...")
    r = subprocess.run(
        [str(python_exe), "-m", "pip", "install", "-q", "-r", str(requirements)],
        cwd=str(base),
    )
    if r.returncode != 0:
        print("Erro ao instalar dependencias.", file=sys.stderr)
        sys.exit(r.returncode)

    print("Iniciando o programa.")
    os.chdir(base)
    r = subprocess.run([str(python_exe), str(main_py)])
    sys.exit(r.returncode if r.returncode is not None else 0)


if __name__ == "__main__":
    main()
