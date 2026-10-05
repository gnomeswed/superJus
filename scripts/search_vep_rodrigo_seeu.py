# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
nome = "Rodrigo dos Reis Nobrega"
nome_accent = "Rodrigo dos Reis Nóbrega"

print("=== BUSCANDO VEP / EXECUÇÃO PENAL DE RODRIGO DOS REIS NÓBREGA ===")

# Consultar DataJud TJRJ com filtros de execução
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

queries = [
    {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": f'"{nome}" OR "{nome_accent}"'}},
                    {"query_string": {"query": 'execucao OR VEP OR "Vara de Execuções Penais" OR pena'}}
                ]
            }
        },
        "size": 20
    },
    {
        "query": {
            "bool": {
                "must": [
                    {"match": {"orgaoJulgador.nome": "VARA DE EXECUCOES PENAIS"}},
                    {"query_string": {"query": f'"{nome}" OR "{nome_accent}"'}}
                ]
            }
        },
        "size": 20
    },
    {
        "query": {
            "query_string": {"query": f'"{nome}"'}
        },
        "size": 30
    }
]

for idx, q in enumerate(queries, 1):
    print(f"\n[Estratégia {idx}] Consultando...")
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  -> Hits: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                classe = src.get("classe", {}).get("nome")
                grau = src.get("grau")
                dt = src.get("dataAjuizamento")
                print(f"  📌 Processo: {np} | Grau: {grau} | Órgão: {orgao} | Classe: {classe} | Data: {dt}")
    except Exception as e:
        print(f"  Erro: {e}")
