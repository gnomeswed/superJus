# -*- coding: utf-8 -*-
"""Reindexa memórias sem segmentos no memU.

Memórias gravadas via INSERT direto no SQLite (scripts antigos) ficaram sem
segmentos/embeddings, então não aparecem na busca semântica (`memu retrieve`).
Este script lê esses arquivos do banco e os reenvia via `memu commit`, que
segmenta e gera embeddings — atualizando os registros existentes sem duplicar
(o commit é keyed por track+name).

Uso:
    python scripts/memu_reindex.py
"""
import json
import os
import sqlite3
import subprocess
import sys
import tempfile

DB_PATH = os.path.expanduser("~/.memu/memu.sqlite3")


def main() -> None:
    if not os.path.exists(DB_PATH):
        print(f"ERRO: banco não encontrado em {DB_PATH}")
        sys.exit(1)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        SELECT f.name, f.track, f.description, f.content
        FROM memu_recall_files f
        WHERE NOT EXISTS (
            SELECT 1 FROM memu_recall_file_segments s WHERE s.recall_file_id = f.id
        )
        ORDER BY f.track, f.name
        """
    )
    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("Nenhuma memória sem segmentos. Nada a reindexar.")
        return

    print(f"=== REINDEXANDO {len(rows)} memória(s) sem segmentos ===")
    payload = {
        "recall_files": [
            {
                "name": r[0],
                "track": r[1],
                "description": r[2],
                "content": r[3],
            }
            for r in rows
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
        print("ERRO ao reindexar:", result.stderr.strip() or result.stdout.strip())
        sys.exit(1)

    print(result.stdout)
    print("SUCESSO: memórias reindexadas com segmentos e embeddings.")


if __name__ == "__main__":
    main()
