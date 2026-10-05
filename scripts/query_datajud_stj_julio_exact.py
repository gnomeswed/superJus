# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

queries = [
    {"query": {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": "Julio Pereira Marcos"}}},
    {"query": {"query_string": {"query": '"1.116.750"'}}},
    {"query": {"query_string": {"query": '"0311210-10.2026.3.00.0000"'}}},
    {"query": {"query_string": {"query": '"2026/0311210-7"'}}},
    {"query": {"match": {"numeroProcesso": "03112101020263000000"}}}
]

print("=== CONSULTANDO STJ VIA DATAJUD OFICIAL (SEM BLOQUEIOS) ===")

for idx, q in enumerate(queries, 1):
    print(f"\n[Tentativa {idx}] Executando query...")
    try:
        req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  -> Hits encontrados: {len(hits)}")
            if hits:
                for h in hits:
                    src = h["_source"]
                    np = src.get("numeroProcesso")
                    classe = src.get("classe", {}).get("nome")
                    dt = src.get("dataAjuizamento")
                    movs = src.get("movimentos", [])
                    movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                    print(f"  📌 Processo: {np} | Classe: {classe} | Ajuizamento: {dt}")
                    print(f"     Total Movimentos: {len(movs)}")
                    print("     Últimos 5 movimentos:")
                    for m in movs_sorted[:5]:
                        print(f"       • {m.get('dataHora')} - {m.get('nome')}")
                break
    except Exception as e:
        print(f"  Erro: {e}")
