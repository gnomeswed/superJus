# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
base = r"c:\Projetos\superJus\Clientes\Ecildo_Victor\processos"

print("=== AUDITORIA DE AUDIÊNCIAS - ECILDO VICTOR DOS SANTOS FERREIRA ===\n")

found_hearings = []

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
        
        for m in movs:
            nome = m.get("nome", "")
            comps = m.get("complementosTabelados", [])
            comp_str = " | ".join([f"{c.get('descricao', '')}: {c.get('nome', '')}" for c in comps])
            full = (nome + " " + comp_str).lower()
            if any(k in full for k in ["audiên", "audien", "custódia", "custodia", "apresentação", "apresentacao", "interrogatório", "interrogatorio"]):
                dt = m.get("dataHora", "")[:19]
                found_hearings.append({
                    "data": dt,
                    "processo": folder,
                    "vara": meta.get("vara", ""),
                    "grau": grau,
                    "orgao": orgao,
                    "movimento": nome,
                    "detalhes": comp_str
                })

# Also check other files in Ecildo_Victor folder (like text notes, dossiers, etc.)
extra_notes = []
for root, dirs, files in os.walk(r"c:\Projetos\superJus\Clientes\Ecildo_Victor"):
    for f in files:
        if f.endswith((".md", ".txt", ".html", ".json")):
            fp = os.path.join(root, f)
            try:
                txt = open(fp, "r", encoding="utf-8", errors="ignore").read()
                lines = txt.splitlines()
                for idx, line in enumerate(lines):
                    if any(k in line.lower() for k in ["audiência", "audiencia", "custódia", "custodia", "apresentação"]):
                        extra_notes.append((f, idx+1, line.strip()))
            except Exception:
                pass

print("1. AUDIÊNCIAS REGISTRADAS NAS MOVIMENTAÇÕES OFICIAIS:")
for h in sorted(found_hearings, key=lambda x: x["data"], reverse=True):
    print(f"  • Data: {h['data']} | Processo: {h['processo']} ({h['vara']})")
    print(f"    Movimento: {h['movimento']} | Detalhes: {h['detalhes']}\n")

print("\n2. MENÇÕES A AUDIÊNCIAS NOS DOCUMENTOS E DOSSIÊS DO CLIENTE:")
for fn, lnum, ltxt in extra_notes[:15]:
    print(f"  • [{fn}:L{lnum}] {ltxt[:140]}")
