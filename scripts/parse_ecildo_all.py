# -*- coding: utf-8 -*-
import os
import json
import urllib.request
import re

# 1. Query DataJud for TJMT with exact CPF 08073097290 and name Ecildo
DATAJUD_API_KEY = __import__('os').getenv('DATAJUD_API_KEY','')

def search_tjmt():
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjmt/_search"
    headers = {
        "Authorization": DATAJUD_API_KEY,
        "Content-Type": "application/json"
    }
    
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"numeroProcesso": "10035245720238110015"}},
                    {"query_string": {"query": "\"08073097290\""}},
                    {"query_string": {"query": "\"Ecildo Victor\""}}
                ]
            }
        },
        "size": 50
    }
    
    req = urllib.request.Request(url, data=json.dumps(query).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            print(f"DataJud TJMT returned {len(hits)} hits.")
            return hits
    except Exception as e:
        print(f"Error querying DataJud TJMT: {e}")
        return []

hits = search_tjmt()

# Extract process numbers and latest movements / hearings
processes = []
for h in hits:
    src = h.get('_source', {})
    np = src.get('numeroProcesso')
    classe = src.get('classe', {}).get('nome')
    orgao = src.get('orgaoJulgador', {}).get('nome')
    dt_ajuizamento = src.get('dataAjuizamento')
    movs = src.get('movimentos', [])
    
    # Sort movements descending
    movs_sorted = sorted(movs, key=lambda x: x.get('dataHora', ''), reverse=True)
    
    # Check for recent hearings or movements
    hearings = [m for m in movs_sorted if 'audiência' in m.get('nome', '').lower() or 'audiencia' in m.get('nome', '').lower()]
    
    processes.append({
        "numeroProcesso": np,
        "classe": classe,
        "orgaoJulgador": orgao,
        "dataAjuizamento": dt_ajuizamento,
        "total_movimentacoes": len(movs),
        "ultima_movimentacao": movs_sorted[0] if movs_sorted else None,
        "ultimas_5_movs": movs_sorted[:5],
        "audiencias": hearings
    })

print(json.dumps(processes, indent=2, ensure_ascii=False))

with open(r"c:\Projetos\Super Analista Jurídico\scripts\ecildo_parsed_datajud.json", "w", encoding="utf-8") as f:
    json.dump(processes, f, ensure_ascii=False, indent=2)
