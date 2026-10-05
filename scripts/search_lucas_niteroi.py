import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request
import re

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

# Buscar por "FREITAS" e "LUCAS" na Comarca de Niterói ou TJRJ
q = {
    "query": {
        "bool": {
            "must": [
                {"match_phrase": {"movimentos.complementosTabelados.descricao": "Lucas de Souza Freitas"}}
            ]
        }
    },
    "size": 50
}

req = urllib.request.Request(url, data=json.dumps(q).encode('utf-8'), headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"Total encontrado: {len(hits)}")
        for idx, h in enumerate(hits, start=1):
            src = h['_source']
            num = src.get('numeroProcesso', '')
            classe = src.get('classe', {}).get('nome', '')
            orgao = src.get('orgaoJulgador', {}).get('nome', '')
            dt = src.get('dataAjuizamento', '')
            print(f"{idx}. Processo: {num} | Classe: {classe} | Órgão: {orgao} | Data: {dt}")
            
            # Checar se há menção a RG / Alvará / Soltura nas movimentações
            src_str = json.dumps(src, ensure_ascii=False)
            if "alvará" in src_str.lower() or "alvara" in src_str.lower() or "rg" in src_str.lower():
                print("   Found keywords in process!")
                # buscar padroes de RG (7-10 digitos) ou linhas com documento
                for l in src_str.split(','):
                    if any(w in l.lower() for w in ['rg', 'cpf', 'identidade', 'alvará', 'soltura', 'expedid']):
                        print("     ->", l.strip()[:140])
except Exception as e:
    print("Erro:", e)
