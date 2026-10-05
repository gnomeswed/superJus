# -*- coding: utf-8 -*-
"""
Teste de queries flexíveis no DataJud CNJ
"""
import json
import urllib.request

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

def q(endpoint, payload):
    url = f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search"
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 1. Processo Principal Atual
r1 = q("api_publica_tjrj", {"query": {"match": {"numeroProcesso": "00118579520248190002"}}, "size": 5})
hits1 = r1.get('hits', {}).get('hits', [])
print(f"DataJud por Número (0011857-95.2024): {len(hits1)} hits")
for h in hits1:
    s = h['_source']
    print(f"  Processo: {s.get('numeroProcesso')} | Órgão: {s.get('orgaoJulgador', {}).get('nome')} | Classe: {s.get('classe', {}).get('nome')} | Movs: {len(s.get('movimentos', []))}")
    print(f"  Partes:")
    for p in s.get('partes', []):
        print(f"    - {p.get('nome')} ({p.get('tipoPessoa')})")

# 2. Processo 2017
r2 = q("api_publica_tjrj", {"query": {"match": {"numeroProcesso": "00002537820178190004"}}, "size": 5})
hits2 = r2.get('hits', {}).get('hits', [])
print(f"\nDataJud por Número (2017 - 0000253-78): {len(hits2)} hits")
for h in hits2:
    s = h['_source']
    print(f"  Processo: {s.get('numeroProcesso')} | Órgão: {s.get('orgaoJulgador', {}).get('nome')} | Classe: {s.get('classe', {}).get('nome')}")

# 3. Query string por LUCAS DE SOUZA FREITAS
r3 = q("api_publica_tjrj", {
    "query": {
        "query_string": {
            "query": "\"LUCAS DE SOUZA FREITAS\" OR \"Lucas de Souza Freitas\""
        }
    },
    "size": 20
})
hits3 = r3.get('hits', {}).get('hits', [])
print(f"\nDataJud Query String 'LUCAS DE SOUZA FREITAS': {len(hits3)} hits")
for h in hits3:
    s = h['_source']
    print(f"  Processo: {s.get('numeroProcesso')} | Órgão: {s.get('orgaoJulgador', {}).get('nome')} | Classe: {s.get('classe', {}).get('nome')}")

# 4. Query string por LUCAS AND NITEROI AND 2019
r4 = q("api_publica_tjrj", {
    "query": {
        "query_string": {
            "query": "LUCAS AND FREITAS AND Niteroi AND (2019 OR 2018 OR 2020)"
        }
    },
    "size": 20
})
hits4 = r4.get('hits', {}).get('hits', [])
print(f"\nDataJud Query String 'LUCAS FREITAS NITEROI 2018-2020': {len(hits4)} hits")
for h in hits4:
    s = h['_source']
    print(f"  Processo: {s.get('numeroProcesso')} | Órgão: {s.get('orgaoJulgador', {}).get('nome')} | Classe: {s.get('classe', {}).get('nome')}")
