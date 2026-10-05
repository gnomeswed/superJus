# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

target_file = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha\acao_penal_08027595320258190023_G1.json"
src = json.load(open(target_file, encoding="utf-8"))

print("=== ANÁLISE DETALHADA DA AÇÃO PENAL 0802759-53.2025.8.19.0023 ===")
movs = src.get("movimentos", [])
print(f"Total movimentos: {len(movs)}")

# Filtrar decisões, sentenças, audiências, mandados, alvarás
marcos = [m for m in movs if any(k in m.get("nome", "").lower() for k in [
    "prisão", "liberdade", "alvará", "audiência", "decisão", "despacho", "recebimento", "denúncia", "mandado", "defesa"
])]

marcos_sorted = sorted(marcos, key=lambda m: m.get("dataHora", ""))
print(f"Marcos relevantes ({len(marcos_sorted)}):")
for m in marcos_sorted:
    dt = m.get("dataHora", "")[:19].replace("T", " ")
    comps = m.get("complementosTabelados", [])
    comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
    print(f"[{dt}] {m.get('nome')} (Cód {m.get('codigo')})" + (f" - {comp_str}" if comp_str else ""))
