# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"c:\Projetos\superJus\Clientes\Ecildo_Victor\processos"

print("=== BUSCA POR MOVIMENTAÇÕES E AUDIÊNCIAS EM 2026 NOS PROCESSOS DE ECILDO ===\n")

for folder in sorted(os.listdir(base)):
    json_path = os.path.join(base, folder, "detalhes_processo.json")
    if not os.path.exists(json_path):
        continue
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    meta = data.get("metadados", {})
    
    entries = data.get("datajud_raw", [])
    for entry in entries:
        grau = entry.get("grau", "")
        orgao = entry.get("orgaoJulgador", {}).get("nome", "")
        movs = entry.get("movimentos", [])
        
        movs_2026 = [m for m in movs if m.get("dataHora", "").startswith("2026")]
        if movs_2026:
            print(f"📁 PROCESSO: {folder} ({meta.get('vara')})")
            print(f"   Órgão: [{grau}] {orgao} | Total Movs em 2026: {len(movs_2026)}")
            for m in sorted(movs_2026, key=lambda x: x.get("dataHora", ""), reverse=True):
                comps = m.get("complementosTabelados", [])
                comp_str = " | ".join([f"{c.get('descricao', '')}: {c.get('nome', '')}" for c in comps])
                print(f"   📅 {m.get('dataHora', '')[:19]} | {m.get('nome')} | {comp_str}")
            print("-" * 60)
