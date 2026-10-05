# -*- coding: utf-8 -*-
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}

proc_clean = "08272332320268190001"
proc_fmt = "0827233-23.2026.8.19.0001"

print(f"=== AUDITORIA COMPLETA EM TODAS AS INSTÂNCIAS — LEANDRO DA SILVA ===")
print(f"Processo de Referência: {proc_fmt} (1ª Vara Criminal de Santa Cruz)")

# 1. Checagem TJRJ DataJud (1G e 2G)
print("\n--- 1. TJRJ (Tribunal de Justiça do Rio de Janeiro) ---")
try:
    r = requests.post("https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search", headers=HEADERS, json={
        "query": {"match": {"numeroProcesso": proc_clean}},
        "size": 10
    }, timeout=30)
    if r.status_code == 200:
        hits = r.json().get("hits", {}).get("hits", [])
        print(f"Total de registros encontrados no TJRJ: {len(hits)}")
        for i, h in enumerate(hits):
            src = h["_source"]
            print(f"  [{i+1}] Grau: {src.get('grau')} | Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Classe: {src.get('classe', {}).get('nome')}")
            print(f"      Última Atualização: {src.get('dataHoraUltimaAtualizacao')}")
            movs = sorted(src.get("movimentos", []), key=lambda m: m.get("dataHora", ""), reverse=True)
            print(f"      Total de movimentações: {len(movs)}")
            for m in movs[:3]:
                comps = [f"{c.get('nome')}: {c.get('descricao')}" for c in m.get('complementosTabelados', [])]
                comp_str = f" ({'; '.join(comps)})" if comps else ""
                print(f"        • {m.get('dataHora','')[:19].replace('T', ' ')}: {m.get('nome','')}{comp_str}")
    else:
        print(f"Status HTTP TJRJ: {r.status_code}")
except Exception as e:
    print(f"Erro na consulta TJRJ: {e}")

# 2. Checagem STJ DataJud
print("\n--- 2. STJ (Superior Tribunal de Justiça) ---")
try:
    r_stj = requests.post("https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search", headers=HEADERS, json={
        "query": {"match": {"numeroProcesso": proc_clean}},
        "size": 5
    }, timeout=30)
    if r_stj.status_code == 200:
        hits_stj = r_stj.json().get("hits", {}).get("hits", [])
        print(f"Registros encontrados no STJ com o número originário: {len(hits_stj)}")
        for i, h in enumerate(hits_stj):
            src = h["_source"]
            print(f"  [{i+1}] Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Classe: {src.get('classe', {}).get('nome')}")
    else:
        print(f"Status HTTP STJ: {r_stj.status_code}")
except Exception as e:
    print(f"Erro na consulta STJ: {e}")

# 3. Busca por Habeas Corpus dos Corréus ou Leandro no TJRJ
print("\n--- 3. Busca de HCs no TJRJ vinculados à comarca de Santa Cruz / Leandro ---")
try:
    r_hc = requests.post("https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search", headers=HEADERS, json={
        "query": {
            "bool": {
                "must": [
                    {"match": {"classe.codigo": 307}},  # Habeas Corpus Criminal
                    {"query_string": {"query": "\"Santa Cruz\" AND (\"Leandro da Silva\" OR \"Ryan Ferreira Venceslau\" OR \"Reinaldo Venceslau\" OR \"0827233\")", "default_field": "*"}}
                ]
            }
        },
        "size": 5
    }, timeout=30)
    if r_hc.status_code == 200:
        hits_hc = r_hc.json().get("hits", {}).get("hits", [])
        print(f"HCs correlacionados encontrados: {len(hits_hc)}")
        for h in hits_hc:
            src = h["_source"]
            print(f"  • HC: {src.get('numeroProcesso')} | Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Data: {src.get('dataAjuizamento')}")
    else:
        print(f"Status HTTP busca HC: {r_hc.status_code}")
except Exception as e:
    print(f"Erro na busca de HC: {e}")

print("\n=== AUDITORIA FINALIZADA ===")
