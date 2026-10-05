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
                    "match_phrase": {
                        "dadosBasicos.polo.parte.pessoa.nome": "Rodrigo Duarte de Souza"
                    }
                }
            ]
        }
    },
    "size": 30
}

# Also try query_string
payload_qs = {
    "query": {
        "query_string": {
            "query": "\"Rodrigo Duarte de Souza\""
        }
    },
    "size": 30
}

print("Consultando DataJud para 'Rodrigo Duarte de Souza'...", flush=True)

try:
    req = urllib.request.Request(url, data=json.dumps(payload_qs).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        hits = data.get('hits', {}).get('hits', [])
        print(f"Total encontrados: {len(hits)}", flush=True)
        for h in hits:
            src = h.get('_source', {})
            num = src.get('numeroProcesso')
            classe = src.get('classe', {}).get('nome')
            orgao = src.get('orgaoJulgador', {}).get('nome')
            data_ajuizamento = src.get('dataAjuizamento')
            assuntos = [a.get('nome') for a in src.get('assuntos', [])]
            print(f"Processo: {num} | Órgão: {orgao} | Classe: {classe} | Data: {data_ajuizamento} | Assuntos: {assuntos}", flush=True)
except Exception as e:
    print(f"Erro na consulta: {e}", flush=True)
