# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

print("=== BUSCANDO EXECUÇÃO PENAL / VEP: RODRIGO DOS REIS NÓBREGA ===")

query_vep = {
    "query": {
        "bool": {
            "should": [
                {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": "Rodrigo dos Reis Nobrega"}},
                {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": "Rodrigo dos Reis Nóbrega"}},
                {"query_string": {"query": '"Rodrigo dos Reis Nobrega"'}},
                {"query_string": {"query": '"Rodrigo dos Reis Nóbrega"'}},
                {"query_string": {"query": '"0800060-52.2023.8.19.0058"'}},
                {"query_string": {"query": '"0800262-29.2023.8.19.0058"'}}
            ],
            "minimum_should_match": 1
        }
    },
    "size": 20
}

try:
    req = urllib.request.Request(url_tjrj, data=json.dumps(query_vep).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"Hits encontrados no TJRJ: {len(hits)}")
        for h in hits:
            src = h["_source"]
            np = src.get("numeroProcesso")
            orgao = src.get("orgaoJulgador", {}).get("nome")
            classe = src.get("classe", {}).get("nome")
            grau = src.get("grau")
            dt = src.get("dataAjuizamento")
            print(f"  • Proc: {np} | Grau: {grau} | Órgão: {orgao} | Classe: {classe} | Data: {dt}")
except Exception as e:
    print(f"Erro: {e}")
