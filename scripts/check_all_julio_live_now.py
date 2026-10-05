# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== CHECAGEM DE DADOS — JÚLIO PEREIRA MARCOS ===")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

# 1. HC TJRJ (0029845-67.2026.8.19.0000)
print("\n1. Habeas Corpus TJRJ (0029845-67.2026.8.19.0000):")
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
req_data = json.dumps({"query": {"match": {"numeroProcesso": "00298456720268190000"}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"   • Encontrados {len(hits)} registros no Datajud:")
        for hit in hits:
            src = hit['_source']
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"   • Órgão: {src.get('orgaoJulgador', {}).get('nome')} | Classe: {src.get('classe', {}).get('nome')}")
            print(f"   • Última Atualização no Datajud: {src.get('dataHoraUltimaAtualizacao')}")
            print("   • Últimas 5 movimentações:")
            for m in movs_sorted[:5]:
                dt = m.get('dataHora', '')[:19].replace('T', ' ')
                nome = m.get('nome', '')
                print(f"     - {dt} | {nome}")
except Exception as e:
    print(f"   • Erro HC TJRJ: {e}")

# 2. RHC STJ (Julio Pereira Marcos)
print("\n2. STJ — Recurso Ordinário em HC (Julio Pereira Marcos):")
try:
    url_stj = 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search'
    req_stj = urllib.request.Request(url_stj, data=json.dumps({"query": {"match_phrase": {"pessoas.nome": "Julio Pereira Marcos"}}, "size": 5}).encode('utf-8'), headers=headers)
    with urllib.request.urlopen(req_stj) as resp:
        res_stj = json.loads(resp.read().decode('utf-8'))
        hits_stj = res_stj.get('hits', {}).get('hits', [])
        print(f"   • Encontrados {len(hits_stj)} registros no STJ Datajud:")
        for h in hits_stj:
            src = h['_source']
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"   • STJ Processo: {src.get('numeroProcesso')} | Classe: {src.get('classe', {}).get('nome')}")
            print(f"   • Última Atualização no Datajud: {src.get('dataHoraUltimaAtualizacao')}")
            print("   • Últimas 5 movimentações:")
            for m in movs_sorted[:5]:
                dt = m.get('dataHora', '')[:19].replace('T', ' ')
                nome = m.get('nome', '')
                print(f"     - {dt} | {nome}")
except Exception as e:
    print(f"   • Erro STJ: {e}")

print("\n=== CHECAGEM CONCLUÍDA ===")
