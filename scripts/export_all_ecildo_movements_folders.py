# -*- coding: utf-8 -*-
import os
import json
import urllib.request
import re
from datetime import datetime

DATAJUD_API_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
BASE_DIR = r"c:\Projetos\Super Analista Jurídico\Clientes\ecildo\processos"

processes_info = [
    {
        "numero": "1003524-57.2023.8.11.0015",
        "clean": "10035245720238110015",
        "vara": "1ª Vara Criminal - Comarca de Sinop/MT",
        "classe": "Ação Penal - Procedimento Ordinário",
        "assunto": "Furto Simples (Art. 155, CP)",
        "status": "ATIVO (Em tramitação - Mandado / Recambiamento)"
    },
    {
        "numero": "1017084-03.2022.8.11.0015",
        "clean": "10170840320228110015",
        "vara": "2ª Vara Criminal - Comarca de Sinop/MT",
        "classe": "Ação Penal - Procedimento Ordinário",
        "assunto": "Furto Qualificado (Art. 155, § 4º, CP)",
        "status": "ATIVO (Reativado em 17/07/2025)"
    },
    {
        "numero": "1013261-21.2022.8.11.0015",
        "clean": "10132612120228110015",
        "vara": "1ª Vara Criminal - Comarca de Sinop/MT",
        "classe": "Ação Penal - Procedimento Ordinário",
        "assunto": "Furto Simples",
        "status": "ATIVO / SUSPENSO (Art. 366 do CPP)"
    },
    {
        "numero": "1014274-55.2022.8.11.0015",
        "clean": "10142745520228110015",
        "vara": "5ª Vara Criminal - Comarca de Sinop/MT",
        "classe": "Procedimento Especial da Lei Antitóxicos",
        "assunto": "Tráfico de Drogas e Condutas Afins",
        "status": "INATIVO (Arquivado Provisoriamente em 03/05/2025)"
    },
    {
        "numero": "1019059-60.2022.8.11.0015",
        "clean": "10190596020228110015",
        "vara": "Juizado Especial Cível e Criminal de Sinop/MT",
        "classe": "Termo Circunstanciado",
        "assunto": "Posse de Drogas para Consumo Pessoal (Art. 28)",
        "status": "INATIVO (Arquivado Definitivamente em 27/03/2023)"
    },
    {
        "numero": "1014036-36.2022.8.11.0015",
        "clean": "10140363620228110015",
        "vara": "4ª Vara Criminal - Comarca de Sinop/MT",
        "classe": "Auto de Prisão em Flagrante",
        "assunto": "Tráfico de Drogas",
        "status": "INATIVO (Arquivado Definitivamente em 22/08/2022)"
    },
    {
        "numero": "1011246-79.2022.8.11.0015",
        "clean": "10112467920228110015",
        "vara": "1ª Vara Criminal - Comarca de Sinop/MT",
        "classe": "Auto de Prisão em Flagrante",
        "assunto": "Furto",
        "status": "INATIVO (Arquivado Definitivamente em 19/08/2022)"
    }
]

os.makedirs(BASE_DIR, exist_ok=True)

