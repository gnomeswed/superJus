# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import os
import sys

headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

nome_busca = "Daniel Ferreira Lima"

def search_ep(ep):
    url = f"https://api-publica.datajud.cnj.jus.br/{ep}/_search"
    payloads = [
        {"query": {"match_phrase": {"polo.parte.pessoa.nome": nome_busca}}, "size": 10},
        {"query": {"match_phrase": {"partes.nome": nome_busca}}, "size": 10},
        {"query": {"query_string": {"query": f'"{nome_busca}"'}}, "size": 10}
    ]
    for p in payloads:
        try:
            req_data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(url, data=req_data, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                hits = data.get('hits', {}).get('hits', [])
                if hits:
                    return hits
        except Exception as e:
            pass
    return []

endpoints = [
    ("api_publica_tjrj", "TJRJ"),
    ("api_publica_stj", "STJ"),
    ("api_publica_stf", "STF"),
    ("api_publica_tjsp", "TJSP"),
    ("api_publica_trf2", "TRF2")
]

results = {}

for ep, name in endpoints:
    print(f"Buscando {name}...", flush=True)
    hits = search_ep(ep)
    print(f"--> {name}: {len(hits)} resultados", flush=True)
    if hits:
        results[name] = []
        for h in hits:
            src = h['_source']
            results[name].append({
                "numeroProcesso": src.get('numeroProcesso'),
                "classe": src.get('classe', {}).get('nome'),
                "orgaoJulgador": src.get('orgaoJulgador', {}).get('nome'),
                "dataAjuizamento": src.get('dataAjuizamento'),
                "dataHoraUltimaAtualizacao": src.get('dataHoraUltimaAtualizacao'),
                "assuntos": [a.get('nome') for a in src.get('assuntos', [])],
                "movimentos": src.get('movimentos', [])[:5]
            })

with open("daniel_results_fast.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("CONCLUIDO", flush=True)
