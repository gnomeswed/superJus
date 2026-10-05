# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
headers = {
    'Authorization': f'APIKey {API_KEY}',
    'Content-Type': 'application/json'
}

nome_busca = "Daniel Ferreira Lima"

# Lista de tribunais para consulta
tjs = [
    "tjrj", "tjsp", "tjmg", "tjba", "tjce", "tjpe", "tjpr", "tjrs", 
    "tjgo", "tjmt", "tjms", "tjdf", "tjes", "tjpa", "tjpb", "tjrn", 
    "tjal", "tjse", "tjma", "tjpi", "tjam", "tjro", "tjrr", "tjac", 
    "tjap", "tjto", "tjsc", "stj"
]

results = []

print(f"Iniciando busca DataJud para: {nome_busca} em 28 tribunais...", flush=True)

for tj in tjs:
    ep = f"api_publica_{tj}"
    url = f"https://api-publica.datajud.cnj.jus.br/{ep}/_search"
    
    # 1. Query com match de nome e filtro de homicídio ou júri ou geral
    payload = {
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": f'"{nome_busca}"'
                        }
                    }
                ]
            }
        },
        "size": 15
    }
    
    try:
        req_data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=req_data, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            if hits:
                print(f"[{tj.upper()}] Encontrados {len(hits)} processos com o nome!", flush=True)
                for h in hits:
                    src = h.get('_source', {})
                    num_proc = src.get('numeroProcesso')
                    classe = src.get('classe', {}).get('nome', '')
                    orgao = src.get('orgaoJulgador', {}).get('nome', '')
                    dt = src.get('dataAjuizamento', '')
                    assuntos = [a.get('nome', '') for a in src.get('assuntos', [])]
                    
                    is_homicidio = any('homic' in a.lower() or '121' in a.lower() or 'vida' in a.lower() for a in assuntos) or ('júri' in orgao.lower() or 'juri' in orgao.lower() or 'júri' in classe.lower() or 'juri' in classe.lower())
                    
                    proc_entry = {
                        "tribunal": tj.upper(),
                        "numero": num_proc,
                        "classe": classe,
                        "orgao": orgao,
                        "dataAjuizamento": dt[:10] if dt else '',
                        "assuntos": assuntos,
                        "is_homicidio": is_homicidio,
                        "movimentos": [m.get('nome', '') for m in src.get('movimentos', [])[:3]]
                    }
                    results.append(proc_entry)
                    print(f"  -> {num_proc} | {classe} | {orgao} | Homicídio: {is_homicidio} | Assuntos: {assuntos}", flush=True)
    except Exception as e:
        # print(f"Erro em {tj}: {e}")
        pass

with open("daniel_homicidio_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nBusca finalizada! Total de processos mapeados: {len(results)}")
homicidios = [r for r in results if r['is_homicidio']]
print(f"Total relacionados a Homicídio/Júri: {len(homicidios)}")
