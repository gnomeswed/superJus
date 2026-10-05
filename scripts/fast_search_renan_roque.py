# -*- coding: utf-8 -*-
import json, urllib.request, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core.config import datajud_headers

sys.stdout.reconfigure(encoding="utf-8")

endpoints = [
    ("api_publica_tjrj", "TJRJ"),
    ("api_publica_stj", "STJ"),
    ("api_publica_tjsp", "TJSP"),
    ("api_publica_trf2", "TRF2")
]

termo = "Renan Roque"
print(f"=== BUSCA GLOBAL DATAJUD POR '{termo}' ===")

headers = datajud_headers()

for ep, name in endpoints:
    url = f"https://api-publica.datajud.cnj.jus.br/{ep}/_search"
    p = {"query": {"query_string": {"query": f'"{termo}"'}}, "size": 5}
    try:
        req = urllib.request.Request(url, data=json.dumps(p).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=12) as r:
            res = json.loads(r.read().decode("utf-8"))
            hits = res.get("hits", {}).get("hits", [])
            print(f"{name}: {len(hits)} processo(s)")
            for h in hits:
                src = h["_source"]
                print(f"  • Proc: {src.get('numeroProcesso')} | {src.get('classe',{}).get('nome')} | {src.get('orgaoJulgador',{}).get('nome')}")
                for p in src.get("pessoas", []):
                    print(f"    - Parte: {p.get('nome')} ({p.get('polo')})")
    except Exception as e:
        print(f"{name} erro: {e}")
