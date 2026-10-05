# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q = {"query": {"match": {"numeroProcesso": "03112101020263000000"}}}

req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
with urllib.request.urlopen(req, timeout=12) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    hits = data.get("hits", {}).get("hits", [])
    if hits:
        stj_data = hits[0]["_source"]
        out_path = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\stj_datajud_full_29ago.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(stj_data, f, ensure_ascii=False, indent=2)
        print(f"Salvo STJ JSON com {len(stj_data.get('movimentos', []))} movimentos em {out_path}")
