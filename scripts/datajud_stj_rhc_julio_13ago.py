# -*- coding: utf-8 -*-
"""DataJud STJ: busca pelo numeroRegistro interno 202603112107 (RHC Julio)"""
import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
headers = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
url_stj = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"

def safe_urlopen(url, headers, body, timeout=30):
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return None, f"Erro: {e}"

# Tentativa 1: numeroRegistro interno
for q in ["202603112107", "2026/0311210-7"]:
    body = json.dumps({"query": {"match": {"numeroRegistro": q}}, "size": 10}).encode()
    status, raw = safe_urlopen(url_stj, headers, body)
    print(f"=== DataJud STJ numeroRegistro={q} status={status} ===")
    if status == 200:
        data = json.loads(raw)
        hits = data.get("hits", {}).get("hits", [])
        print(f"Hits: {len(hits)}")
        for h in hits[:3]:
            src = h.get("_source", {})
            print(f"  Registro: {src.get('numeroRegistro')} | CNJ: {src.get('numeroProcesso')}")
            print(f"  Classe: {src.get('classeProcesso',{}).get('nome')} | Órgão: {src.get('orgaoJulgador',{}).get('nome')}")
            print(f"  Relator: {src.get('relator',{}).get('nome')}")
            movs = src.get("movimentos", [])
            print(f"  Movimentos: {len(movs)}")
            for m in movs[-12:]:
                print(f"    {m.get('dataHora','')[:10]} | {m.get('nome','')} | {m.get('complemento','')}")
    else:
        print(raw[:800])
