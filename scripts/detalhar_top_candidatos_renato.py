# -*- coding: utf-8 -*-
"""
SUPERJUS — DETALHAMENTO DOS 4 PROCESSOS PRINCIPAIS DE FURTO 2026 EM ITAPERUNA
Inspeciona todos os movimentos para identificar o flagrante de Renato Bastos Rocha.
"""

import sys, json, ssl, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

PROCS = [
    ("08029367120268190026", "0802936-71.2026.8.19.0026", "20/06/2026"),
    ("08009144020268190026", "0800914-40.2026.8.19.0026", "20/02/2026"),
    ("08028899720268190026", "0802889-97.2026.8.19.0026", "17/06/2026"),
    ("08000093520268190026", "0800009-35.2026.8.19.0026", "04/01/2026")
]

print("=" * 85)
print("🔍 AUDITORIA PROFUNDA DOS PROCESSOS DE FURTO COM RÉU PRESO EM ITAPERUNA (2026)")
print("=" * 85)

for clean, fmt, dt_aj in PROCS:
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    payload = json.dumps({"query": {"match": {"numeroProcesso": clean}}, "size": 1}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            if hits:
                src = hits[0]["_source"]
                movs = src.get("movimentos", [])
                movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                
                print(f"\n📂 PROCESSO: {fmt}")
                print(f"   📅 Ajuizado em: {dt_aj} | Total de Movimentações: {len(movs)}")
                print(f"   🏛️ Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Classe: {src.get('classe', {}).get('nome')}")
                print("   📜 8 Movimentações Mais Recentes:")
                for m in movs_sorted[:8]:
                    dt = m.get("dataHora", "")[:19].replace("T", " ")
                    nm = m.get("nome", "")
                    comps = m.get("complementosTabelados", [])
                    comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")" if comps else ""
                    print(f"      • {dt} — {nm}{comp_str} [Cód. {m.get('codigo')}]")
    except Exception as e:
        print(f"Erro em {fmt}: {e}")

print("\n" + "=" * 85)
print("✅ Auditoria dos 4 casos concluída.")
print("=" * 85)
