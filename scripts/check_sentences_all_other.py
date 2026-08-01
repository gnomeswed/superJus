# -*- coding: utf-8 -*-
import json

with open(r"c:\Projetos\Super Analista Jurídico\scripts\datajud_all_ecildo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== VERIFICAÇÃO DE SENTENÇAS / CONDENAÇÕES EM TODOS OS DEMAIS PROCESSOS ===")

for proc, hits in data.items():
    if proc == "1003524-57.2023.8.11.0015":
        continue
    
    print(f"\n--------------------------------------------------")
    print(f"PROCESSO: {proc}")
    if not hits or not isinstance(hits, list):
        print("  Sem dados no DataJud.")
        continue
    
    for h in hits:
        classe = h.get('classe', {}).get('nome')
        orgao = h.get('orgaoJulgador', {}).get('nome')
        movs = h.get('movimentos', [])
        movs_sorted = sorted(movs, key=lambda x: x.get('dataHora', ''))
        
        print(f"  Classe: {classe} | Vara: {orgao}")
        print(f"  Total de Movimentações: {len(movs)}")
        
        # Check for sentence terms
        sentences = [m for m in movs if any(k in m.get('nome', '').lower() for k in ['senten', 'conden', 'absolv', 'extin', 'punibilid'])]
        if sentences:
            print("  SENTENÇA / DECISÃO DE MÉRITO ENCONTRADA:")
            for s in sentences:
                print(f"    * [{s.get('dataHora')}] {s.get('nome')} | {s.get('complementosTabelados')}")
        else:
            print("  Nenhuma sentença de mérito/condenação registrada no DataJud.")
            
        print("  Últimas 5 movimentações:")
        for m in movs_sorted[-5:]:
            print(f"    - [{m.get('dataHora')}] {m.get('nome')} | {m.get('complementosTabelados')}")
