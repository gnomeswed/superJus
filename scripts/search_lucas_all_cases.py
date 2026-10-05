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

# Pesquisar por "Lucas de Souza Freitas" no Datajud TJRJ
query = {
    "query": {
        "match_phrase": {
            "dadosBasicos.polo.parte.pessoa.nome": "Lucas de Souza Freitas"
        }
    },
    "size": 20
}

req_data = json.dumps(query).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        hits = res.get('hits', {}).get('hits', [])
        print(f"Total de processos encontrados para 'Lucas de Souza Freitas': {len(hits)}")
        
        for idx, hit in enumerate(hits, start=1):
            src = hit['_source']
            num = src.get('numeroProcesso', '')
            classe = src.get('classe', {}).get('nome', '')
            orgao = src.get('orgaoJulgador', {}).get('nome', '')
            dt = src.get('dataAjuizamento', '')
            print(f"{idx}. Processo: {num} | Classe: {classe} | Órgão: {orgao} | Data: {dt}")
            
            # Buscar qualquer texto / complemento com RG, CPF, documento
            src_str = json.dumps(src, ensure_ascii=False)
            doc_matches = re.findall(r'(\b\d{2,3}[\.\s]?\d{3}[\.\s]?\d{3}[-\s]?\d{1,2}\b|\b\d{7,10}\b)', src_str)
            rg_cpf_lines = [l for l in src_str.split('\n') if any(x in l.lower() for x in ['rg', 'cpf', 'identidade', 'alvará', 'soltura', 'documento', 'numero'])]
            if rg_cpf_lines:
                print("   Ocorrências de documentos no JSON:")
                for l in rg_cpf_lines[:5]:
                    print("    ->", l.strip()[:150])
            print("-" * 60)
except Exception as e:
    print(f"Erro na busca Datajud: {e}")
