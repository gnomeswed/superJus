# -*- coding: utf-8 -*-
"""
Consulta HCs do Dr. Gabriel Alves Guimarães (OAB/RJ 203.902)
e estatísticas de tempo de decisão de Ministros no STJ.
"""
import urllib.request
import json
import sys
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

print("=" * 70)
print("🔍 1. DATAJUD STJ - BUSCA POR GABRIEL ALVES GUIMARÃES")
print("=" * 70)

queries = [
    {"query": {"match_phrase": {"pessoas.nome": "Gabriel Alves Guimarães"}}, "size": 30},
    {"query": {"match_phrase": {"pessoas.nome": "Gabriel Alves Guimaraes"}}, "size": 30},
    {"query": {"match": {"pessoas.nome": "Gabriel Alves Guimaraes"}}, "size": 30},
]

stj_hits = []
seen_procs = set()

for q in queries:
    try:
        url = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
        req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            for h in hits:
                p_num = h["_source"].get("numeroProcesso")
                if p_num not in seen_procs:
                    seen_procs.add(p_num)
                    stj_hits.append(h["_source"])
    except Exception as e:
        print(f"Erro query DataJud STJ: {e}")

print(f"Total de processos encontrados no STJ DataJud: {len(stj_hits)}")
for p in stj_hits:
    p_num = p.get("numeroProcesso")
    classe = p.get("classe", {}).get("nome")
    orgao = p.get("orgaoJulgador", {}).get("nome")
    pessoas = [pes.get("nome") for pes in p.get("pessoas", [])]
    movs = p.get("movimentos", [])
    print(f"\n• Processo STJ: {p_num} | Classe: {classe} | Órgão: {orgao}")
    print(f"  Pessoas: {pessoas[:4]}")
    print(f"  Total movimentos: {len(movs)}")
    # Ordena movimentos
    movs_s = sorted(movs, key=lambda x: x.get("dataHora", ""), reverse=True)
    for m in movs_s[:6]:
        print(f"    - {m.get('dataHora')[:19]}: {m.get('nome')}")

