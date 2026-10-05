# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\datajud_raw_1_GUAPIMIRIM_2_VARA_Ação_Penal_de_Competência_do_Júri.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

movs = sorted(data.get("movimentos", []), key=lambda m: m.get("dataHora", ""))

print(f"=== AUDIÊNCIAS, DECISÕES E PERÍCIAS NOS AUTOS ===")

for m in movs:
    nm = m.get("nome", "")
    cod = m.get("codigo", "")
    dt = m.get("dataHora", "")[:19].replace("T", " ")
    comps = [f"{c.get('nome')}: {c.get('descricao')}" for c in m.get("complementosTabelados", [])]
    comp_str = " | ".join(comps) if comps else ""
    
    # Filtrar audiencias, sentencas, decisoes, laudos
    if any(term in nm.lower() for term in ["audiência", "audiencia", "sessão", "sessao", "pronúncia", "pronuncia", "procedência", "procedencia", "laudo", "perícia", "pericia", "júri", "juri", "decisão", "decisao"]):
        print(f"[{dt}] Cod {cod}: {nm} -> {comp_str}")
