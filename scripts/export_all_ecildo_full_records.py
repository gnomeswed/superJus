# -*- coding: utf-8 -*-
import json
import os
import sys
import urllib.request
import fitz # PyMuPDF

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
base_dir = r"c:\Projetos\superJus\Clientes\Ecildo_Victor"
processos_dir = os.path.join(base_dir, "processos")
os.makedirs(processos_dir, exist_ok=True)

# 1. Definir lista de todos os processos de Ecildo
PROCESSOS = [
    {
        "numero": "1003524-57.2023.8.11.0015",
        "clean": "10035245720238110015",
        "vara": "1ª Vara Criminal - Comarca de Sinop/MT",
        "classe_esperada": "Ação Penal - Procedimento Ordinário / RESE (TJMT)",
        "assunto": "Furto Simples (Art. 155 do CP)",
        "tribunal": "tjmt"
    },
    {
        "numero": "1017084-03.2022.8.11.0015",
        "clean": "10170840320228110015",
        "vara": "2ª Vara Criminal - Comarca de Sinop/MT",
        "classe_esperada": "Ação Penal - Procedimento Ordinário",
        "assunto": "Furto Qualificado (Art. 155, § 4º do CP)",
        "tribunal": "tjmt"
    },
    {
        "numero": "1013261-21.2022.8.11.0015",
        "clean": "10132612120228110015",
        "vara": "1ª Vara Criminal - Comarca de Sinop/MT",
        "classe_esperada": "Ação Penal - Procedimento Ordinário",
        "assunto": "Furto Simples",
        "tribunal": "tjmt"
    },
    {
        "numero": "1014274-55.2022.8.11.0015",
        "clean": "10142745520228110015",
        "vara": "5ª Vara Criminal - Comarca de Sinop/MT",
        "classe_esperada": "Procedimento Especial da Lei Antitóxicos",
        "assunto": "Tráfico de Drogas e Condutas Afins (Art. 33)",
        "tribunal": "tjmt"
    },
    {
        "numero": "1011246-79.2022.8.11.0015",
        "clean": "10112467920228110015",
        "vara": "1ª Vara Criminal - Comarca de Sinop/MT",
        "classe_esperada": "Auto de Prisão em Flagrante",
        "assunto": "Furto",
        "tribunal": "tjmt"
    },
    {
        "numero": "1014036-36.2022.8.11.0015",
        "clean": "10140363620228110015",
        "vara": "4ª Vara Criminal - Comarca de Sinop/MT",
        "classe_esperada": "Ação Penal",
        "assunto": "Tráfico de Drogas",
        "tribunal": "tjmt"
    },
    {
        "numero": "1019059-60.2022.8.11.0015",
        "clean": "10190596020228110015",
        "vara": "Juizado Especial Cível e Criminal de Sinop/MT",
        "classe_esperada": "Termo Circunstanciado",
        "assunto": "Posse de Drogas para Consumo Pessoal (Art. 28)",
        "tribunal": "tjmt"
    }
]

print("=== INICIANDO EXTRAÇÃO TOTAL DE MOVIMENTAÇÕES, DECISÕES E DESPACHOS DE ECILDO ===")

# Extrair textos integrais dos PDFs locais para acoplar às decisões
pdf_texts = {}
for f in os.listdir(base_dir):
    if f.endswith(".pdf"):
        fp = os.path.join(base_dir, f)
        try:
            doc = fitz.open(fp)
            full_t = ""
            for p in doc:
                full_t += p.get_text() + "\n"
            pdf_texts[f] = full_t.strip()
            print(f"📄 PDF Processado: {f} ({len(doc)} págs)")
        except Exception as e:
            print(f"Erro no PDF {f}: {e}")

master_dossie_lines = []
master_dossie_lines.append("# 🏛️ DOSSIÊ MASTER DE TODOS OS PROCESSOS, DECISÕES E DESPACHOS")
master_dossie_lines.append("**Cliente:** Ecildo Victor dos Santos Ferreira  ")
master_dossie_lines.append("**CPF:** `080.730.972-90`  ")
master_dossie_lines.append("**Data de Extração Completa:** 29/08/2026  ")
master_dossie_lines.append("**Status Geral:** Preso Preventivamente no RJ (SEAP/RJ) | Alvará expedido prejudicado por outros mandados em MT.  \n")
master_dossie_lines.append("---\n")

