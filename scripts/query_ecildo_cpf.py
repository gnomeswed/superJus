# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.error

DATAJUD_API_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

cpf = "08073097290"
cpf_formatted = "080.730.972-90"
nome = "Ecildo Victor dos Santos Ferreira"

tribunais = ["tjmt", "tjrj", "stj", "trf1", "trf2"]

results_by_tribunal = {}

for tb in tribunais:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {
        "Authorization": DATAJUD_API_KEY,
        "Content-Type": "application/json"
    }
    
    # We can query by query_string or match on cpf / parte / nome
    query = {
        "query": {
            "bool": {
                "should": [
                    {"query_string": {"query": f'"{cpf}"'}},
                    {"query_string": {"query": f'"{cpf_formatted}"'}},
                    {"query_string": {"query": f'"{nome}"'}},
                    {"query_string": {"query": '"Ecildo"'}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 100
    }
    
    data = json.dumps(query).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            print(f"Tribunal {tb.upper()}: {len(hits)} processo(s) encontrado(s).")
            results_by_tribunal[tb] = hits
    except Exception as e:
        print(f"Erro em {tb}: {e}")

output_file = r"c:\Projetos\Super Analista Jurídico\scripts\ecildo_datajud_search.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results_by_tribunal, f, ensure_ascii=False, indent=2)

print(f"\nResultados salvos em {output_file}")
