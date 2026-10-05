# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys

sys.stdout.reconfigure(encoding="utf-8")

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

print("=== BUSCA POR DANIEL FERREIRA LIMA NO DATAJUD TJRJ ===")
payload = json.dumps({
    "query": {
        "bool": {
            "must": [
                {"match_phrase": {"dadosBasicos.poloPassivo.nome": "Daniel Ferreira Lima"}}
            ]
        }
    },
    "size": 10
}).encode("utf-8")

req = urllib.request.Request(BASE_TJRJ, data=payload, headers=HEADERS)
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        hits = res.get("hits", {}).get("hits", [])
        print(f"Hits por poloPassivo: {len(hits)}")
        for h in hits:
            src = h["_source"]
            print(f"Proc: {src.get('numeroProcesso')} | Grau: {src.get('grau')} | Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Classe: {src.get('classe', {}).get('nome')}")
except Exception as e:
    print(f"Erro: {e}")

payload2 = json.dumps({
    "query": {
        "match_phrase": {"pessoas.nome": "Daniel Ferreira Lima"}
    },
    "size": 10
}).encode("utf-8")
req2 = urllib.request.Request(BASE_TJRJ, data=payload2, headers=HEADERS)
try:
    with urllib.request.urlopen(req2) as resp:
        res = json.loads(resp.read().decode("utf-8"))
        hits = res.get("hits", {}).get("hits", [])
        print(f"\nHits por pessoas.nome: {len(hits)}")
        for h in hits:
            src = h["_source"]
            print(f"Proc: {src.get('numeroProcesso')} | Grau: {src.get('grau')} | Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Classe: {src.get('classe', {}).get('nome')}")
except Exception as e:
    print(f"Erro 2: {e}")
