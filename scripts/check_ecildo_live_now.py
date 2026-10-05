# -*- coding: utf-8 -*-
import os
import json
import urllib.request

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
cpf = "08073097290"
cpf_formatted = "080.730.972-90"
nome = "Ecildo Victor dos Santos Ferreira"
tribunais = ["tjmt", "tjrj", "stj", "trf1", "trf2"]

results = {}

for tb in tribunais:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"numeroProcesso": "10035245720238110015"}},
                    {"query_string": {"query": f'"{cpf}"'}},
                    {"query_string": {"query": f'"{cpf_formatted}"'}},
                    {"query_string": {"query": f'"{nome}"'}},
                    {"query_string": {"query": '"Ecildo"'}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 30
    }
    req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"=== {tb.upper()} ({len(hits)} hits) ===")
            results[tb] = []
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                dt = src.get("dataAjuizamento")
                movs = src.get("movimentos", [])
                movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""))
                last_mov = movs_sorted[-1] if movs_sorted else {}
                print(f"Proc: {np} | Classe: {classe} | Orgão: {orgao} | Ultima Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}")
                results[tb].append({
                    "numeroProcesso": np,
                    "classe": classe,
                    "orgao": orgao,
                    "dataAjuizamento": dt,
                    "total_movs": len(movs),
                    "last_mov": last_mov,
                    "all_movs_last5": movs_sorted[-5:] if len(movs_sorted) >= 5 else movs_sorted
                })
    except Exception as e:
        print(f"Erro {tb}: {e}")

with open("scripts/ecildo_live_check_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
