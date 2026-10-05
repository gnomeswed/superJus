import json
import os

with open(r"C:\Projetos\swedsystem\docs\consulta_ao_vivo_22_09_2026.json", "r", encoding="utf-8") as f:
    d22 = json.load(f)

print("Data da consulta:", d22.get("data_consulta"), d22.get("hora_consulta"))
portal = d22.get("portal_tjrj", {})

for k, v in portal.items():
    if isinstance(v, dict):
        print(f"\n==========================================")
        print(f"PROCESSO: {k}")
        print(f"Status: {v.get('status')}")
        print(f"Localizacao: {v.get('localizacao')}")
        print(f"Ultimo movimento: {v.get('ultimo_movimento')}")
        print(f"Total movimentos: {v.get('total_movimentos')}")
        movs = v.get("ultimos_movimentos", [])
        print(f"Top movimentos ({len(movs)}):")
        for m in movs:
            print(f"  - {m}")
    else:
        print(f"\n{k}: {v}")