for p_info in PROCESSOS:
    num = p_info["numero"]
    clean = p_info["clean"]
    vara = p_info["vara"]
    assunto = p_info["assunto"]
    tb = p_info["tribunal"]
    
    print(f"\n🚀 Consultando Processo {num} no DataJud ({tb.upper()})...")
    
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
    query = {
        "query": {
            "match": {
                "numeroProcesso": clean
            }
        },
        "size": 20
    }
    
    hits = []
    try:
        req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
    except Exception as e:
        print(f"  ❌ Erro ao consultar {num}: {e}")
        
    # Se DataJud não retornou hits mas já tínhamos cache local, usar cache
    p_folder = os.path.join(processos_dir, num)
    os.makedirs(p_folder, exist_ok=True)
    cache_json_path = os.path.join(p_folder, "detalhes_processo.json")
    
    raw_entries = []
    if hits:
        raw_entries = [h["_source"] for h in hits]
    elif os.path.exists(cache_json_path):
        try:
            cached = json.load(open(cache_json_path, encoding="utf-8"))
            raw_entries = cached.get("datajud_raw", [])
            print(f"  ℹ️ Usando cache local para {num} ({len(raw_entries)} graus/instâncias)")
        except Exception:
            pass
            
    # Salvar JSON detalhado
    process_json_data = {
        "metadados": p_info,
        "total_instancias": len(raw_entries),
        "datajud_raw": raw_entries
    }
    with open(os.path.join(p_folder, "dados_completos_datajud.json"), "w", encoding="utf-8") as f:
        json.dump(process_json_data, f, ensure_ascii=False, indent=2)
        
    # Processar todas as movimentações e separar decisões/despachos
    all_movements_combined = []
    decisoes_e_despachos = []
    
    for entry in raw_entries:
        grau = entry.get("grau", "G1")
        orgao = entry.get("orgaoJulgador", {}).get("nome", vara)
        classe = entry.get("classe", {}).get("nome", p_info["classe_esperada"])
        movs = entry.get("movimentos", [])
        
        for m in movs:
            cod = m.get("codigo")
            dt = m.get("dataHora", "")
            nome = m.get("nome", "")
            comps = m.get("complementosTabelados", [])
            comp_list = []
            for c in comps:
                d = c.get("descricao", "")
                n = c.get("nome", "")
                comp_list.append(f"**{d}:** {n}")
            comp_str = " | ".join(comp_list)
            
            is_decision = any(k in nome.lower() or k in comp_str.lower() for k in [
                "decisão", "decisao", "despacho", "sentença", "sentenca", "provimento",
                "mandado", "prisão", "prisao", "preventiva", "alvará", "alvara",
                "audiência", "audiencia", "conclusão para decisão", "conclusão para despacho",
                "citação", "citacao", "edital", "revel", "recambiamento", "366"
            ])
            
            mov_dict = {
                "grau": grau,
                "orgao": orgao,
                "classe": classe,
                "codigo": cod,
                "dataHora": dt,
                "nome": nome,
                "complementos": comp_str,
                "is_decision": is_decision
            }
            all_movements_combined.append(mov_dict)
            if is_decision:
                decisoes_e_despachos.append(mov_dict)
                
    # Ordenar movimentações descrescente (da mais recente para a mais antiga)
    all_movements_combined = sorted(all_movements_combined, key=lambda x: x["dataHora"], reverse=True)
    decisoes_e_despachos = sorted(decisoes_e_despachos, key=lambda x: x["dataHora"], reverse=True)
    
    print(f"  ✅ {num}: Total de {len(all_movements_combined)} movimentações | {len(decisoes_e_despachos)} decisões/despachos/atos-chave.")
    
    # Gerar Markdown Completo do Processo
    p_md_lines = []
    p_md_lines.append(f"# 📂 PROCESSO: {num}")
    p_md_lines.append(f"- **Vara / Juízo:** {vara}")
    p_md_lines.append(f"- **Assunto:** {assunto}")
    p_md_lines.append(f"- **Total de Movimentações Registradas:** {len(all_movements_combined)}")
    p_md_lines.append(f"- **Total de Despachos / Decisões / Atos Críticos:** {len(decisoes_e_despachos)}\n")
    
    p_md_lines.append("## ⚖️ 1. SELEÇÃO DE DECISÕES, DESPACHOS E ATOS CRÍTICOS")
    if decisoes_e_despachos:
        for idx, d in enumerate(decisoes_e_despachos, 1):
            dt_fmt = d['dataHora'][:19].replace("T", " ")
            p_md_lines.append(f"### {idx}. [{dt_fmt}] — {d['nome']} ({d['grau']} - {d['orgao']})")
            if d['complementos']:
                p_md_lines.append(f"- **Detalhes/Classificação:** {d['complementos']}")
            p_md_lines.append(f"- **Código CNJ:** `{d['codigo']}`\n")
    else:
        p_md_lines.append("*(Nenhum despacho judicial autônomo individualizado no DataJud)*\n")
        
    p_md_lines.append("## 📜 2. HISTÓRICO CRONOLÓGICO COMPLETO DE TODAS AS MOVIMENTAÇÕES")
    for idx, m in enumerate(all_movements_combined, 1):
        dt_fmt = m['dataHora'][:19].replace("T", " ")
        p_md_lines.append(f"{idx}. **`{dt_fmt}`** | **{m['nome']}** | *{m['grau']} - {m['orgao']}*")
        if m['complementos']:
            p_md_lines.append(f"   ↳ {m['complementos']}")
            
    # Se houver textos de decisões em PDF para este processo, anexar
    if num == "1003524-57.2023.8.11.0015":
        p_md_lines.append("\n## 📑 3. ÍNTEGRA DAS DECISÕES JUDICIAIS EXTRAÍDAS DOS AUTOS (PDFs OFICIAIS)")
        for pdf_name, pdf_content in pdf_texts.items():
            if "1003524" in pdf_name:
                p_md_lines.append(f"\n### 📝 Decisão / Documento: `{pdf_name}`")
                p_md_lines.append("```text")
                p_md_lines.append(pdf_content[:3000] + ("\n... [Trecho sintetizado para o dossiê]" if len(pdf_content) > 3000 else ""))
                p_md_lines.append("```\n")
                
    p_md_file = os.path.join(p_folder, "historico_completo_movimentacoes_e_decisoes.md")
    with open(p_md_file, "w", encoding="utf-8") as f:
        f.write("\n".join(p_md_lines))
        
    # Adicionar ao Master Dossiê
    master_dossie_lines.append(f"## 📁 Processo: `{num}` — {assunto}")
    master_dossie_lines.append(f"**Vara:** {vara} | **Movimentações:** {len(all_movements_combined)} | **Decisões/Despachos:** {len(decisoes_e_despachos)}")
    master_dossie_lines.append(f"**Arquivo Individual Detalhado:** [{num}/historico_completo_movimentacoes_e_decisoes.md](file:///{p_md_file.replace(chr(92), '/')})\n")
    
    if decisoes_e_despachos:
        master_dossie_lines.append("### Principais Decisões e Movimentos de Risco Cautelar:")
        for d in decisoes_e_despachos[:6]:
            dt_fmt = d['dataHora'][:10]
            master_dossie_lines.append(f"- **`{dt_fmt}`** | **{d['nome']}** {('— ' + d['complementos']) if d['complementos'] else ''}")
    master_dossie_lines.append("\n---\n")

master_file = os.path.join(base_dir, "DOSSIE_MASTER_TODOS_PROCESSOS_ECILDO.md")
with open(master_file, "w", encoding="utf-8") as f:
    f.write("\n".join(master_dossie_lines))

print(f"\n🎉 SUCESSO TOTAL! Todos os processos foram extraídos, categorizados e salvos!")
print(f"📌 Master Dossiê salvo em: {master_file}")
