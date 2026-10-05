# -*- coding: utf-8 -*-
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

target_file = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\acao_penal_08027595320258190023_G1.json"
src = json.load(open(target_file, encoding="utf-8"))

movs = src.get("movimentos", [])
movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""))

print("=== MOVIMENTAÇÕES DE MAIO/2025 A DEZEMBRO/2025 ===")
for m in movs_sorted:
    dt = m.get("dataHora", "")
    if "2025-05" in dt or "2025-06" in dt or "2025-07" in dt or "2025-08" in dt or "2025-09" in dt or "2025-10" in dt or "2025-11" in dt or "2025-12" in dt:
        comps = m.get("complementosTabelados", [])
        comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
        print(f"[{dt[:19]}] {m.get('nome')} (Cód {m.get('codigo')})" + (f" - {comp_str}" if comp_str else ""))
