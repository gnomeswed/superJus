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

req_data = json.dumps({"query": {"match": {"numeroProcesso": "00464189820178190000"}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url, data=req_data, headers=headers)

try:
    with urllib.request.urlopen(req) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        print("=== JSON COMPLETO DO DATAJUD PARA O HC 0046418-98.2017.8.19.0000 ===")
        print(json.dumps(res, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Erro: {e}")
