# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"

procs = [
    ("0800060-52.2023.8.19.0058", "Saquarema 1 - Roubo Majorado / Dosimetria"),
    ("0800262-29.2023.8.19.0058", "Saquarema 2 - Flagrante e Roubo"),
    ("0801082-93.2023.8.19.0043", "Piraí - Roubo Majorado"),
    ("0809172-80.2023.8.19.0014", "Campos - Tráfico e Armas")
]

print("=== CONSOLIDANDO AS SENTENÇAS, ACÓRDÃOS E DESPACHOS DE TODOS OS PROCESSOS ===")

sentencas_doc = [
    "# ⚖️ PAINEL INTEGRAL DE SENTENÇAS E ACÓRDÃOS",
    "**Cliente:** Rodrigo dos Reis Nóbrega  ",
    "**Comarca de Origem:** Saquarema / RJ  ",
    "**Data da Compilação:** 30/08/2026  \n",
    "---\n"
]

for num_cnj, desc in procs:
    p_dir = os.path.join(target_dir, "processos", num_cnj)
    g1_file = os.path.join(p_dir, "raw_G1.json")
    g2_file = os.path.join(p_dir, "raw_G2.json")
    
    sentencas_doc.append(f"## 🏛️ PROCESSO: `{num_cnj}` — {desc}")
    
    # 1ª Instância (Sentença)
    if os.path.exists(g1_file):
        src1 = json.load(open(g1_file, encoding="utf-8"))
        orgao1 = src1.get("orgaoJulgador", {}).get("nome")
        movs1 = src1.get("movimentos", [])
        
        sentencas_doc.append(f"### 📄 1ª Instância: {orgao1}")
        # Filtrar sentenças, decisões, conclusões
        sent_movs = [m for m in movs1 if any(k in m.get("nome", "").lower() for k in [
            "sentença", "sentenca", "decisão", "decisao", "julgamento", "condenação", "condenacao", "conclusão", "conclusao", "audiência", "audiencia", "definitivo", "baixa"
        ])]
        
        sent_sorted = sorted(sent_movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        for sm in sent_sorted:
            dt = sm.get("dataHora", "")[:19].replace("T", " ")
            comps = sm.get("complementosTabelados", [])
            comp_str = " | ".join([f"**{c.get('descricao')}:** {c.get('nome')}" for c in comps])
            sentencas_doc.append(f"- **`{dt}`** — **{sm.get('nome')}** (Código CNJ: `{sm.get('codigo')}`)")
            if comp_str:
                sentencas_doc.append(f"  - *Detalhes:* {comp_str}")
        sentencas_doc.append("\n")
        
    # 2ª Instância (Acórdão / Apelação)
    if os.path.exists(g2_file):
        src2 = json.load(open(g2_file, encoding="utf-8"))
        orgao2 = src2.get("orgaoJulgador", {}).get("nome")
        movs2 = src2.get("movimentos", [])
        
        sentencas_doc.append(f"### ⚖️ 2ª Instância (Acórdão TJRJ): {orgao2}")
        acord_movs = [m for m in movs2 if any(k in m.get("nome", "").lower() for k in [
            "acórdão", "acordao", "julgamento", "decisão", "decisao", "sessão", "sessao", "conclusão", "conclusao", "baixa", "definitivo", "distribuição"
        ])]
        acord_sorted = sorted(acord_movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        for am in acord_sorted:
            dt = am.get("dataHora", "")[:19].replace("T", " ")
            comps = am.get("complementosTabelados", [])
            comp_str = " | ".join([f"**{c.get('descricao')}:** {c.get('nome')}" for c in comps])
            sentencas_doc.append(f"- **`{dt}`** — **{am.get('nome')}** (Código CNJ: `{am.get('codigo')}`)")
            if comp_str:
                sentencas_doc.append(f"  - *Detalhes:* {comp_str}")
        sentencas_doc.append("\n")
        
    sentencas_doc.append("---\n")

out_file = os.path.join(target_dir, "SENTENCAS_E_ACORDAOS_COMPILADOS.md")
with open(out_file, "w", encoding="utf-8") as f:
    f.write("\n".join(sentencas_doc))

print(f"✅ Painel de sentenças consolidado em: {out_file}")
