# -*- coding: utf-8 -*-
"""
Script de Cadastro e Extração Completa — Daniel Ferreira Lima
Processo: 0004301-33.2018.8.19.0073 (Guapimirim / TJRJ)
"""
import os
import json
import time
import requests
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

CLIENT_DIR = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima"
SUBDIRS = [
    os.path.join(CLIENT_DIR, "01_Dados_do_Cliente"),
    os.path.join(CLIENT_DIR, "02_Movimentacoes"),
    os.path.join(CLIENT_DIR, "03_Documentos_do_Processo"),
    os.path.join(CLIENT_DIR, "04_Analises_e_Estrategias"),
    os.path.join(CLIENT_DIR, "Caso_Principal", "analises"),
    os.path.join(CLIENT_DIR, "Caso_Principal", "documentos_processo"),
    os.path.join(CLIENT_DIR, "Caso_Principal", "pecas")
]

for d in SUBDIRS:
    os.makedirs(d, exist_ok=True)

print(f"Estrutura de pastas criada em: {CLIENT_DIR}")

# 1. Obter dados integrais do DataJud
DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

proc_num = "0004301-33.2018.8.19.0073"
proc_clean = "00043013320188190073"

print(f"\nConsultando DataJud para o processo {proc_num}...")
resp = requests.post(BASE_TJRJ, headers=HEADERS, json={
    "query": {"match": {"numeroProcesso": proc_clean}},
    "size": 10
}, timeout=30)

if resp.status_code == 200:
    hits = resp.json().get("hits", {}).get("hits", [])
    print(f"Total de instâncias encontradas no DataJud: {len(hits)}")
    
    instancias_data = []
    
    for idx, hit in enumerate(hits):
        src = hit.get("_source", {})
        inst_nome = src.get("orgaoJulgador", {}).get("nome", f"Instancia_{idx+1}")
        classe_nome = src.get("classe", {}).get("nome", "Classe_NI")
        safe_name = f"{idx+1}_{inst_nome.replace(' ', '_')}_{classe_nome.replace(' ', '_')}"
        
        # Salvar JSON raw
        raw_json_path = os.path.join(CLIENT_DIR, "02_Movimentacoes", f"datajud_raw_{safe_name}.json")
        with open(raw_json_path, "w", encoding="utf-8") as f:
            json.dump(src, f, indent=2, ensure_ascii=False)
            
        movs = sorted(src.get("movimentos", []), key=lambda m: m.get("dataHora", ""), reverse=True)
        print(f"  [{idx+1}] {inst_nome} | {classe_nome} | {len(movs)} movimentos salvos em {raw_json_path}")
        
        # Gerar Markdown formatado de movimentações
        md_movs_path = os.path.join(CLIENT_DIR, "02_Movimentacoes", f"movimentacoes_{safe_name}.md")
        with open(md_movs_path, "w", encoding="utf-8") as f:
            f.write(f"# Movimentações Processuais — {proc_num}\n\n")
            f.write(f"- **Órgão Julgador:** {inst_nome}\n")
            f.write(f"- **Classe Processual:** {classe_nome} (Cód. {src.get('classe', {}).get('codigo')})\n")
            f.write(f"- **Assuntos:** {', '.join([a.get('nome','') for a in src.get('assuntos', [])])}\n")
            f.write(f"- **Data de Ajuizamento:** {src.get('dataAjuizamento', '')}\n")
            f.write(f"- **Última Atualização:** {src.get('dataHoraUltimaAtualizacao', '')}\n")
            f.write(f"- **Total de Movimentações:** {len(movs)}\n\n")
            f.write("## Histórico Cronológico Decrescente\n\n")
            f.write("| Data/Hora | Código | Movimento | Detalhes / Complementos |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")
            for m in movs:
                dt = m.get("dataHora", "")[:19].replace("T", " ")
                cod = m.get("codigo", "")
                nm = m.get("nome", "")
                comps = m.get("complementosTabelados", [])
                comp_txt = "; ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) if comps else "-"
                f.write(f"| {dt} | {cod} | {nm} | {comp_txt} |\n")
        print(f"    Markdown gerado: {md_movs_path}")
else:
    print(f"Erro no DataJud: {resp.status_code}")

