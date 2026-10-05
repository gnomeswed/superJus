# -*- coding: utf-8 -*-
"""DataJud: movimentos recentes do processo de Búzios 0023013-51.2021.8.19.0078"""
import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
headers = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

def safe_urlopen(url, headers, body, timeout=30):
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except Exception as e:
        return None, f"Erro: {e}"

# CNJ sem pontuação
cnj = "00230135120218190078"
body = json.dumps({"query": {"match": {"numeroProcesso": cnj}}, "size": 10}).encode()
status, raw = safe_urlopen(url_tjrj, headers, body)
print(f"=== DataJud TJRJ {cnj} status={status} ===")
if status == 200:
    data = json.loads(raw)
    hits = data.get("hits", {}).get("hits", [])
    print(f"Hits: {len(hits)}")
    for h in hits[:3]:
        src = h.get("_source", {})
        print(f"  CNJ: {src.get('numeroProcesso')} | atualização: {src.get('dataAtualizacao')}")
        movs = src.get("movimentos", [])
        print(f"  Movimentos: {len(movs)}")
        for m in movs[-15:]:
            print(f"    {m.get('dataHora','')[:10]} | {m.get('nome','')} | {m.get('complemento','')}")
else:
    print(raw[:1500])
