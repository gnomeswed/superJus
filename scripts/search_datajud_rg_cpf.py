# -*- coding: utf-8 -*-
import json
import urllib.request

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

queries = [
    {"numeroProcesso": "00002537820178190004"},
    {"numeroProcesso": "00464189820178190000"},
    {"query_string": {"query": "\"Lucas de Souza Freitas\""}}
]

for idx, q in enumerate(queries, 1):
    req_data = json.dumps({"query": {"match" if "numeroProcesso" in q else "query_string": q}, "size": 100}).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            print(f"=== QUERY {idx} ({q}): {len(hits)} RESULTADOS ===")
            for h in hits:
                src = h['_source']
                n_proc = src.get('numeroProcesso')
                polos = src.get('polo', [])
                print(f"Processo: {n_proc} | Classe: {src.get('classe', {}).get('nome')}")
                for p in polos:
                    for pt in p.get('parte', []):
                        pess = pt.get('pessoa', {})
                        print(f"   Parte: {pess.get('nome')} | Doc: {pess.get('tipoDocumento')} {pess.get('numeroDocumentoPrincipal')}")
    except Exception as e:
        print(f"Erro na query {idx}: {e}")
