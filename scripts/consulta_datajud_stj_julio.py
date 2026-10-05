# -*- coding: utf-8 -*-
"""Verificação final: sigilo + busca CNJ completo no DataJud."""
import json, urllib.request, ssl, sys

sys.stdout.reconfigure(encoding="utf-8")

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

def safe_urlopen(url, headers, data=None, timeout=20):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return None, str(e).encode()

headers = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}

# 1. Buscar RHC pelo CNJ completo (0029845-67.2026.8.19.0000 -> limpo)
cnj_rhc = "00298456720268190000"
url_stj = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"

print("=== Busca STJ por CNJ completo do RHC ===")
body = json.dumps({"query": {"match": {"numeroProcesso": cnj_rhc}}, "size": 5}).encode()
status, raw = safe_urlopen(url_stj, headers, body)
if status == 200:
    res = json.loads(raw)
    hits = res.get("hits", {}).get("hits", [])
    print(f"Hits: {len(hits)}")
    for hit in hits:
        src = hit["_source"]
        print(f"  • {src.get('numeroProcesso')} | sigilo={src.get('nivelSigilo')} | {src.get('dataHoraUltimaAtualizacao')}")
else:
    print(f"HTTP {status}")

# 2. Buscar com wildcard no final (pode ter variação)
print("\n=== Busca STJ por prefixo 0029845 ===")
body2 = json.dumps({"query": {"wildcard": {"numeroProcesso": "0029845*"}}, "size": 5}).encode()
status2, raw2 = safe_urlopen(url_stj, headers, body2)
if status2 == 200:
    hits2 = json.loads(raw2).get("hits", {}).get("hits", [])
    print(f"Hits: {len(hits2)}")
    for hit in hits2:
        src = hit["_source"]
        print(f"  • {src.get('numeroProcesso')} | sigilo={src.get('nivelSigilo')}")
else:
    print(f"HTTP {status2}")

# 3. Buscar no TJRJ o CNJ completo (pode ter atualização do RHC)
print("\n=== Busca TJRJ por CNJ 0029845 ===")
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
body3 = json.dumps({"query": {"wildcard": {"numeroProcesso": "0029845*"}}, "size": 5}).encode()
status3, raw3 = safe_urlopen(url_tjrj, headers, body3)
if status3 == 200:
    hits3 = json.loads(raw3).get("hits", {}).get("hits", [])
    print(f"Hits: {len(hits3)}")
    for hit in hits3:
        src = hit["_source"]
        print(f"  • {src.get('numeroProcesso')} | sigilo={src.get('nivelSigilo')} | atualização={src.get('dataHoraUltimaAtualizacao')}")
        movs = src.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        for m in movs_sorted[:5]:
            print(f"      - {m.get('dataHora','')[:19]} | {m.get('nome','')}")
else:
    print(f"HTTP {status3}")
