# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFICANDO HABEAS CORPUS / RECURSOS PARA LUCAS DIAS OLIVEIRA ===")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

# Search TJRJ for Habeas Corpus or any 2nd instance process matching "Lucas Dias Oliveira"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
query = {
    "query": {
        "match": {
            "numeroProcesso": "08085953620268190002"
        }
    },
    "size": 10
}

req = urllib.request.Request(url_tjrj, data=json.dumps(query).encode('utf-8'), headers=headers)
try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"Total de processos associados na base TJRJ: {len(hits)}")
        for h in hits:
            src = h['_source']
            print(f"  • Processo: {src.get('numeroProcesso')} | Classe: {src.get('classe', {}).get('nome')} | Órgão: {src.get('orgaoJulgador', {}).get('nome')}")
            # Check movements for any mention of HC, Recurso, Mandado de Segurança, Agravo
            movs = src.get('movimentos', [])
            hc_movs = [m for m in movs if any(w in m.get('nome', '').upper() for w in ['HABEAS', 'RECURSO', 'AGRAVO', 'INSTÂNCIA', 'TRIBUNAL'])]
            print(f"  • Movimentações com menção a recurso/HC: {len(hc_movs)}")
            for m in hc_movs[:10]:
                print(f"     - {m.get('dataHora')[:10]} | {m.get('nome')}")
except Exception as e:
    print(f"Erro: {e}")

print("\n=== CONSULTA CONCLUÍDA ===")