# Load DataJud dump if exists or fetch
def get_datajud_process(clean_num):
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjmt/_search"
    headers = {
        "Authorization": DATAJUD_API_KEY,
        "Content-Type": "application/json"
    }
    query = {"query": {"match": {"numeroProcesso": clean_num}}, "size": 10}
    req = urllib.request.Request(url, data=json.dumps(query).encode('utf-8'), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            hits = data.get('hits', {}).get('hits', [])
            return [h['_source'] for h in hits]
    except Exception as e:
        print(f"Error fetching {clean_num}: {e}")
        return []

# Read dossier PDF text for supplementary records
with open(r"c:\Projetos\Super Analista Jurídico\scripts\pdf_dossie_text.txt", "r", encoding="utf-8") as f:
    pdf_text = f.read()

for p in processes_info:
    num = p["numero"]
    clean = p["clean"]
    p_dir = os.path.join(BASE_DIR, num)
    os.makedirs(p_dir, exist_ok=True)
    
    print(f"\nProcessing {num} -> Folder: {p_dir}")
    
    sources = get_datajud_process(clean)
    
    # Save raw json
    with open(os.path.join(p_dir, "detalhes_processo.json"), "w", encoding="utf-8") as f:
        json.dump({
            "metadados": p,
            "datajud_raw": sources
        }, f, ensure_ascii=False, indent=2)
    
    # Build movimentacoes_completas.md
    md_content = f"# Histórico Completo de Movimentações - Processo {num}\n\n"
    md_content += f"**Réu:** Ecildo Victor dos Santos Ferreira (CPF: 080.730.972-90)\n"
    md_content += f"**Juízo:** {p['vara']}\n"
    md_content += f"**Classe:** {p['classe']}\n"
    md_content += f"**Assunto:** {p['assunto']}\n"
    md_content += f"**Status:** {p['status']}\n\n"
    md_content += "---\n\n## Movimentações Registradas\n\n"
    
    all_movs = []
    if sources:
        for s in sources:
            instancia = "2ª Instância (TJMT)" if s.get('grau') == 'G2' or 'Câmara' in s.get('orgaoJulgador', {}).get('nome', '') else "1ª Instância"
            movs = s.get('movimentos', [])
            for m in movs:
                dt_raw = m.get('dataHora', '')
                dt_fmt = dt_raw
                if len(dt_raw) >= 10:
                    parts = dt_raw[:10].split('-')
                    dt_fmt = f"{parts[2]}/{parts[1]}/{parts[0]}"
                
                name = m.get('nome', 'Sem descrição')
                comps = m.get('complementosTabelados', [])
                comp_strs = []
                for c in comps:
                    if isinstance(c, dict):
                        comp_strs.append(f"{c.get('nome', '')}: {c.get('valor', '')}")
                comp_text = " (" + ", ".join(comp_strs) + ")" if comp_strs else ""
                
                all_movs.append({
                    "data_raw": dt_raw,
                    "data_fmt": dt_fmt,
                    "instancia": instancia,
                    "descricao": name + comp_text,
                    "orgao": m.get('orgaoJulgador', {}).get('nome', s.get('orgaoJulgador', {}).get('nome', ''))
                })
    
    # Sort reverse chronological
    all_movs_sorted = sorted(all_movs, key=lambda x: x['data_raw'], reverse=True)
    
    if all_movs_sorted:
        for idx, m in enumerate(all_movs_sorted, 1):
            md_content += f"### {idx}. {m['data_fmt']} - {m['descricao']}\n"
            md_content += f"- **Instância/Órgão:** {m['instancia']} | {m['orgao']}\n"
            md_content += f"- **Data/Hora Oficial:** `{m['data_raw']}`\n\n"
    else:
        md_content += "_Nenhuma movimentação pública retornada pela API do DataJud para este número. Consultando registros históricos locais..._\n\n"
        # Extract from dossier text for this process
        proc_regex = re.escape(num)
        pos = pdf_text.find(num)
        if pos != -1:
            snippet = pdf_text[pos:pos+2500]
            md_content += f"```text\n{snippet}\n```\n\n"
    
    # Write movimentacoes_completas.md
    with open(os.path.join(p_dir, "movimentacoes_completas.md"), "w", encoding="utf-8") as f:
        f.write(md_content)
        
    # Write analise_situacao.md
    analise_md = f"# Análise de Situação e Riscos - Processo {num}\n\n"
    analise_md += f"## 1. Diagnóstico do Caso\n"
    if "1003524" in num:
        analise_md += (
            "Este é o **processo criminal principal** (Ação Penal de Furto). "
            "A prisão preventiva foi decretada pela 3ª Câmara Criminal do TJMT (RESE) em razão da não localização de Ecildo em Sinop/MT. "
            "Recentemente, Ecildo foi preso no Estado do Rio de Janeiro. "
            "O juízo da 1ª Vara Criminal de Sinop expediu ofício requerendo o seu recambiamento para o Mato Grosso. "
            "Em 16/06/2026 houve juntada de petição e o processo encontra-se **concluso para decisão desde 17/06/2026**.\n\n"
            "### A Justiça de MT sabe que ele está preso no RJ?\n"
            "**Sim.** A juíza da 1ª Vara Criminal de Sinop expediu ofício solicitando o recambiamento de Ecildo à Policial Penal/SEAP do RJ. "
            "Contudo, é **extremamente urgente que a Defesa peticione nos autos** informando o local exato da custódia no RJ, "
            "pedindo a revogação da prisão preventiva ou a substituição por medidas cautelares (tornozeleira eletrônica no RJ), "
            "demonstrando que ele possui residência fixada no RJ e que a transferência física para MT trará prejuízos à sua integridade e custos desnecessários.\n"
        )
    elif "1017084" in num:
        analise_md += (
            "Processo ativo de **Furto Qualificado** na 2ª Vara Criminal de Sinop. "
            "O processo foi **reativado em 17/07/2025** e teve mandado de prisão juntado em 23/07/2025. "
            "A Defesa precisa peticionar neste feito para informar a prisão do réu no RJ e evitar decretação de nova ordem de prisão por contumácia.\n"
        )
    elif "1013261" in num:
        analise_md += (
            "Processo **suspenso com base no Art. 366 do CPP** na 1ª Vara Criminal de Sinop. "
            "Como o réu está preso, a Defesa deve requerer a **habilitação nos autos e citação pessoal no presídio**, "
            "para que o processo retome seu curso regular e desfaça a suspensão da prescrição.\n"
        )
    else:
        analise_md += (
            "Processo inativo ou arquivado (ou Termo Circunstanciado/APF). "
            "Não há risco iminente de nova ordem de prisão oriunda deste feito, pois já se encontra encerrado/arquivado.\n"
        )
    
    with open(os.path.join(p_dir, "analise_situacao.md"), "w", encoding="utf-8") as f:
        f.write(analise_md)

print("\nConcluído exportação e criação de todas as pastas!")
