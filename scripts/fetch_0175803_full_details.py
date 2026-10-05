# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== DETALHAMENTO COMPLETO DO PROCESSO 0175803-86.2023.8.19.0001 ===")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "01758038620238190001"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        for idx, hit in enumerate(hits, start=1):
            src = hit['_source']
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
            movs = src.get('movimentos', [])
            pessoas = src.get('pessoas', [])
            
            print(f"\n============================================================")
            print(f"📌 INSTÂNCIA / REGISTRO #{idx}")
            print(f"Processo: {src.get('numeroProcesso')}")
            print(f"Órgão Julgador: {orgao}")
            print(f"Classe Processual: {classe}")
            print(f"Última Atualização: {dt_at}")
            print(f"Total de Movimentos: {len(movs)}")
            
            if pessoas:
                print("\nPARTES ENVOLVIDAS:")
                for p in pessoas:
                    print(f"  • [{p.get('polo')}] {p.get('nome')} ({p.get('tipoPessoa')})")
            
            movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
            print(f"\nÚLTIMAS MOVIMENTAÇÕES:")
            for i, m in enumerate(movs_sorted[:25], start=1):
                dt = m.get('dataHora', '')[:19].replace('T', ' ')
                nome_mov = m.get('nome', '')
                code = m.get('codigo', '')
                comps = m.get('complementosTabelados', [])
                comp_str = ""
                if comps:
                    comp_str = " -> " + " | ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps])
                print(f"  {i:02d}. {dt} | {nome_mov}{comp_str} [Cód: {code}]")

except Exception as e:
    print(f"Erro: {e}")

print("\n=== CONSULTA FINALIZADA ===")
