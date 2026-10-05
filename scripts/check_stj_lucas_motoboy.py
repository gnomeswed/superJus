# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url_stj = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

q = {
    "query": {
        "bool": {
            "should": [
                {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": "Lucas de Souza Freitas"}},
                {"query_string": {"query": '"0011857-95.2024.8.19.0002"'}}
            ],
            "minimum_should_match": 1
        }
    },
    "size": 10
}

print("=== VERIFICANDO SE HÁ HC OU RECURSO NO STJ PARA LUCAS MOTOBOY ===")
try:
    req = urllib.request.Request(url_stj, data=json.dumps(q).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"Hits no STJ: {len(hits)}")
        for h in hits:
            src = h["_source"]
            np = src.get("numeroProcesso")
            classe = src.get("classe", {}).get("nome")
            orgao = src.get("orgaoJulgador", {}).get("nome")
            dt = src.get("dataAjuizamento")
            print(f"  📌 STJ: {np} | {classe} | {orgao} | {dt}")
except Exception as e:
    print(f"Erro: {e}")
