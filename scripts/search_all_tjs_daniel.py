# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import sys

headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

nome_busca = "Daniel Ferreira Lima"

tjs = [
    "tjrj", "tjsp", "tjmg", "tjrs", "tjpr", "tjba", "tjpe", "tjce", 
    "tjgo", "tjma", "tjmt", "tjms", "tjes", "tjdf", "tjsc", "tjpa",
    "tjpb", "tjpi", "tjrn", "tjal", "tjse", "tjam", "tjro", "tjrr",
    "tjac", "tjap", "tjto"
]

results = {}

for tj in tjs:
    ep = f"api_publica_{tj}"
    url = f"https://api-publica.datajud.cnj.jus.br/{ep}/_search"
    payload = {
        "query": {
            "query_string": {
                "query": f'"{nome_busca}"'
            }
        },
        "size": 10
    }
    try:
        req_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=req_data, headers=headers)
        with urllib.request.urlopen(req, timeout=4) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            if hits:
                print(f"ENCONTRADO NO {tj.upper()}: {len(hits)} processos!", flush=True)
                results[tj.upper()] = []
                for h in hits:
                    src = h['_source']
                    results[tj.upper()].append({
                        "numeroProcesso": src.get('numeroProcesso'),
                        "classe": src.get('classe', {}).get('nome'),
                        "orgaoJulgador": src.get('orgaoJulgador', {}).get('nome'),
                        "dataAjuizamento": src.get('dataAjuizamento'),
                        "dataHoraUltimaAtualizacao": src.get('dataHoraUltimaAtualizacao'),
                        "assuntos": [a.get('nome') for a in src.get('assuntos', [])],
                        "movimentos": src.get('movimentos', [])[:5]
                    })
    except Exception as e:
        pass

with open("daniel_all_tjs_result.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("VARREDURA NACIONAL DATAJUD CONCLUIDA", flush=True)
