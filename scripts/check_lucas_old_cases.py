# -*- coding: utf-8 -*-
import json
import urllib.request
import re

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

test_procs = [
    "00141744220198190002",
    "00040227120158190002",
    "00310206620218190002",
    "00234341220208190002"
]

for num in test_procs:
    q = {"query": {"match": {"numeroProcesso": num}}, "size": 1}
    req = urllib.request.Request(url, data=json.dumps(q).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            if hits:
                src = hits[0]['_source']
                classe = src.get('classe', {}).get('nome', '')
                orgao = src.get('orgaoJulgador', {}).get('nome', '')
                print(f"=== Processo {num} ===")
                print(f"  Classe: {classe} | Órgão: {orgao}")
                # Imprimir partes / movimentos que mencionem documento / RG / CPF / Lucas
                src_str = json.dumps(src, ensure_ascii=False)
                for l in src_str.split(','):
                    if any(w in l.lower() for w in ['lucas', 'freitas', 'rg', 'cpf', 'alvará', 'soltura']):
                        print("    ->", l.strip()[:140])
    except Exception as e:
        print(f"Erro em {num}: {e}")
