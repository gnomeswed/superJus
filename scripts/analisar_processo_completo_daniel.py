# -*- coding: utf-8 -*-
import json
import os
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

raw_path = r"C:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\datajud_raw_2026-09-07_132404.json"
out_report = r"C:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima\02_Movimentacoes\relatorio_integral_processo_daniel.md"

with open(raw_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total instâncias no DataJud: {len(data)}")

g1_doc = None
g2_doc = None

for d in data:
    if d.get("grau") == "G1":
        g1_doc = d
    elif d.get("grau") == "G2":
        g2_doc = d

if not g1_doc and len(data) > 0:
    g1_doc = data[1] if len(data) > 1 else data[0]

movs_g1 = g1_doc.get("movimentos", [])
# Sort chronological
movs_g1_chrono = sorted(movs_g1, key=lambda m: m.get("dataHora", ""))

print(f"Total movimentos G1: {len(movs_g1_chrono)}")

# Identify key milestones
milestones = []
for m in movs_g1_chrono:
    cod = m.get("codigo")
    nome = m.get("nome", "")
    dt = m.get("dataHora", "")
    comps = m.get("complementosTabelados", [])
    comp_str = "; ".join([f"{c.get('nome')} ({c.get('descricao')})" for c in comps])
    
    # Check important keywords or codes
    is_important = False
    reasons = []
    
    if cod in [26]: # Distribuicao
        reasons.append("Distribuição da Ação Penal")
    elif cod in [219, 193, 237, 246]: # Julgamento / Sentenca
        reasons.append(f"Decisão/Sentença/Julgamento: {nome}")
    elif cod in [12066, 12067, 12068]: # Prisao
        reasons.append(f"Prisão/Custódia: {nome}")
    elif cod in [12146]: # Liberdade
        reasons.append(f"Liberdade Provisória: {nome}")
    elif cod in [497, 856, 12260]: # Sessao do Juri
        reasons.append(f"Tribunal do Júri: {nome}")
    elif cod in [123]: # Remessa
        reasons.append(f"Remessa: {nome} ({comp_str})")
    elif cod in [426, 85]: # Peticao / Recurso
        if "recurso" in comp_str.lower() or "apela" in comp_str.lower() or "razões" in comp_str.lower():
            reasons.append(f"Recurso/Apelação: {nome} ({comp_str})")
    elif cod in [11025, 11026, 11027]: # Pronuncia
        reasons.append(f"Pronúncia: {nome}")
    elif cod in [11383, 11010]:
        if "júri" in comp_str.lower() or "pauta" in comp_str.lower():
            reasons.append(f"Ato Relevante: {nome} ({comp_str})")
            
    if reasons or "2026" in dt:
        milestones.append({
            "data": dt[:19].replace("T", " "),
            "codigo": cod,
            "nome": nome,
            "complementos": comp_str,
            "motivo": " | ".join(reasons) if reasons else "Movimentação 2026"
        })

print(f"Marcos relevantes identificados: {len(milestones)}")

# Write detailed markdown report
with open(out_report, "w", encoding="utf-8") as f:
    f.write("# RELATÓRIO INTEGRAL E AUDITORIA PROCESSUAL — DANIEL FERREIRA LIMA\n\n")
    f.write(f"**Data da Auditoria:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
    f.write(f"**Número Único CNJ:** `0004301-33.2018.8.19.0073`\n")
    f.write(f"**Comarca / Juízo:** {g1_doc.get('orgaoJulgador', {}).get('nome', 'Guapimirim 2ª Vara')}\n")
    f.write(f"**Classe Processual:** {g1_doc.get('classe', {}).get('nome', 'Ação Penal de Competência do Júri')}\n")
    f.write(f"**Data de Ajuizamento:** 03/05/2018\n")
    f.write(f"**Assuntos:** {', '.join([a.get('nome') for a in g1_doc.get('assuntos', [])])}\n\n")
    
    f.write("---\n\n")
    f.write("## 📌 1. Resumo Executivo da Situação Processual\n\n")
    f.write("- **Fase Atual:** Autos remetidos ao Tribunal de Justiça do Estado do Rio de Janeiro (TJRJ) em **15/06/2026** em grau de **Apelação Criminal**.\n")
    f.write("- **Origem:** Sessão Plenária do Tribunal do Júri realizada em **18/05/2026** na 2ª Vara de Guapimirim, com condenação pelo conselho de sentença.\n")
    f.write("- **Histórico Pregresso:** Ação distribuída em 2018; suspensa sob o Art. 366 do CPP; cumprimento de mandado de prisão em 01/04/2024; pronúncia confirmada pelo TJRJ no RESE (Desª Márcia Perrini Bodart em 22/05/2025); júri em 18/05/2026.\n\n")
    
    f.write("---\n\n")
    f.write("## ⏱️ 2. Linha do Tempo dos Marcos Críticos e Decisões\n\n")
    f.write("| Data / Hora | Cód. TPU | Movimento | Complemento / Detalhe | Relevância Jurídica |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    for m in milestones:
        f.write(f"| {m['data']} | {m['codigo']} | {m['nome']} | {m['complementos']} | **{m['motivo']}** |\n")
        
    f.write("\n---\n\n")
    f.write("## 📜 3. Últimos 20 Andamentos na 1ª Instância (Guapimirim - 2026)\n\n")
    f.write("| Data / Hora | Cód. TPU | Movimento | Complementos |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    for m in movs_g1_chrono[-20:]:
        dt = m.get("dataHora", "")[:19].replace("T", " ")
        cod = m.get("codigo")
        nome = m.get("nome")
        comps = m.get("complementosTabelados", [])
        comp_str = "; ".join([f"{c.get('nome')} ({c.get('descricao')})" for c in comps])
        f.write(f"| {dt} | {cod} | {nome} | {comp_str} |\n")

print(f"Relatório gerado com sucesso em: {out_report}")
