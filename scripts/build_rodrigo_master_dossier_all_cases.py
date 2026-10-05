# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"
os.makedirs(target_dir, exist_ok=True)

procs = [
    ("0800060-52.2023.8.19.0058", "Ação Penal 1 — 2ª Vara de Saquarema (Roubo Majorado / Dosimetria)"),
    ("0800262-29.2023.8.19.0058", "Ação Penal 2 — 2ª Vara de Saquarema (Prisão em Flagrante / Roubo)"),
    ("0801082-93.2023.8.19.0043", "Ação Penal 3 — Vara Única de Piraí (Roubo Majorado)"),
    ("0809172-80.2023.8.19.0014", "Ação Penal 4 — 3ª Vara Criminal de Campos (Tráfico / Armas)")
]

dossie_master = []
dossie_master.append("# 🏛️ DOSSIÊ MASTER DE PROCESSOS E EXECUÇÃO PENAL")
dossie_master.append("**Cliente:** Rodrigo dos Reis Nóbrega  ")
dossie_master.append("**Origem Principal:** Comarca de Saquarema / RJ  ")
dossie_master.append("**Data da Extração Integral:** 29/08/2026  \n")
dossie_master.append("---\n")

dossie_master.append("## 📋 1. MAPA GERAL DOS 4 PROCESSOS MAPEADOS NO TJRJ\n")

for num_cnj, desc in procs:
    p_dir = os.path.join(target_dir, "processos", num_cnj)
    os.makedirs(p_dir, exist_ok=True)
    
    # Check raw files
    g1_file = os.path.join(p_dir, "raw_G1.json")
    g2_file = os.path.join(p_dir, "raw_G2.json")
    
    dossie_master.append(f"### ⚖️ Processo CNJ: `{num_cnj}`")
    dossie_master.append(f"**Descrição:** {desc}  ")
    
    # Process G1 and G2 details
    for g_tag, f_path in [("1ª Instância (Origem)", g1_file), ("2ª Instância (TJRJ - Apelação)", g2_file)]:
        if os.path.exists(f_path):
            src = json.load(open(f_path, encoding="utf-8"))
            orgao = src.get("orgaoJulgador", {}).get("nome")
            classe = src.get("classe", {}).get("nome")
            dt = src.get("dataAjuizamento")
            assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
            movs = src.get("movimentos", [])
            movs_desc = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
            
            dossie_master.append(f"#### 🏛️ {g_tag}:")
            dossie_master.append(f"- **Órgão Julgador:** {orgao}")
            dossie_master.append(f"- **Classe:** {classe}")
            dossie_master.append(f"- **Assuntos:** {', '.join(assuntos)}")
            dossie_master.append(f"- **Data Ajuizamento:** {dt}")
            dossie_master.append(f"- **Total de Movimentações:** {len(movs)}")
            dossie_master.append(f"- **Último Andamento:** `{movs_desc[0].get('dataHora') if movs_desc else ''}` — **{movs_desc[0].get('nome') if movs_desc else 'N/A'}**\n")
            
            # Gerar arquivo individual de histórico completo
            ind_lines = [
                f"# 📜 HISTÓRICO COMPLETO: {num_cnj} ({g_tag})",
                f"- **Órgão:** {orgao} | **Classe:** {classe}",
                f"- **Assuntos:** {', '.join(assuntos)}\n",
                "## Movimentações Cronológicas:"
            ]
            for idx, m in enumerate(movs_desc, 1):
                dt_m = m.get("dataHora", "")[:19].replace("T", " ")
                comps = m.get("complementosTabelados", [])
                comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
                ind_lines.append(f"{idx}. **`{dt_m}`** — **{m.get('nome')}** (Cód. `{m.get('codigo')}`)" + (f" *({comp_str})*" if comp_str else ""))
                
            ind_path = os.path.join(p_dir, f"historico_{'1a_instancia' if '1ª' in g_tag else '2a_instancia'}.md")
            with open(ind_path, "w", encoding="utf-8") as f_ind:
                f_ind.write("\n".join(ind_lines))
                
    dossie_master.append("---\n")

# Seção de Execução Penal / VEP
dossie_master.append("""## ⛓️ 2. QUADRO DA EXECUÇÃO PENAL (VEP / SEEU)

Como as Ações Penais de Saquarema (`0800060-52.2023.8.19.0058` e `0800262-29.2023.8.19.0058`) e de Piraí (`0801082-93.2023.8.19.0043`) transitaram em julgado na 2ª Instância do TJRJ, as Cartas de Guia / Execução Definitiva foram remetidas à **Vara de Execuções Penais (VEP/RJ)** para unificação e cumprimento de pena.

### 🎯 Oportunidades Estratégicas na VEP / Execução:
1. **Pedido de Unificação de Penas por Continuidade Delitiva (Art. 66, III, 'a' da LEP c/c Art. 71 do CP):**
   - Os crimes de roubo foram praticados em condições de tempo, lugar e maneira de execução semelhantes no início de 2023 no Estado do RJ.
   - **Tese:** Pleitear perante o Juízo da VEP que as penas dos roubos sejam unificadas sob a regra da Continuidade Delitiva (aplicação da pena de um só crime com aumento de 1/6 a 2/3), afastando a soma simples do Concurso Material (Art. 69 do CP). Isso reduzirá anos da condenação total.
2. **Revisão e Cálculo do Lapso Temporal para Progressão de Regime (Art. 112 da LEP):**
   - Com a unificação, refazer a liquidação de penas para fixar a data-base para progressão ao **Regime Semiaberto** e **Livramento Condicional** (Art. 83 do CP).
3. **Detração Penal (Art. 42 do CP) e Remição de Pena (Art. 126 da LEP):**
   - Computar todo o período em que Rodrigo permaneceu preso cautelarmente/preventivamente desde o flagrante de janeiro de 2023, acrescido de dias trabalhados ou estudados na unidade prisional.
""")

master_md_file = os.path.join(target_dir, "DOSSIE_MASTER_RODRIGO_NOBREGA.md")
with open(master_md_file, "w", encoding="utf-8") as f:
    f.write("\n".join(dossie_master))

print(f"✅ Dossiê Master consolidado em: {master_md_file}")
