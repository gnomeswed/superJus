# -*- coding: utf-8 -*-
"""
SUPERJUS — VARREDURA COMPLETA DE 2ª E 3ª INSTÂNCIA: LEANDRO DA SILVA & CORRÉUS
Pesquisa exaustiva por HC, RHC, Apelação e Recursos em:
- TJRJ 2ª Instância (Câmaras Criminais)
- STJ (Superior Tribunal de Justiça)
- STF (Supremo Tribunal Federal)
"""

import sys, json, ssl, urllib.request
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}

cpf_leandro = "05983012754"
proc_origem_limpo = "08272332320268190001"
proc_origem_fmt = "0827233-23.2026.8.19.0001"

partes = [
    ("Leandro da Silva", "05983012754"),
    ("Ryan Ferreira Venceslau", "20517113724"),
    ("Reinaldo Venceslau dos Santos", "10059399775"),
    ("Joao Clayton de Jesus Ferreira", "")
]

endpoints = [
    ("TJRJ (1ª e 2ª Instâncias)", "api_publica_tjrj"),
    ("STJ (3ª Instância)", "api_publica_stj"),
    ("STF (Corte Constitucional)", "api_publica_stf")
]

print("=" * 85)
print(f"🔍 VARREDURA DE RECURSOS, HCs E PROCESSOS EM 2ª E 3ª INSTÂNCIA")
print(f"⚖️ Processo de Origem: {proc_origem_fmt} (1ª Vara Criminal de Santa Cruz)")
print(f"⏰ Consulta: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print("=" * 85)

ctx = ssl._create_unverified_context()

# 1. Pesquisa pelo número do processo de origem citado como processo vinculado / referência
print("\n[FASE 1] Buscando feitos que referenciam o processo de origem (0827233-23.2026)...")
for ep_label, ep_name in endpoints:
    url = f"https://api-publica.datajud.cnj.jus.br/{ep_name}/_search"
    query = {
        "query": {
            "query_string": {
                "query": f'"{proc_origem_limpo}" OR "{proc_origem_fmt}" OR "0827233"'
            }
        },
        "size": 10
    }
    req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  • {ep_label}: {len(hits)} registro(s) encontrado(s)")
            for h in hits:
                s = h["_source"]
                print(f"    -> Proc: {s.get('numeroProcesso')} | Grau: {s.get('grau')} | Órgão: {s.get('orgaoJulgador', {}).get('nome')} | Classe: {s.get('classe', {}).get('nome')}")
    except Exception as e:
        print(f"  • {ep_label}: Erro ({e})")

# 2. Pesquisa pelo CPF dos 4 réus em 2ª e 3ª Instâncias
print("\n[FASE 2] Buscando por CPF de Leandro e de todos os corréus no TJRJ, STJ e STF...")
for nome, doc in partes:
    if not doc:
        continue
    print(f"\n🔎 Investigando réu: {nome} (CPF: {doc})")
    for ep_label, ep_name in endpoints:
        url = f"https://api-publica.datajud.cnj.jus.br/{ep_name}/_search"
        query = {
            "query": {
                "query_string": {
                    "query": f'"{doc}"'
                }
            },
            "size": 5
        }
        req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=HEADERS)
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                hits = data.get("hits", {}).get("hits", [])
                print(f"  • {ep_label}: {len(hits)} hit(s)")
                for h in hits:
                    s = h["_source"]
                    print(f"    -> Proc: {s.get('numeroProcesso')} | Grau: {s.get('grau')} | Classe: {s.get('classe', {}).get('nome')} | Órgão: {s.get('orgaoJulgador', {}).get('nome')}")
        except Exception as e:
            print(f"  • {ep_label}: Erro ({e})")

# 3. Pesquisa por Nome Exato no TJRJ 2ª Instância (Câmaras Criminais)
print("\n[FASE 3] Buscando por Nome dos Corréus em Câmaras Criminais do TJRJ...")
for nome, _ in partes:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    query = {
        "query": {
            "bool": {
                "must": [
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": nome}},
                    {"match_phrase": {"grau": "G2"}}
                ]
            }
        },
        "size": 5
    }
    req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  • {nome} em Grau 2 (TJRJ): {len(hits)} feito(s)")
            for h in hits:
                s = h["_source"]
                print(f"    -> Proc: {s.get('numeroProcesso')} | Órgão: {s.get('orgaoJulgador', {}).get('nome')} | Classe: {s.get('classe', {}).get('nome')}")
    except Exception as e:
        print(f"  • {nome}: Erro ({e})")

print("\n" + "=" * 85)
print("✅ Varredura concluída.")
print("=" * 85)
