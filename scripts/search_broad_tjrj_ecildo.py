# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
cpf = "08073097290"
cpf_formatted = "080.730.972-90"
nome = "Ecildo Victor dos Santos Ferreira"

print("=== BUSCA AMPLA NO TJRJ (DATAJUD) ===")
url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

queries = [
    {"query_string": {"query": f'"{cpf}"'}},
    {"query_string": {"query": f'"{cpf_formatted}"'}},
    {"query_string": {"query": '"Ecildo Victor"'}},
    {"query_string": {"query": '"Ecildo"'}},
    {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": "*Ecildo*"}}
]

for idx, q in enumerate(queries):
    body = {"query": q, "size": 20}
    req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"Query {idx+1}: {len(hits)} hits encontrados no TJRJ.")
            for h in hits:
                src = h["_source"]
                print(f"  Proc: {src.get('numeroProcesso')} | Classe: {src.get('classe', {}).get('nome')} | Orgão: {src.get('orgaoJulgador', {}).get('nome')}")
                for m in src.get('movimentos', []):
                    if 'audiên' in m.get('nome', '').lower() or 'custódia' in m.get('nome', '').lower():
                        print(f"    -> {m.get('dataHora')} | {m.get('nome')}")
    except Exception as e:
        print(f"Query {idx+1} erro: {e}")
