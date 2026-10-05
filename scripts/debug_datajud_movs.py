# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

headers = {
    'Authorization': 'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==',
    'Content-Type': 'application/json'
}

proc_clean = "08085953620268190002"
url_tjrj = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'

req_data = json.dumps({"query": {"match": {"numeroProcesso": proc_clean}}, "size": 10}).encode('utf-8')
req = urllib.request.Request(url_tjrj, data=req_data, headers=headers)

with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    hits = res.get('hits', {}).get('hits', [])
    for hit in hits:
        src = hit['_source']
        movs = src.get('movimentos', [])
        for m in movs:
            # Let's inspect movements around 10/08/2026
            dt = m.get('dataHora', '')
            if '2026-08-10' in dt or '2026-08-17' in dt or 'Liberdade' in m.get('nome', ''):
                print(json.dumps(m, indent=2, ensure_ascii=False))
