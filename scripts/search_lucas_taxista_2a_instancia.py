# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

print("=== BUSCA POR NOME NO DATAJUD TJRJ — LUCAS DIAS OLIVEIRA ===")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({
    "query": {
        "match_phrase": {
            "pessoas.nome": "Lucas Dias Oliveira"
        }
    },
    "size": 10
}).encode('utf-8')

req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"\n📌 Encontrados {len(hits)} processos para o nome Lucas Dias Oliveira:")
        for hit in hits:
            src = hit['_source']
            num = src.get('numeroProcesso', 'N/I')
            classe = src.get('classe', {}).get('nome', 'N/I')
            orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
            dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
            movs = src.get('movimentos', [])
            print(f"\n• Processo: {num}")
            print(f"  - Órgão: {orgao}")
            print(f"  - Classe: {classe}")
            print(f"  - Última Atualização: {dt_at}")
            print(f"  - Total de movimentos: {len(movs)}")
            if movs:
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                print("  - Últimas movimentações:")
                for m in movs_sorted[:3]:
                    dt = m.get('dataHora', '')[:19].replace('T', ' ')
                    nome = m.get('nome', '')
                    print(f"    • {dt} | {nome}")
except Exception as e:
    print(f"Erro na busca por nome: {e}")

print("\n=== CONSULTA CONCLUÍDA ===")
