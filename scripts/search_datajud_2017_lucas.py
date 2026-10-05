import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

# 1. Pesquisa ampla por wildcard / query_string no Datajud TJRJ
search_queries = [
    # Query 1: Lucas de Souza Freitas e 2017
    {
        "query": {
            "query_string": {
                "query": "Lucas AND Freitas AND 2017"
            }
        },
        "size": 50
    },
    # Query 2: Marcia de Souza Freitas
    {
        "query": {
            "query_string": {
                "query": "\"Marcia de Souza Freitas\" OR \"Márcia de Souza Freitas\""
            }
        },
        "size": 50
    },
    # Query 3: Niterói 2017 homicídio / roubo / furto / tráfico / lesão
    {
        "query": {
            "query_string": {
                "query": "\"Lucas de Souza\" AND 2017"
            }
        },
        "size": 50
    }
]

for idx, q in enumerate(search_queries, start=1):
    print(f"=== EXECUTANDO BUSCA {idx} DA DATAJUD ===")
    req = urllib.request.Request(url, data=json.dumps(q).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            print(f"Resultados encontrados: {len(hits)}")
            for h in hits:
                src = h['_source']
                num = src.get('numeroProcesso', '')
                classe = src.get('classe', {}).get('nome', '')
                orgao = src.get('orgaoJulgador', {}).get('nome', '')
                dt = src.get('dataAjuizamento', '')
                print(f"  -> Processo: {num} | Classe: {classe} | Órgão: {orgao} | Data: {dt}")
                
                # Checar se contem a palavra Lucas ou Marcia
                src_str = json.dumps(src, ensure_ascii=False)
                for line in src_str.split(','):
                    if any(w in line.lower() for w in ['lucas', 'marcia', 'márcia', 'rg', 'cpf', 'alvará', 'soltura']):
                        print("     *", line.strip()[:140])
    except Exception as e:
        print(f"Erro na busca {idx}: {e}")

print("Busca concluída!")
