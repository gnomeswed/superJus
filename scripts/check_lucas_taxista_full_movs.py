# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

print("=== DETALHAMENTO DE MOVIMENTAÇÕES — LUCAS TAXISTA (0808595-36.2026.8.19.0002) ===")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "08085953620268190002"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        for hit in hits:
            src = hit['_source']
            movs = src.get('movimentos', [])
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"Total de movimentações: {len(movs)}\n")
            for i, m in enumerate(movs_sorted[:30], start=1):
                dt = m.get('dataHora', '')[:19].replace('T', ' ')
                nome = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = ""
                if comps:
                    comp_str = " -> " + " | ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps])
                print(f"{i:02d}. {dt} | {nome}{comp_str} [Cód: {code}]")
except Exception as e:
    print(f"Erro: {e}")
