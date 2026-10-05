# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

# Test multiple queries on TJRJ, TJSP, TJMT, TRF2
tribunais = ["tjrj", "tjsp", "tjmg", "tjmt", "trf2", "stj"]

patterns = [
    "*Melquisedeque*",
    "*Melquisedec*",
    "*Melkisedeque*",
    "Melquisedeque",
    "Melquisedec"
]

print("=== TESTANDO CONSULTAS AVANÇADAS NO DATAJUD ===")

for tb in tribunais:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
    
    # Query with wildcard and match
    query = {
        "query": {
            "bool": {
                "should": [
                    {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": {"value": "*Melquisedeque*", "case_insensitive": True}}},
                    {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": {"value": "*Melquisedec*", "case_insensitive": True}}},
                    {"query_string": {"query": "*Melquisedeque*"}},
                    {"query_string": {"query": "*Melquisedec*"}},
                    {"match": {"dadosBasicos.polo.parte.pessoa.nome": "Melquisedeque"}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 15
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"[{tb.upper()}] Encontrados: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                print(f"   • Proc: {np} | Classe: {classe} | Órgão: {orgao}")
    except Exception as e:
        print(f"[{tb.upper()}] Erro: {e}")
