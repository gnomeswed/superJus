# -*- coding: utf-8 -*-
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}

tjs = ["tjrj", "tjsp", "tjmg", "tjba", "tjce", "tjpe", "tjpr", "tjrs", "tjgo", "tjmt", "tjms", "tjdf", "stj"]

print("=== BUSCA DATAJUD COM DEFAULT_FIELD: * ===")

for tj in tjs:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tj}/_search"
    payload = {
        "query": {
            "query_string": {
                "query": "\"Daniel Ferreira Lima\"",
                "default_field": "*"
            }
        },
        "size": 10
    }
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=6)
        if r.status_code == 200:
            hits = r.json().get("hits", {}).get("hits", [])
            total = r.json().get("hits", {}).get("total", {})
            if hits:
                print(f"\n[!] ENCONTRADO NO {tj.upper()}! Total: {total}")
                for h in hits:
                    src = h["_source"]
                    num = src.get("numeroProcesso")
                    classe = src.get("classe", {}).get("nome")
                    orgao = src.get("orgaoJulgador", {}).get("nome")
                    assuntos = [a.get("nome") for a in src.get("assuntos", [])]
                    print(f"  - {num} | {classe} | {orgao} | Assuntos: {assuntos}")
    except Exception as e:
        # print(f"Erro em {tj}: {e}")
        pass
