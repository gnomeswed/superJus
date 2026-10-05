# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFICAÇÃO EM TEMPO REAL — 04/08/2026 18:36 ===")

headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

# 1. Check TJRJ processes
tjrj_procs = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal Desmembrada - 2ª Vara Búzios"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "HC TJRJ - 7ª Câmara Criminal"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Principal - 2ª Vara Búzios")
]

url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

for formatted, clean, label in tjrj_procs:
    req_data = json.dumps({"query": {"match": {"numeroProcesso": clean}}, "size": 5}).encode('utf-8')
    req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)
    print(f"\n📌 {label} [{formatted}]:")
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            if not hits:
                print("   Nenhum registro retornado.")
            for hit in hits:
                src = hit['_source']
                orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
                dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
                movs = src.get('movimentos', [])
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                print(f"   • Órgão: {orgao}")
                print(f"   • Última Atualização no Datajud: {dt_at}")
                print(f"   • Últimas 3 movimentações:")
                for m in movs_sorted[:3]:
                    dt = m.get('dataHora', '')[:19].replace('T', ' ')
                    nome = m.get('nome', '')
                    print(f"     - {dt} | {nome}")
    except Exception as e:
        print(f"   Erro ao consultar Datajud TJRJ: {e}")

# 2. Check STJ process
url_stj = 'https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search'
stj_procs = [
    ("HC 1.116.750/RJ (2026/0311210-7)", "202603112107", "RHC STJ - 6ª Turma (Rel. Min. Og Fernandes)")
]

for formatted, clean, label in stj_procs:
    print(f"\n📌 {label} [{formatted}]:")
    req_data = json.dumps({"query": {"match": {"numeroProcesso": clean}}, "size": 5}).encode('utf-8')
    req = urllib.request.Request(url_stj, data=req_data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            if not hits:
                # Try query by text if number didn't match directly
                req_data2 = json.dumps({"query": {"query_string": {"query": "Júlio Pereira Marcos"}}, "size": 5}).encode('utf-8')
                req2 = urllib.request.Request(url_stj, data=req_data2, headers=headers)
                with urllib.request.urlopen(req2) as resp2:
                    res2 = json.loads(resp2.read().decode('utf-8'))
                    hits = res2.get('hits', {}).get('hits', [])
            
            if not hits:
                print("   Sem atualizações no Datajud STJ.")
            for hit in hits:
                src = hit['_source']
                num = src.get('numeroProcesso', 'N/I')
                dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
                movs = src.get('movimentos', [])
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                print(f"   • Número: {num}")
                print(f"   • Última Atualização: {dt_at}")
                print(f"   • Últimas movimentações:")
                for m in movs_sorted[:3]:
                    dt = m.get('dataHora', '')[:19].replace('T', ' ')
                    nome = m.get('nome', '')
                    print(f"     - {dt} | {nome}")
    except Exception as e:
        print(f"   Consulta Datajud STJ: {e}")

print("\n=== CHECAGEM CONCLUÍDA ===")