# 2. Criar Ficha Cadastral do Cliente
ficha_path = os.path.join(CLIENT_DIR, "01_Dados_do_Cliente", "ficha_cadastral_daniel.md")
with open(ficha_path, "w", encoding="utf-8") as f:
    f.write("""# FICHA CADASTRAL DO CLIENTE — SUPERJUS

## 👤 Dados Pessoais e Identificação
- **Nome Completo:** Daniel Ferreira Lima
- **Cliente:** Daniel Ferreira Lima
- **Status Processual:** Réu / Recorrente
- **Situação Cautelar:** Condenado em 1ª Instância no Tribunal do Júri (18/05/2026); Autos remetidos ao TJRJ em grau de Apelação (15/06/2026).

## ⚖️ Mapeamento Processual
- **Processo Principal:** `0004301-33.2018.8.19.0073`
- **Comarca / Juízo:** Comarca de Guapimirim / RJ — 2ª Vara (Tribunal do Júri)
- **Classe:** Ação Penal de Competência do Júri (Cód. 282)
- **Imputação Penal:** Homicídio Qualificado (Artigo 121, § 2º do Código Penal) / Homicídio Simples (Cód. 3370/3372) e Aplicação da Pena (Cód. 10621).
- **Data da Distribuição:** 03/05/2018
- **2ª Instância (TJRJ):** Recurso em Sentido Estrito julgado pela Desª Márcia Perrini Bodart em 2025 (Não-Provimento); Atual Recurso de Apelação Criminal remetido em 15/06/2026.

## 🎯 Marco Histórico Relevante
1. **03/05/2018:** Distribuição da Ação Penal pelo MPRJ na 2ª Vara de Guapimirim.
2. **22/05/2025:** Julgamento do RESE no TJRJ mantendo a pronúncia ao Tribunal do Júri.
3. **18/05/2026 (13:00h às 21:03h):** Sessão do Tribunal do Júri realizada na 2ª Vara de Guapimirim com julgamento de procedência (condenação).
4. **15/06/2026:** Remessa dos autos ao TJRJ em grau de recurso de Apelação Criminal.
""")
print(f"Ficha cadastral gerada em: {ficha_path}")

# 3. Criar Dossiê Inicial e Roteiro de Auditoria
dossie_path = os.path.join(CLIENT_DIR, "04_Analises_e_Estrategias", "dossie_inicial_homicidio_daniel.md")
with open(dossie_path, "w", encoding="utf-8") as f:
    f.write("""# DOSSIÊ ESTRATÉGICO INICIAL — DANIEL FERREIRA LIMA
**Processo:** `0004301-33.2018.8.19.0073` | **Comarca:** Guapimirim / RJ (2ª Vara)  
**Assunto:** Homicídio Qualificado (Art. 121, § 2º, CP) | **Fase Atual:** Apelação Criminal no TJRJ (Remessa em 15/06/2026)

---

## 📌 1. Visão Geral do Caso
O cliente Daniel Ferreira Lima foi submetido a julgamento perante o Tribunal do Júri da Comarca de Guapimirim em **18 de maio de 2026**, tendo a sessão se estendido das 13:00h até as 21:03h, quando foi proferida a sentença condenatória (Movimento 219).
Em **15 de junho de 2026**, a defesa formalizou a remessa dos autos ao Tribunal de Justiça do Rio de Janeiro (TJRJ) em grau de **Apelação Criminal (Art. 593, III do CPP)**.

---

## 🎯 2. Linhas de Ação e Auditoria da Banca

### A. Nulidades em Plenário e Ata do Júri (Art. 593, III, 'a', CPP c/c Art. 564 CPP)
- Auditar a Ata de Julgamento da Sessão do Júri de 18/05/2026.
- Checar se houve protesto formal da defesa quanto à quebra de incomunicabilidade dos jurados, uso indevido de argumentos de autoridade pelo Ministério Público (*argumentum ad verecundiam* - menção à pronúncia ou silêncio do réu como presunção de culpa, Art. 478 do CPP).
- Verificar defeito na elaboração dos quesitos (Art. 482 e 483 do CPP).

### B. Veredito Manifestamente Contrário à Prova dos Autos (Art. 593, III, 'd', CPP)
- Avaliar se a tese acusatória acolhida pelos jurados encontra amparo mínimo em provas judicializadas ou se decorreu exclusivamente de presunções da fase inquisitorial policial (violação ao Art. 155 do CPP).

### C. Erro ou Injustiça na Aplicação da Pena — Dosimetria (Art. 593, III, 'c', CPP)
- Auditar a sentença proferida pelo Juiz Presidente na noite de 18/05/2026.
- Avaliar vetores do Art. 59 do Código Penal: se a pena-base foi elevada com fundamentação abstrata ou inerente ao próprio tipo do homicídio.
- Checar atenuantes (confissão espontânea, menoridade relativa ou provocação da vítima) e compensação legal na 2ª fase.
- Verificar causas de aumento e incidência de qualificadoras.

---

## 📋 3. Próximos Passos
1. Obter a cópia integral da Ata de Julgamento da sessão plenária de 18/05/2026 e a sentença condenatória.
2. Acompanhar a distribuição da Apelação Criminal na 2ª Instância do TJRJ (Câmaras Criminais).
3. Elaborar/aditar Razões de Apelação com foco em anulação do julgamento ou redução drástica da pena privativa de liberdade.
""")
print(f"Dossiê gerado em: {dossie_path}")

print("\n=== CADASTRO E EXTRAÇÃO CONCLUÍDOS COM SUCESSO ===")
