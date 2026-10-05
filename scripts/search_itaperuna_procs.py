# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"

url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

print("=== BUSCANDO PROCESSOS NA COMARCA DE ITAPERUNA (8.19.0026) ===")

queries = [
    {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": '"ITAPERUNA"'}},
                    {"query_string": {"query": '"Renato Bastos Rocha" OR "Renato Bastos"'}}
                ]
            }
        },
        "size": 30
    },
    {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": '"8.19.0026"'}},
                    {"query_string": {"query": '"Renato"'}}
                ]
            }
        },
        "size": 30
    },
    {
        "query": {
            "wildcard": {
                "numeroProcesso": "*8190026"
            }
        },
        "size": 30
    }
]

for idx, q in enumerate(queries, 1):
    print(f"\n[Consulta {idx}]...")
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"Hits: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                dt = src.get("dataAjuizamento")
                print(f"  📌 {np} | {classe} | {orgao} | {dt}")
    except Exception as e:
        print(f"Erro: {e}")
