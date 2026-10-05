# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

target_file = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\acao_penal_08027595320258190023_G1.json"
src = json.load(open(target_file, encoding="utf-8"))

movs = src.get("movimentos", [])
movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""))

print("=== TODAS AS MOVIMENTAÇÕES DE 2026 NA AÇÃO PENAL ===")
for m in movs_sorted:
    dt = m.get("dataHora", "")
    if "2026" in dt:
        comps = m.get("complementosTabelados", [])
        comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
        print(f"[{dt[:19]}] {m.get('nome')} (Cód {m.get('codigo')})" + (f" - {comp_str}" if comp_str else ""))
