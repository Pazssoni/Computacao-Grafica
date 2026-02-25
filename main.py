#!/usr/bin/env python3
"""
Projeto prático - Computação Gráfica (6pts)
Menu principal no terminal: executa um dos 4 módulos ou sai.
Ao fechar a janela do módulo, retorna ao menu.
"""
import sys


def print_menu():
    print("\n" + "=" * 50)
    print("  PROJETO PRÁTICO - COMPUTAÇÃO GRÁFICA")
    print("=" * 50)
    print("  1 - Transformações Geométricas")
    print("  2 - Projeção")
    print("  3 - ViewPort")
    print("  4 - Iluminação")
    print("  5 - Sair")
    print("=" * 50)


def main():
    while True:
        print_menu()
        try:
            opcao = input("Escolha uma opção (1-5): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando.")
            sys.exit(0)
        if opcao == "5":
            print("Até logo!")
            sys.exit(0)
        if opcao == "1":
            from modulos.transformacoes import run
            run()
            continue
        if opcao == "2":
            from modulos.projecao import run
            run()
            continue
        if opcao == "3":
            from modulos.viewport import run
            run()
            continue
        if opcao == "4":
            from modulos.iluminacao import run
            run()
            continue
        print("Opção inválida. Digite 1, 2, 3, 4 ou 5.")


if __name__ == "__main__":
    main()
