# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

# Query specifically for 08016300420258190026 without specifying grau
q = {"query": {"match": {"numeroProcesso": "08016300420258190026"}}, "size": 10}

req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    hits = data.get("hits", {}).get("hits", [])
    print(f"Total hits para 08016300420258190026: {len(hits)}")
    for h in hits:
        src = h["_source"]
        grau = src.get("grau")
        orgao = src.get("orgaoJulgador", {}).get("nome")
        classe = src.get("classe", {}).get("nome")
        dt = src.get("dataAjuizamento")
        movs = src.get("movimentos", [])
        print(f"  Grau: {grau} | Órgão: {orgao} | Classe: {classe} | Movs: {len(movs)}")
