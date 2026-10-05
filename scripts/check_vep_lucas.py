# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

nome_cliente = "Lucas de Souza Freitas"
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

print("=== CONSULTA DATAJUD — VARA DE EXECUÇÕES PENAIS (VEP / SEEU) ===")

payloads = [
    {"query": {"bool": {"must": [{"match_phrase": {"partes.nome": nome_cliente}}]}}, "size": 20},
    {"query": {"bool": {"must": [{"match": {"orgaoJulgador.nome": "Vara de Execucoes Penais"}}, {"match_phrase": {"partes.nome": nome_cliente}}]}}, "size": 20}
]

for idx, p in enumerate(payloads, start=1):
    print(f"\n--- Teste {idx} ---")
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    req_data = json.dumps(p).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            print(f"Total de acertos no Datajud TJRJ: {len(hits)}")
            for h in hits:
                src = h['_source']
                num = src.get('numeroProcesso')
                orgao = src.get('orgaoJulgador', {}).get('nome')
                classe = src.get('classe', {}).get('nome')
                dt = src.get('dataHoraUltimaAtualizacao')
                print(f"  • Processo: {num} | Órgão: {orgao} | Classe: {classe} | Atualizado: {dt}")
    except Exception as e:
        print(f"Erro no teste {idx}: {e}")

