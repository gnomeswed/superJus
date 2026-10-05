# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

proc_clean = "00043013320188190073"

print("=== CONSULTA COMPLETA DATAJUD — DANIEL FERREIRA LIMA ===")
payload = json.dumps({
    "query": {"match": {"numeroProcesso": proc_clean}},
    "size": 10
}).encode("utf-8")

req = urllib.request.Request(BASE_TJRJ, data=payload, headers=HEADERS)
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    hits = res.get("hits", {}).get("hits", [])
    print(f"Total de instâncias/registros no TJRJ: {len(hits)}\n")
    for i, h in enumerate(hits, 1):
        src = h["_source"]
        grau = src.get("grau")
        orgao = src.get("orgaoJulgador", {}).get("nome")
        classe = src.get("classe", {}).get("nome")
        dt_atualizacao = src.get("dataHoraUltimaAtualizacao")
        movs = src.get("movimentos", [])
        print(f"[{i}] Grau: {grau} | Órgão: {orgao} | Classe: {classe}")
        print(f"    Última atualização no banco: {dt_atualizacao}")
        print(f"    Total de movimentações: {len(movs)}")
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        print("    Top 10 Movimentações mais recentes:")
        for idx, m in enumerate(movs_sorted[:10], 1):
            dt = m.get("dataHora", "")[:19].replace("T", " ")
            nome = m.get("nome", "")
            code = m.get("codigo", "")
            comps = m.get("complementosTabelados", [])
            comp_str = ""
            if comps:
                comp_str = " -> " + " | ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps])
            print(f"      {idx:02d}. {dt} | {nome}{comp_str} [Cód: {code}]")
        print()
