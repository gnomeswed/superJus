# -*- coding: utf-8 -*-
"""Grava memória na base compartilhada memU (mesma usada por Antigravity/Hermes/OpenCode).

Uso:
    python scripts/memu_store.py --name "Nome" --track memory --description "Descrição" --content "Conteúdo"

O comando delega para `memu commit`, que gera embeddings automaticamente
e deixa a memória pesquisável por similaridade.

Uso com arquivo (evita problemas de escaping em conteúdo longo):
    python scripts/memu_store.py --name "Nome" --track memory --description "Descrição" --content-file caminho/arquivo.md
"""
import argparse
import json
import subprocess
import sys
import tempfile
import os


def main() -> None:
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description="Grava memória no memU")
    parser.add_argument("--name", required=True, help="Nome da memória (ex.: memoria_caso_julio.md)")
    parser.add_argument("--track", default="memory", choices=["memory", "skill", "Julio_Pereira_Marcos_Caso_Principal", "TJRJ_Scraper_Workflow"], help="Trilha da memória")
    parser.add_argument("--description", required=True, help="Descrição curta e acionável (1 linha)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--content", help="Conteúdo da memória diretamente")
    group.add_argument("--content-file", help="Arquivo com o conteúdo da memória")
    args = parser.parse_args()

    if args.content_file:
        content = open(args.content_file, "r", encoding="utf-8").read()
    else:
        content = args.content

    payload = {
        "recall_files": [
            {
                "name": args.name,
                "track": args.track,
                "description": args.description,
                "content": content,
            }
        ]
    }

    with tempfile.NamedTemporaryFile(
        "w", suffix=".json", delete=False, encoding="utf-8"
    ) as f:
        json.dump(payload, f, ensure_ascii=False)
        payload_path = f.name

    try:
        result = subprocess.run(
            ["memu", "commit", payload_path, "--json"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except FileNotFoundError:
        print("ERRO: CLI 'memu' não encontrado no PATH. Instale com: pip install memu-cli")
        sys.exit(1)
    finally:
        os.unlink(payload_path)

    if result.returncode != 0:
        print("ERRO ao gravar no memU:", result.stderr.strip() or result.stdout.strip())
        sys.exit(1)

    print("SUCESSO: memória gravada no memU.")
    print(result.stdout)


if __name__ == "__main__":
    main()
