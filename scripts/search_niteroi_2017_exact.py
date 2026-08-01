# -*- coding: utf-8 -*-
import json
import urllib.request

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

# Consultas no Datajud para Niterói
queries = [
    # Query A: Qualquer processo com "Lucas de Souza Freitas"
    {
        "query": {
            "query_string": {
                "query": "\"Lucas de Souza Freitas\""
            }
        },
        "size": 50
    },
    # Query B: "Lucas" AND "Freitas" AND "Niterói"
    {
        "query": {
            "query_string": {
                "query": "Lucas AND Freitas AND Niteroi"
            }
        },
        "size": 50
    },
    # Query C: "Marcia de Souza Freitas"
    {
        "query": {
            "query_string": {
                "query": "\"Marcia de Souza\" OR \"Márcia de Souza\""
            }
        },
        "size": 50
    }
]

for idx, q in enumerate(queries, start=1):
    print(f"=== BUSCA DATAJUD NITERÓI {idx} ===")
    req = urllib.request.Request(url, data=json.dumps(q).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            print(f"Resultados: {len(hits)}")
            for h in hits:
                src = h['_source']
                num = src.get('numeroProcesso', '')
                classe = src.get('classe', {}).get('nome', '')
                orgao = src.get('orgaoJulgador', {}).get('nome', '')
                dt = src.get('dataAjuizamento', '')
                print(f" -> Processo: {num} | Classe: {classe} | Órgão: {orgao} | Data: {dt}")
                
                # Inspecionar para ver se contem RG / CPF / Alvará / Soltura
                src_str = json.dumps(src, ensure_ascii=False)
                for l in src_str.split(','):
                    if any(w in l.lower() for w in ['rg', 'cpf', 'identidade', 'alvará', 'soltura', 'lucas', 'marcia']):
                        print("   *", l.strip()[:140])
    except Exception as e:
        print("Erro:", e)
