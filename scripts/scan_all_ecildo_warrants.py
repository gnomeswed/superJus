# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

base = r"c:\Projetos\superJus\Clientes\Ecildo_Victor\processos"

print("=================================================================")
print("RELATÓRIO DE MANDADOS E IMPEDIMENTOS - ECILDO VICTOR DOS SANTOS FERREIRA")
print("=================================================================")

for folder in sorted(os.listdir(base)):
    json_path = os.path.join(base, folder, "detalhes_processo.json")
    if not os.path.exists(json_path):
        continue
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    meta = data.get("metadados", {})
    vara = meta.get("vara", "")
    assunto = meta.get("assunto", "")
    status = meta.get("status", "")
    
    print(f"\n📁 PROCESSO: {folder}")
    print(f"   Vara: {vara}")
    print(f"   Assunto: {assunto}")
    print(f"   Status Mapeado: {status}")
    
    datajud_entries = data.get("datajud_raw", [])
    has_warrant_movement = False
    
    for entry in datajud_entries:
        grau = entry.get("grau", "")
        orgao = entry.get("orgaoJulgador", {}).get("nome", "")
        classe = entry.get("classe", {}).get("nome", "")
        movs = entry.get("movimentos", [])
        
        # Sort movements descending
        movs_sorted = sorted(movs, key=lambda x: x.get("dataHora", ""), reverse=True)
        
        relevant = []
        for m in movs_sorted:
            nome = m.get("nome", "")
            comps = m.get("complementosTabelados", [])
            comp_str = " | ".join([f"{c.get('descricao', '')}: {c.get('nome', '')}" for c in comps])
            full_txt = (nome + " " + comp_str).lower()
            if any(k in full_txt for k in ["mandado", "pris", "preventiv", "edital", "revel", "366", "alvar", "contramandado", "recambiamento", "provimento", "conclusão para decisão"]):
                dt = m.get("dataHora", "")[:10]
                relevant.append(f"{dt} - {nome} ({comp_str})")
                
        if relevant:
            has_warrant_movement = True
            print(f"   🏛️ [{grau}] {orgao} ({classe}):")
            for r in relevant[:10]: # show top 10 most recent
                print(f"      • {r}")
                
    if not has_warrant_movement:
        print("   ✅ Nenhum mandado ou movimentação de prisão detectada neste feito.")
