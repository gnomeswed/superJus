# -*- coding: utf-8 -*-
"""
SUPERJUS — CONSULTA COMPLETA AO VIVO: LEANDRO DA SILVA ("LEANDRO MECÂNICO")
Processo: 0827233-23.2026.8.19.0001
Vara: 1ª Vara Criminal da Regional de Santa Cruz
Juíza: Regina Célia Moraes de Freitas
"""

import sys, json, ssl, urllib.request
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

print("=" * 85)
print(f"🔍 AUDITORIA PROCESSUAL EM TEMPO REAL — LEANDRO MECÂNICO")
print(f"⚖️ Processo: 0827233-23.2026.8.19.0001 (1ª Vara Criminal de Santa Cruz)")
print(f"⏰ Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

# 1. Consulta em Câmaras Criminais do TJRJ por Habeas Corpus com corréus
coreus = ["Ryan Ferreira Venceslau", "Reinaldo Venceslau dos Santos", "Joao Clayton de Jesus Ferreira", "Leandro da Silva"]

print("\n[1] Verificando no TJRJ se houve impetração de Habeas Corpus pelos réus...")
for c in coreus:
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    payload = json.dumps({
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": c}},
                    {"match_phrase": {"classe.nome": "Habeas Corpus"}}
                ]
            }
        },
        "size": 5
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    ctx = ssl._create_unverified_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  • {c}: {len(hits)} HC(s) encontrado(s)")
            for h in hits:
                s = h["_source"]
                print(f"    -> HC nº {s.get('numeroProcesso')} | {s.get('orgaoJulgador',{}).get('nome')} | Data: {s.get('dataAjuizamento')}")
    except Exception as e:
        print(f"  • Erro em {c}: {e}")

print("\n" + "=" * 85)
print("✅ Checagem de HCs concluída.")
print("=" * 85)
