# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
headers = {
    'Authorization': f'APIKey {API_KEY}',
    'Content-Type': 'application/json'
}

url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

payload = {
    "query": {
        "bool": {
            "must": [
                {
                    "wildcard": {
                        "numeroProcesso": "*0078"
                    }
                },
                {
                    "query_string": {
                        "query": "\"Rodrigo Duarte de Souza\""
                    }
                }
            ]
        }
    },
    "size": 10
}

print("Buscando processos de Rodrigo Duarte de Souza em Búzios (DataJud)...", flush=True)

try:
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        hits = data.get('hits', {}).get('hits', [])
        print(f"Total encontrados em Búzios: {len(hits)}", flush=True)
        for h in hits:
            src = h.get('_source', {})
            num = src.get('numeroProcesso')
            classe = src.get('classe', {}).get('nome')
            orgao = src.get('orgaoJulgador', {}).get('nome')
            dt = src.get('dataAjuizamento')
            print(f"-> Processo: {num} | Classe: {classe} | Órgão: {orgao} | Data: {dt}", flush=True)
except Exception as e:
    print(f"Erro DataJud: {e}", flush=True)

# Testar também consulta de números vizinhos a 0023013-51.2021.8.19.0078
vizinhos = [
    "0023011-81.2021.8.19.0078",
    "0023012-66.2021.8.19.0078",
    "0023013-51.2021.8.19.0078",
    "0023014-36.2021.8.19.0078",
    "0023015-21.2021.8.19.0078"
]

print("\nVerificando números vizinhos da distribuição de 2021...", flush=True)
for num in vizinhos:
    p = {
        "query": {
            "match": {
                "numeroProcesso": num.replace("-", "").replace(".", "")
            }
        }
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(p).encode('utf-8'), headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            if hits:
                src = hits[0].get('_source', {})
                partes = []
                for polo in src.get('dadosBasicos', {}).get('polo', []):
                    for pt in polo.get('parte', []):
                        partes.append(pt.get('pessoa', {}).get('nome'))
                print(f"Vizinho {num}: {src.get('classe', {}).get('nome')} | Partes: {partes}", flush=True)
    except Exception as e:
        pass
