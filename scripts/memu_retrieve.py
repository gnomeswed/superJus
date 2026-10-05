# -*- coding: utf-8 -*-
"""Busca semântica na memória compartilhada memU.

Uso:
    python scripts/memu_retrieve.py "termos da busca"
"""
import subprocess
import sys
sys.stdout.reconfigure(encoding='utf-8')


def main() -> None:
    if len(sys.argv) < 2:
        print('Uso: python scripts/memu_retrieve.py "termos da busca"')
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    try:
        result = subprocess.run(
            ["memu", "retrieve", query],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        print("ERRO: CLI 'memu' não encontrado no PATH. Instale com: pip install memu-cli")
        sys.exit(1)

    if result.returncode != 0:
        print("ERRO ao consultar memU:", result.stderr.strip() or result.stdout.strip())
        sys.exit(1)

    print(result.stdout)


if __name__ == "__main__":
    main()
