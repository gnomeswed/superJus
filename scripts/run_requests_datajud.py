import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import requests
import json

url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

payload = {
    "query": {
        "match": {
            "numeroProcesso": "00230135120218190078"
        }
    }
}

print("Iniciando requisição com biblioteca requests...")
try:
    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    print(f"Status Code: {resp.status_code}")
    data = resp.json()
    hits = data.get('hits', {}).get('hits', [])
    print(f"\n========================================================")
    print(f"🎉 CONSULTA CONCLUÍDA COM SUCESSO! TOTAL DE HITS: {len(hits)}")
    print(f"========================================================\n")
    if hits:
        src = hits[0]['_source']
        print(f"• Número do Processo: {src.get('numeroProcesso')}")
        print(f"• Classe: {src.get('classe', {}).get('nome')}")
        print(f"• Órgão Julgador: {src.get('orgaoJulgador', {}).get('nome')}")
        print(f"• Data Ajuizamento: {src.get('dataAjuizamento')}")
        print(f"• Última Atualização: {src.get('dataHoraUltimaAtualizacao')}")
        
        with open("resultado_positivo_datajud.json", "w", encoding="utf-8") as f:
            json.dump(src, f, indent=2, ensure_ascii=False)
except Exception as e:
    print(f"Erro na requisição: {e}")
