import sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
# -*- coding: utf-8 -*-
import json
import urllib.request

procs = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal (Búzios - 2ª Vara)"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Principal (Búzios)"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "Habeas Corpus (7ª Câm. Criminal TJRJ)"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "Execução / Medida (Búzios)")
]

url = 'https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search'
headers = {
    'Authorization': __import__('core.config', fromlist=['datajud_headers']).datajud_headers()['Authorization'],
    'Content-Type': 'application/json'
}

for formatted, clean, label in procs:
    req_data = json.dumps({"query": {"match": {"numeroProcesso": clean}}, "size": 10}).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            hits = res.get('hits', {}).get('hits', [])
            print(f"=== Processo: {formatted} ({label}) ===")
            for hit in hits:
                src = hit['_source']
                movs = src.get('movimentos', [])
                movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
                for m in movs_sorted[:4]:
                    dt = m.get('dataHora', '')
                    nome = m.get('nome', '')
                    comps = m.get('complementosTabelados', [])
                    comp_str = ""
                    if comps:
                        comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
                    print(f"  • {dt[:19].replace('T', ' ')} — {nome}{comp_str}")
    except Exception as e:
        print(f"Erro em {formatted}: {e}")
