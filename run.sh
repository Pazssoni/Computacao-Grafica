#!/bin/bash
# Executa o projeto usando o Python do venv (evita "python não encontrado" e módulos faltando).
cd "$(dirname "$0")"
if [ ! -d "venv" ]; then
    echo "Crie o venv antes: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi
exec ./venv/bin/python main.py
