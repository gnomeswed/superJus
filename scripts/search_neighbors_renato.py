# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

tribunais = [
    ("TJES", "https://api-publica.datajud.cnj.jus.br/api_publica_tjes/_search"),
    ("TRF2", "https://api-publica.datajud.cnj.jus.br/api_publica_trf2/_search"),
    ("TJMG", "https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search")
]

headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q = {
    "query": {
        "bool": {
            "should": [
                {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": "Renato Bastos Rocha"}},
                {"query_string": {"query": '"Renato Bastos Rocha"'}}
            ],
            "minimum_should_match": 1
        }
    },
    "size": 20
}

for sigla, url in tribunais:
    print(f"\n--- Consultando {sigla} ---")
    try:
        req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"[{sigla}] Hits: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                dt = src.get("dataAjuizamento")
                print(f"  📌 {np} | {classe} | {orgao} | {dt}")
    except Exception as e:
        print(f"[{sigla}] Erro: {e}")
