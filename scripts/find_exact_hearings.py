# -*- coding: utf-8 -*-
import json
import re
import fitz

with open(r"c:\Projetos\Super Analista Jurídico\scripts\datajud_all_ecildo.json", "r", encoding="utf-8") as f:
    datajud_all = json.load(f)

print("=== BUSCA POR MOVIMENTAÇÕES DE AUDIÊNCIA NO DATAJUD ===")

all_hearings_datajud = []

for proc, hits in datajud_all.items():
    if not isinstance(hits, list):
        continue
    for h in hits:
        movs = h.get('movimentos', [])
        for m in movs:
            nome = m.get('nome', '')
            dt = m.get('dataHora', '')
            comps = m.get('complementosTabelados', [])
            comps_str = " ".join([f"{c.get('nome')}:{c.get('valor')}" for c in comps if isinstance(c, dict)])
            full_txt = f"{nome} {comps_str}"
            
            if 'audi' in full_txt.lower() or 'custodi' in full_txt.lower() or 'julgamento' in full_txt.lower() or 'designa' in full_txt.lower() or 'pauta' in full_txt.lower():
                all_hearings_datajud.append({
                    "processo": proc,
                    "classe": h.get('classe', {}).get('nome'),
                    "orgao": h.get('orgaoJulgador', {}).get('nome'),
                    "dataHora": dt,
                    "descricao": nome,
                    "complementos": comps
                })

for ah in sorted(all_hearings_datajud, key=lambda x: x['dataHora'], reverse=True):
    print(f"[{ah['dataHora']}] Proc {ah['processo']} ({ah['classe']}) - {ah['descricao']}")
    if ah['complementos']:
        print("  Comp:", ah['complementos'])

print("\n=== BUSCA POR TERMOS DE AUDIÊNCIA EM MHTML E PDF ===")
with open(r"c:\Projetos\Super Analista Jurídico\scripts\mhtml1_text.txt", "r", encoding="utf-8") as f:
    m1 = f.read()

m1_lines = m1.split('\n')
for i, l in enumerate(m1_lines):
    if any(k in l.lower() for k in ['audiência', 'audiencia', 'custódia', 'custodia']):
        context = "\n".join(m1_lines[max(0, i-2):min(len(m1_lines), i+3)])
        print(f"Line {i}: {l.strip()}")
        # print context snippet if short
