# -*- coding: utf-8 -*-
import json
import ssl
import sys
import time
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding="utf-8")

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Test DataJud STJ & TJRJ
api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
datajud_headers = {
    "Authorization": f"APIKey {api_key}",
    "Content-Type": "application/json"
}

print("=== 1. Test DataJud STJ ===")
t0 = time.perf_counter()
req = urllib.request.Request(
    "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search",
    data=json.dumps({"query": {"match": {"numeroProcesso": "00298456720268190000"}}, "size": 1}).encode("utf-8"),
    headers=datajud_headers
)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        elapsed = (time.perf_counter() - t0) * 1000
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"DataJud STJ: status {resp.status} in {elapsed:.1f}ms | Hits: {len(hits)}")
        if hits:
            src = hits[0]["_source"]
            print(f"  Processo: {src.get('numeroProcesso')} | Classe: {src.get('classe', {}).get('nome')} | Sigilo: {src.get('nivelSigilo')}")
except Exception as e:
    print(f"DataJud STJ error: {e}")

print("\n=== 2. Test DataJud TJRJ ===")
t0 = time.perf_counter()
req = urllib.request.Request(
    "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search",
    data=json.dumps({"query": {"match": {"numeroProcesso": "00230135120218190078"}}, "size": 1}).encode("utf-8"),
    headers=datajud_headers
)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=8) as resp:
        elapsed = (time.perf_counter() - t0) * 1000
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"DataJud TJRJ: status {resp.status} in {elapsed:.1f}ms | Hits: {len(hits)}")
        if hits:
            src = hits[0]["_source"]
            print(f"  Processo: {src.get('numeroProcesso')} | Classe: {src.get('classe', {}).get('nome')} | Movimentos: {len(src.get('movimentos', []))}")
except Exception as e:
    print(f"DataJud TJRJ error: {e}")

print("\n=== 3. Test TJRJ Direct REST API ===")
tjrj_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www3.tjrj.jus.br",
    "Referer": "https://www3.tjrj.jus.br/consultaprocessual/"
}

t0 = time.perf_counter()
req = urllib.request.Request(
    "https://www3.tjrj.jus.br/consultaprocessual/api/processos/por-numeracao-unica",
    data=json.dumps({"tipoProcesso": "1", "codigoProcesso": "0023013-51.2021.8.19.0078"}).encode("utf-8"),
    headers=tjrj_headers
)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        elapsed = (time.perf_counter() - t0) * 1000
        raw = resp.read().decode("utf-8", errors="ignore")
        print(f"TJRJ por-numeracao-unica: status {resp.status} in {elapsed:.1f}ms")
        print(f"  Response: {raw[:300]}")
except urllib.error.HTTPError as e:
    print(f"TJRJ por-numeracao-unica HTTPError {e.code}: {e.reason}")
    print(f"  Body: {e.read()[:300]}")
except Exception as e:
    print(f"TJRJ por-numeracao-unica error: {e}")

print("\n=== 4. Test STJ Processo Web Endpoint ===")
t0 = time.perf_counter()
stj_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}
req = urllib.request.Request(
    "https://processo.stj.jus.br/processo/pesquisa/?tipoPesquisa=tipoPesquisaNumeroRegistro&termo=202603112107&totalRegistrosPorPagina=40&aplicacao=processos.ea",
    headers=stj_headers
)
try:
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        elapsed = (time.perf_counter() - t0) * 1000
        raw = resp.read().decode("utf-8", errors="ignore")
        print(f"STJ Web Pesquisa: status {resp.status} in {elapsed:.1f}ms | HTML size: {len(raw)} bytes")
        if "HC 1116750" in raw or "1116750" in raw or "JULIO" in raw.upper():
            print("  ✓ HC 1116750 / Júlio encontrado no HTML retornado!")
except Exception as e:
    print(f"STJ Web error: {e}")
