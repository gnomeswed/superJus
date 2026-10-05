# -*- coding: utf-8 -*-
import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\datajud_raw_1_GUAPIMIRIM_2_VARA_Ação_Penal_de_Competência_do_Júri.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

movs = sorted(data.get("movimentos", []), key=lambda m: m.get("dataHora", ""))

print(f"Total de movimentos: {len(movs)}")

# 1. Primeiros 20 movimentos (denuncia, inquerito, fatos de 2018)
print("\n--- PRIMEIROS 25 MOVIMENTOS (2018) ---")
for m in movs[:25]:
    dt = m.get("dataHora", "")[:19].replace("T", " ")
    nm = m.get("nome", "")
    cod = m.get("codigo", "")
    comps = [f"{c.get('nome')}: {c.get('descricao')}" for c in m.get("complementosTabelados", [])]
    comp_str = "; ".join(comps) if comps else ""
    print(f"{dt} | Cod {cod}: {nm} | {comp_str}")

# 2. Buscar movimentos que contenham termos como inquerito, denuncia, prisao, laudo, pericia, vítima
keywords = ["denúncia", "denuncia", "inquérito", "inquerito", "laudo", "necrópsia", "necropsia", "local", "arma", "flagrante", "preventiva", "pronúncia", "pronuncia", "vítima", "vitima"]
print("\n--- MOVIMENTOS COM TERMOS-CHAVE RELEVANTES ---")
for m in movs:
    nm = m.get("nome", "").lower()
    comps = [f"{c.get('nome')}: {c.get('descricao')}".lower() for c in m.get("complementosTabelados", [])]
    all_text = nm + " " + " ".join(comps)
    if any(k in all_text for k in keywords):
        dt = m.get("dataHora", "")[:10]
        cod = m.get("codigo", "")
        print(f"[{dt}] Cod {cod}: {m.get('nome')} | {comps}")
