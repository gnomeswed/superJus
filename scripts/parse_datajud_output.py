# -*- coding: utf-8 -*-
import json

with open(r"c:\Projetos\Super Analista Jurídico\scripts\datajud_all_ecildo.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== STATUS NO DATAJUD DE TODOS OS PROCESSOS DE ECILDO ===")

summary = []

for proc, hits in data.items():
    if not hits:
        print(f"\n[?] Processo {proc}: Sem dados públicos no DataJud ou em segredo.")
        summary.append({
            "processo": proc,
            "datajud": False,
            "info": "Sem dados públicos no DataJud (ou segredo)"
        })
        continue
    
    print(f"\n[+] Processo {proc} ({len(hits)} registro(s) no DataJud):")
    for idx, h in enumerate(hits):
        np = h.get('numeroProcesso')
        classe = h.get('classe', {}).get('nome', 'N/A')
        orgao = h.get('orgaoJulgador', {}).get('nome', 'N/A')
        dt_ajuiz = h.get('dataAjuizamento', 'N/A')
        movs = h.get('movimentos', [])
        movs_sorted = sorted(movs, key=lambda x: x.get('dataHora', ''), reverse=True)
        
        last_mov = movs_sorted[0] if movs_sorted else {}
        dt_last = last_mov.get('dataHora', 'N/A')
        nome_last = last_mov.get('nome', 'N/A')
        
        # Look for hearings
        auds = [m for m in movs_sorted if 'audi' in m.get('nome', '').lower()]
        
        print(f"  - Record {idx+1}: {classe} | Órgão: {orgao} | Ajuiz: {dt_ajuiz}")
        print(f"    Última Movimentação ({dt_last}): {nome_last}")
        if auds:
            print(f"    Audiências registradas: {len(auds)}")
            for a in auds[:3]:
                print(f"      * {a.get('dataHora')}: {a.get('nome')}")
        else:
            print("    Sem audiências registradas nos movimentos do DataJud.")
            
        summary.append({
            "processo": proc,
            "datajud": True,
            "classe": classe,
            "orgao": orgao,
            "dt_ajuizamento": dt_ajuiz,
            "ultima_movimentacao_data": dt_last,
            "ultima_movimentacao_nome": nome_last,
            "total_movimentacoes": len(movs),
            "audiencias": auds
        })

with open(r"c:\Projetos\Super Analista Jurídico\scripts\ecildo_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)
