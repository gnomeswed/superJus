# -*- coding: utf-8 -*-
import json
import urllib.request
import concurrent.futures
import sys

headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

nome_busca = "Daniel Ferreira Lima"

endpoints = [
    "tjrj", "tjsp", "tjmg", "tjrs", "tjpr", "tjba", "tjpe", "tjce", 
    "tjgo", "tjma", "tjmt", "tjms", "tjes", "tjdf", "tjsc", "tjpa",
    "tjpb", "tjpi", "tjrn", "tjal", "tjse", "tjam", "tjro", "tjrr",
    "tjac", "tjap", "tjto", "stj", "stf", "trf1", "trf2", "trf3", "trf4", "trf5", "trf6"
]

results = {}

def query_ep(tj):
    ep = f"api_publica_{tj}"
    url = f"https://api-publica.datajud.cnj.jus.br/{ep}/_search"
    payloads = [
        {"query": {"match_phrase": {"polo.parte.pessoa.nome": nome_busca}}, "size": 10},
        {"query": {"match_phrase": {"partes.nome": nome_busca}}, "size": 10},
        {"query": {"query_string": {"query": f'"{nome_busca}"'}}, "size": 10}
    ]
    found = []
    for p in payloads:
        try:
            req_data = json.dumps(p).encode('utf-8')
            req = urllib.request.Request(url, data=req_data, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                hits = data.get('hits', {}).get('hits', [])
                if hits:
                    for h in hits:
                        src = h['_source']
                        found.append({
                            "tribunal": tj.upper(),
                            "numeroProcesso": src.get('numeroProcesso'),
                            "classe": src.get('classe', {}).get('nome'),
                            "orgaoJulgador": src.get('orgaoJulgador', {}).get('nome'),
                            "dataAjuizamento": src.get('dataAjuizamento'),
                            "dataHoraUltimaAtualizacao": src.get('dataHoraUltimaAtualizacao'),
                            "assuntos": [a.get('nome') for a in src.get('assuntos', [])],
                            "partes": [p.get('nome') for polo in src.get('polo', []) for p in polo.get('parte', []) if isinstance(p, dict)],
                            "ultimos_movimentos": src.get('movimentos', [])[:5]
                        })
                    break
        except Exception as e:
            pass
    return tj.upper(), found

print("Iniciando busca paralela nacional...", flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
    future_to_tj = {executor.submit(query_ep, tj): tj for tj in endpoints}
    for future in concurrent.futures.as_completed(future_to_tj):
        tj, found = future.result()
        if found:
            print(f"ENCONTRADO EM {tj}: {len(found)} processos!", flush=True)
            results[tj] = found

out_path = r"c:\Projetos\superJus\daniel_parallel_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Busca paralela concluída com sucesso!", flush=True)
