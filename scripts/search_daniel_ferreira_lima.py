# -*- coding: utf-8 -*-
import json
import urllib.request
import time
import os
import sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

sys.stdout.reconfigure(encoding='utf-8')

nome_busca = "Daniel Ferreira Lima"
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

results = {
    "datajud": {},
    "tjrj_portal": [],
    "local_files": []
}

def query_datajud(endpoint, query_payload):
    url = f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search"
    try:
        req_data = json.dumps(query_payload).encode('utf-8')
        req = urllib.request.Request(url, data=req_data, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

print(f"=== PESQUISANDO PROCESSO DE: {nome_busca} ===")

# 1. Pesquisa DataJud em múltiplos tribunais (TJRJ, STJ, STF, TJSP, TRF2)
tribunais = [
    ("api_publica_tjrj", "TJRJ - Tribunal de Justiça do RJ"),
    ("api_publica_stj", "STJ - Superior Tribunal de Justiça"),
    ("api_publica_stf", "STF - Supremo Tribunal Federal"),
    ("api_publica_tjsp", "TJSP - Tribunal de Justiça de SP"),
    ("api_publica_trf2", "TRF2 - Tribunal Regional Federal 2ª Região")
]

for ep, desc in tribunais:
    print(f"\nConsulta DataJud ({desc})...")
    # Tentar match_phrase e match com slop ou wildcard se necessário
    payload = {
        "query": {
            "match_phrase": {
                "polo.parte.pessoa.nome": nome_busca
            }
        },
        "size": 20
    }
    res = query_datajud(ep, payload)
    
    # Se match_phrase em polo.parte.pessoa.nome não trouxer resultados, tentar busca mais ampla
    hits = res.get('hits', {}).get('hits', []) if isinstance(res, dict) else []
    if not hits:
        payload_alt = {
            "query": {
                "match_phrase": {
                    "partes.nome": nome_busca
                }
            },
            "size": 20
        }
        res_alt = query_datajud(ep, payload_alt)
        hits_alt = res_alt.get('hits', {}).get('hits', []) if isinstance(res_alt, dict) else []
        if hits_alt:
            res = res_alt
            hits = hits_alt
            
    if not hits:
        # Tentar query string solta
        payload_qs = {
            "query": {
                "query_string": {
                    "query": f'"{nome_busca}"'
                }
            },
            "size": 20
        }
        res_qs = query_datajud(ep, payload_qs)
        hits_qs = res_qs.get('hits', {}).get('hits', []) if isinstance(res_qs, dict) else []
        if hits_qs:
            res = res_qs
            hits = hits_qs

    print(f"Total encontrado: {len(hits)}")
    results["datajud"][ep] = []
    for hit in hits:
        src = hit.get('_source', {})
        proc_num = src.get('numeroProcesso')
        classe = src.get('classe', {}).get('nome', 'N/I')
        orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
        dt_at = src.get('dataHoraUltimaAtualizacao', 'N/I')
        dt_ajuiz = src.get('dataAjuizamento', 'N/I')
        assuntos = [a.get('nome') for a in src.get('assuntos', [])]
        movs = src.get('movimentos', [])
        movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
        
        proc_info = {
            "numeroProcesso": proc_num,
            "classe": classe,
            "orgaoJulgador": orgao,
            "dataAjuizamento": dt_ajuiz,
            "dataHoraUltimaAtualizacao": dt_at,
            "assuntos": assuntos,
            "ultimos_movimentos": movs_sorted[:5]
        }
        results["datajud"][ep].append(proc_info)
        print(f"  - Proc: {proc_num} | Classe: {classe} | Órgão: {orgao} | Data: {dt_ajuiz[:10] if dt_ajuiz else 'N/I'}")

# 2. Pesquisa de arquivos locais no computador (Desktop, Clientes, Downloads)
search_dirs = [
    r"C:\Users\Administrator\Desktop",
    r"C:\Projetos\superJus\Clientes",
    r"C:\Users\Administrator\Downloads"
]

print("\nVerificando arquivos locais...")
for d in search_dirs:
    if os.path.exists(d):
        for root, _, files in os.walk(d):
            for file in files:
                if any(x in file.lower() for x in ["daniel", "ferreira", "lima"]):
                    fpath = os.path.join(root, file)
                    results["local_files"].append(fpath)
                    print(f"  Arquivo encontrado: {fpath}")

# Save JSON result
out_file = r"c:\Projetos\superJus\daniel_ferreira_lima_result.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nResultados salvos em: {out_file}")
