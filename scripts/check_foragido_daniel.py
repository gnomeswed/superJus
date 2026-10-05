# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\datajud_raw_1_GUAPIMIRIM_2_VARA_Ação_Penal_de_Competência_do_Júri.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

movs = sorted(data.get("movimentos", []), key=lambda m: m.get("dataHora", ""))

print("=== BUSCA POR MOVIMENTAÇÕES DE 2019 A 2024 (FORAGIDO / PRISÃO / ART 366) ===")

for m in movs:
    nm = m.get("nome", "")
    cod = m.get("codigo", "")
    dt = m.get("dataHora", "")[:19].replace("T", " ")
    comps = [f"{c.get('nome')}: {c.get('descricao')}" for c in m.get("complementosTabelados", [])]
    comp_str = " | ".join(comps) if comps else ""
    
    # Filtrar anos de 2019 a 2024 com termos relevantes
    if any(yr in dt for yr in ["2019", "2020", "2021", "2022", "2023", "2024"]):
        if any(term in (nm + " " + comp_str).lower() for term in ["suspensão", "suspensao", "366", "edital", "mandado", "prisão", "prisao", "captura", "cumprimento", "revelia", "procuração", "procuracao", "defesa prévia", "resposta à acusação", "decisão"]):
            print(f"[{dt}] Cod {cod}: {nm} -> {comp_str}")
