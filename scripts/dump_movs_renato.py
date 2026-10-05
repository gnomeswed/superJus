# -*- coding: utf-8 -*-
import json
from pathlib import Path

src = json.load(open(r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\acao_penal_08016300420258190026_G1.json", encoding="utf-8"))
movs = src.get("movimentos", [])
movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)

print("=" * 80)
print(f"MOVIMENTAÇÕES CRONOLÓGICAS COMPLETAS — PROCESSO RENATO BASTOS ROCHA")
print(f"Total de Movimentações: {len(movs)}")
print("=" * 80)

for idx, m in enumerate(movs_sorted[:35], 1):
    dt = m.get("dataHora", "")[:19].replace("T", " ")
    nm = m.get("nome", "")
    code = m.get("codigo", "")
    comps = m.get("complementosTabelados", [])
    comp_str = ""
    if comps:
        comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
    print(f"{idx:02d}. [{dt}] — {nm}{comp_str} [Cód. {code}]")
