# -*- coding: utf-8 -*-
import json

with open(r"c:\Projetos\Super Analista Jurídico\scripts\datajud_all_ecildo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

proc = "1003524-57.2023.8.11.0015"
hits = data.get(proc, [])

for h in hits:
    classe = h.get('classe', {}).get('nome')
    orgao = h.get('orgaoJulgador', {}).get('nome')
    movs = h.get('movimentos', [])
    movs_sorted = sorted(movs, key=lambda x: x.get('dataHora', ''))
    
    print(f"\n=================== {classe} | {orgao} ({len(movs)} movs) ===================")
    for idx, m in enumerate(movs_sorted, 1):
        dt = m.get('dataHora')
        nome = m.get('nome')
        comps = m.get('complementosTabelados')
        print(f"{idx:03d}. [{dt}] {nome} {comps if comps else ''}")
