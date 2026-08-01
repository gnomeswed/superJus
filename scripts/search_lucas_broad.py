# -*- coding: utf-8 -*-
import json
import urllib.request

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

queries = [
    {"query": {"query_string": {"query": "\"Lucas de Souza Freitas\""}}, "size": 30},
    {"query": {"match": {"movimentos.complementosTabelados.descricao": "Lucas de Souza Freitas"}}, "size": 30}
]

for idx, q in enumerate(queries, start=1):
    print(f"=== Query {idx} ===")
    req = urllib.request.Request(url, data=json.dumps(q).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            print(f"Total encontrado: {len(hits)}")
            for h in hits:
                src = h['_source']
                num = src.get('numeroProcesso', '')
                classe = src.get('classe', {}).get('nome', '')
                orgao = src.get('orgaoJulgador', {}).get('nome', '')
                dt = src.get('dataAjuizamento', '')
                print(f" - {num} | {classe} | {orgao} | Data: {dt}")
    except Exception as e:
        print(f"Erro na query {idx}: {e}")
