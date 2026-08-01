# -*- coding: utf-8 -*-
import json

with open(r"c:\Projetos\Super Analista Jurídico\scripts\datajud_all_ecildo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

proc = "1003524-57.2023.8.11.0015"
hits = data.get(proc, [])

print(f"=== ANÁLISE DE SENTENÇA - PROCESSO {proc} ===")

for h in hits:
    classe = h.get('classe', {}).get('nome')
    orgao = h.get('orgaoJulgador', {}).get('nome')
    movs = h.get('movimentos', [])
    movs_sorted = sorted(movs, key=lambda x: x.get('dataHora', ''), reverse=True)
    
    print(f"\nInstância / Órgão: {classe} | {orgao}")
    print(f"Total de movimentações: {len(movs)}")
    
    sentences = [m for m in movs if 'senten' in m.get('nome', '').lower() or 'conden' in m.get('nome', '').lower() or 'absolv' in m.get('nome', '').lower()]
    decisions = [m for m in movs if 'decis' in m.get('nome', '').lower() or 'despacho' in m.get('nome', '').lower()]
    
    if sentences:
        print("SENTENÇAS ENCONTRADAS:")
        for s in sentences:
            print(f"  * {s.get('dataHora')}: {s.get('nome')}")
    else:
        print("NENHUMA SENTENÇA PROFERIDA ATÉ O MOMENTO.")
        
    print("\nÚltimas 10 movimentações:")
    for m in movs_sorted[:10]:
        print(f"  - {m.get('dataHora')}: {m.get('nome')} | {m.get('complementosTabelados')}")
