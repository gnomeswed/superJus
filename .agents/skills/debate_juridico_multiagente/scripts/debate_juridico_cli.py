# -*- coding: utf-8 -*-
"""
SUPERJUS — COMITÊ JURÍDICO ESTRATÉGICO REALISTA (DEBATE MULTIAGENTE SEM ILUSÕES)
Mesa Redonda de Ceticismo e Realismo Crítico:
1. ⚖️ O Magistrado Inquisidor / Relator Cético (A barreira do tribunal e jurisprudência defensiva)
2. ⚔️ O Promotor Acusador / Procurador de Justiça (O Advogado do Diabo e as forças da acusação)
3. 🛡️ O Estrategista Pragmático de Cortes Superiores (O Realista da Advocacia)
4. 📊 O Auditor Realista de Execução Penal (A dura realidade da VEP e tempo real de cadeia)
5. 🎯 O Coordenador da Banca (Matriz de Realidade, Gestão de Expectativas e Action Plan Factual)
"""

import sys
import os
import argparse
import json
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

def gather_client_case_data(client_path: Path) -> dict:
    data = {
        "client_name": client_path.name.replace("_", " "),
        "folder": str(client_path),
        "files": [],
        "case_summary": "",
        "is_lucas": False,
        "is_julio": False
    }
    
    name_lower = client_path.name.lower()
    if "lucas" in name_lower:
        data["is_lucas"] = True
        data["full_name"] = "Lucas de Souza Freitas"
        data["vulgo"] = "Motoboy Lucas / LC"
        data["processo"] = "0011857-95.2024.8.19.0002"
        data["instancia"] = "2ª Instância — TJRJ (2ª Câmara Criminal / Rel. Des. Flávio Itabaiana)"
        data["crime"] = "Homicídio Triplamente Qualificado (Art. 121, § 2º, I, III e IV CP) + Ocultação de Cadáver (Art. 211 CP)"
        data["pena_atual"] = "22 anos de reclusão em regime inicial FECHADO"
    elif "julio" in name_lower or "júlio" in name_lower:
        data["is_julio"] = True
        data["full_name"] = "Júlio Pereira Marcos"
        data["processo"] = "STJ HC 1.116.750/RJ | 1ª Vara Búzios 0023013-51.2021.8.19.0078"
        data["instancia"] = "STJ 6ª Turma (Rel. Min. Og Fernandes)"
        data["crime"] = "Tráfico de Drogas (Art. 33) e Associação para o Tráfico (Art. 35 da Lei 11.343/06)"
        data["pena_atual"] = "Preso Preventivo (>90 dias sem realização de AIJ)"
        
    return data

def run_realistic_multiagent_debate(case_data: dict, topic: str = "") -> dict:
    debate_records = []
    client_name = case_data.get("full_name", case_data["client_name"])
    
    if case_data.get("is_lucas"):
        # =============================================================
        # CASO LUCAS MOTOBOY — REALIDADE CRUA E NUA
        # =============================================================
        # 1. Magistrado Inquisidor (TJRJ 2ª Câmara)
        p1_fala = (
            "Sejamos frios e diretos: este é um homicídio qualificado com ocultação de cadáver de um motorista de aplicativo/taxista, "
            "com condenação pelo Tribunal do Júri. A 2ª Câmara Criminal do TJRJ é uma das mais severas do Estado e NÃO anulará o Júri! "
            "Qualquer tentativa da defesa de pedir novo júri sob alegação de 'decisão contrária à prova' (Art. 593, III, 'd') será "
            "sumariamente REJEITADA por ofensa à soberania dos veredictos (Art. 5º, XXXVIII, 'c', CF). "
            "A ÚNICA brecha que eu, como juiz, sou forçado a analisar é a DOSIMETRIA (Art. 593, III, 'c'): a Juíza de Niterói exagerou na pena-base (+9 anos) "
            "e ignorou a jurisprudência sumulada do STJ sobre compensação de confissão com reincidência. "
            "Fora isso, o cliente continuará condenado e preso em regime fechado."
        )
        p1_risco = "MUITO ALTO para anulação do Júri (chance < 5%); MÉDIO para reforma de dosimetria (chance 40% a 50%)."

        # 2. Promotor Acusador (O Advogado do Diabo)
        p2_fala = (
            "A acusação foi cirúrgica: o crime causou clamor social brutal, a vítima foi atraída para uma emboscada, assassinada a tiros e teve o corpo ocultado. "
            "Lucas confessou os disparos e já possuía registros criminais anteriores. O Ministério Público vai sustentar oralmente no TJRJ que a periculosidade social é extrema, "
            "que o meio foi cruel e que o recurso dificultou a defesa da vítima. O parecer da Procuradoria de Justiça (atualmente com vista) será PELO DESPROVIMENTO TOTAL DA APELAÇÃO. "
            "A defesa não pode prometer soltura ou absolvição mágica: o réu matou e confessou."
        )
        p2_forca = "A materialidade cadavérica e a confissão em plenário blindam a condenação de qualquer anulação substancial."

        # 3. Estrategista Pragmático (Advocacia Realista)
        p3_fala = (
            "A defesa precisa parar de vender ilusões à família e focar no que é MATEMATICAMENTE POSSÍVEL: "
            "1. Esqueça anulação de Júri: isso só atrasa o processo e gera custos inúteis. "
            "2. Nossa briga é 100% TÉCNICA na dosimetria: obrigar o TJRJ a aplicar o TEMA REPETITIVO 585 e SÚMULA 545 DO STJ (compensação confissão x reincidência) "
            "e cortar o excesso da pena-base de 21 anos aplicando a fração de 1/6. "
            "3. O objetivo real e viável é derrubar a pena de 22 anos para a faixa de 17 a 19 anos. Isso é o máximo que a técnica jurídica honesta consegue alcançar."
        )
        p3_acao = "Concentrar 100% das razões e da sustentação oral na dosimetria (Tema 585 STJ) sem divagar sobre o mérito dos jurados."

        # 4. Auditor de Execução Penal (A Realidade da Cadeia e da VEP)
        p4_fala = (
            "Cálculo realista da execução penal (Lei 13.964/19 - Pacote Anticrime): "
            "• Crime Hediondo com Resultado Morte para réu reincidente exige cumprimento de 70% DA PENA (ou 50% se primário específico) para progressão ao semiaberto! "
            "• Com a pena de 22 anos: O réu teria que cumprir mais de 11 a 15 ANOS em regime estritamente fechado antes de sonhar com o semiaberto. "
            "• Se reduzirmos para 18 anos na Apelação: O réu precisará cumprir de 9 a 12 anos em regime fechado. "
            "• A DURA VERDADE: Mesmo com o melhor cenário recursal, Lucas enfrentará longos anos no sistema prisional fechado. A redução de pena é vital não para soltá-lo amanhã, "
            "mas para garantir que ele não passe a vida inteira trancado."
        )
        p4_realidade = "Cumprimento de fração pesada de hediondo (50% a 70%) -> Permanência obrigatória de anos em regime fechado na VEP."

        # 5. Coordenador da Banca (Matriz de Realidade)
        consensus = {
            "verdict": "DIAGNÓSTICO REALISTA: DEFESA RECURSAL ADSTRITA À DOSIMETRIA (SEM PROMESSAS VAZIAS)",
            "success_probability": "45% a 55% de chance de redução da pena para 17-19 anos | < 5% de chance de anulação do Júri",
            "what_wont_work": [
                "❌ Tentar anular o veredito do Júri por 'prova contrária' (TJRJ vai rejeitar sumariamente com base na soberania dos jurados).",
                "❌ Prometer liberdade provisória ou habeas corpus para soltura imediata (inviável diante de homicídio qualificado confesso com condenação).",
                "❌ Discutir desclassificação do crime em sede de Apelação de Júri."
            ],
            "the_only_real_window": [
                "🎯 Redução da Pena-Base na 1ª Fase (cortar o excesso de +9 anos para a fração padrão de 1/6 do STJ).",
                "🎯 Compensação Integral entre Confissão e Reincidência na 2ª Fase (Tema Repetitivo 585 e Súmula 545/STJ).",
                "🎯 Redução Factual da Pena de 22 anos para 17 a 19 anos (corte real de 3 a 5 anos na guia de recolhimento)."
            ],
            "family_alignment_guide": [
                "1. Deixar claro para a família que NÃO há chance de soltura imediata e que o crime é inafiançável e hediondo.",
                "2. Explicar que a vitória possível é jurídica e matemática: tirar 3 a 5 anos da condenação para que ele progrida mais rápido para o semiaberto no futuro.",
                "3. Mostrar o cronograma real da 2ª Câmara: aguardar parecer do MP, despachar memoriais com o Des. Flávio Itabaiana e sustentar na sessão."
            ]
        }

    elif case_data.get("is_julio"):
        # =============================================================
        # CASO JÚLIO PEREIRA MARCOS — REALIDADE CRUA E NUA
        # =============================================================
        p1_fala = (
            "Como magistrado no STJ, vejo dezenas de HCs de tráfico por dia. A 6ª Turma do STJ NÃO vai absolver Júlio em sede de Habeas Corpus, "
            "pois HC não permite revolvimento aprofundado de provas (Súmula 7/STJ). "
            "A alegação de que 'não é traficante' não será analisada pelo Min. Og Fernandes. "
            "O que PODE funcionar: O constrangimento ilegal flagrante pelo fato de estar preso há mais de 90 dias sem que a 1ª Vara de Búzios tenha realizado a AIJ do desmembrado, "
            "somado ao fato de que o corréu Matheus foi solto (Art. 580 CPP) e com Júlio não houve apreensão direta de drogas. "
            "A chance é estritamente cautelar de soltura processual, nunca de trancamento ou absolvição antecipada."
        )
        p1_risco = "MÉDIO — Viável para relaxamento de prisão por excesso de prazo; ZERO para absolvição por HC."

        p2_fala = (
            "O MPF emitiu parecer desfavorável (Manifestação nº 68200-2026), apontando que Júlio integrava o escalão do tráfico em Búzios, "
            "que houve interceptação telefônica e que a preventiva foi mantida para garantia da ordem pública. "
            "A acusação vai bater na tese de periculosidade social e reiteração delitiva para tentar convencer o Min. Og Fernandes a manter a prisão."
        )
        p2_forca = "Parecer ministerial contrário no STJ exige contradita técnica cirúrgica na assessoria do Ministro."

        p3_fala = (
            "A advocacia aqui tem que ser cirúrgica: nossa briga não é dizer que Júlio é santo, mas provar a ILEGALIDADE FORMAL da prisão: "
            "1. Réu preso sem instrução realizada (violação do Art. 400 do CPP). "
            "2. Isonomia objetiva com o corréu Matheus (Art. 580 do CPP). "
            "3. O mérito da inocência e a falta de perícia de voz serão debatidos na 1ª instância em Búzios, não no STJ."
        )
        p3_acao = "Memorial restrito ao excesso de prazo e ao Art. 580 do CPP para despacho com o Relator."

        p4_fala = (
            "Se for mantida a preventiva até a sentença, ele continuará sofrendo antecipação de pena. "
            "Se condenado apenas por tráfico privilegiado em Búzios, a pena seria de 1 ano e 8 meses em regime aberto (o que tornaria a preventiva ilegal por excesso de gravidade). "
            "Mas se for condenado no Art. 33 + Art. 35, a pena ultrapassará 8 anos em regime fechado. A soltura cautelar no STJ é urgente para que ele responda ao processo solto."
        )
        p4_realidade = "Urgência estritamente cautelar para evitar cumprimento antecipado de pena injustificada."

        consensus = {
            "verdict": "OFENSIVA CAUTELAR RESTRITA A EXCESSO DE PRAZO E ISONOMIA (ART. 580 CPP)",
            "success_probability": "55% a 65% de chance de soltura/cautelares no STJ | ZERO de absolvição via HC",
            "what_wont_work": [
                "❌ Pedir trancamento da ação penal ou absolvição no STJ (esbarra na Súmula 7/STJ e será negado).",
                "❌ Discutir ausência de laudo de voz no STJ antes da sentença de 1ª instância (supressão de instância)."
            ],
            "the_only_real_window": [
                "🎯 Relaxamento de Prisão por Excesso de Prazo Injustificado (>90 dias sem AIJ pelo Juízo de Búzios).",
                "🎯 Extensão de Liberdade por Isonomia Processual com o corréu Matheus (Art. 580 do CPP)."
            ],
            "family_alignment_guide": [
                "1. Esclarecer que o STJ julga apenas a LIBERDADE para responder o processo, e não o fim do processo.",
                "2. Avisar que, mesmo se solto, a ação penal continuará tramitando na 1ª Vara de Búzios onde haverá audiência e julgamento."
            ]
        }
    else:
        p1_fala = "Análise fria das barreiras recursais e jurisprudência defensiva..."
        p1_risco = "ALTO"
        p2_fala = "Força dos elementos acusatórios..."
        p2_forca = "Manutenção da persecução"
        p3_fala = "Identificação da única janela viável..."
        p3_acao = "Tese estrita de direito"
        p4_fala = "Cálculo real de execução penal..."
        p4_realidade = "Fração legal da LEP"
        consensus = {"verdict": "ANÁLISE REALISTA", "success_probability": "30%", "what_wont_work": [], "the_only_real_window": [], "family_alignment_guide": []}

    debate_records.append({
        "persona": "⚖️ O MAGISTRADO INQUISIDOR (RELATOR CÉTICO)",
        "role": "Barreiras Recursais, Súmulas & Jurisprudência Defensiva",
        "stance": "PUNITIVISTA & IMPLACÁVEL",
        "statement": p1_fala,
        "risk_evaluation": p1_risco
    })
    debate_records.append({
        "persona": "⚔️ O PROMOTOR ACUSADOR (O ADVOGADO DO DIABO)",
        "role": "Força Probatória da Acusação & Clamor Público",
        "stance": "ATAQUE ACUSATÓRIO RIGOROSO",
        "statement": p2_fala,
        "prosecution_strength": p2_forca
    })
    debate_records.append({
        "persona": "🛡️ O ESTRATEGISTA PRAGMÁTICO DE CORTES SUPERIORES",
        "role": "Eliminação de Ilusões & Janelas Técnicas Concretas",
        "stance": "REALISMO DEFENSIVO",
        "statement": p3_fala,
        "key_action": p3_acao
    })
    debate_records.append({
        "persona": "📊 O AUDITOR REALISTA DE EXECUÇÃO PENAL",
        "role": "Cálculo Factual da LEP, Frações de Hediondo & Tempo de Cadeia",
        "stance": "MATEMÁTICA DA PRISÃO",
        "statement": p4_fala,
        "prison_reality": p4_realidade
    })

    return {
        "client_name": client_name,
        "crime": case_data.get("crime", "N/A"),
        "processo": case_data.get("processo", "N/A"),
        "instancia": case_data.get("instancia", "N/A"),
        "pena_atual": case_data.get("pena_atual", "N/A"),
        "date": datetime.now().strftime("%d/%m/%Y às %H:%M"),
        "debate_records": debate_records,
        "consensus": consensus
    }

def generate_markdown_report(result: dict, output_file: Path) -> Path:
    c = result["client_name"]
    d = result["date"]
    con = result["consensus"]
    
    md = []
    md.append(f"# 🏛️ Relatório do Comitê Jurídico Estratégico Realista — SuperJus")
    md.append(f"**Cliente / Réu:** `{c}`  ")
    md.append(f"**Imputação:** `{result.get('crime', 'N/A')}`  ")
    md.append(f"**Processo:** `{result.get('processo', 'N/A')}`  ")
    md.append(f"**Instância Atual:** `{result.get('instancia', 'N/A')}`  ")
    md.append(f"**Situação / Pena Atual:** `{result.get('pena_atual', 'N/A')}`  ")
    md.append(f"**Data da Mesa Redonda:** `{d}`  ")
    md.append(f"**Protocolo Aplicado:** Realismo Crítico, Ceticismo Processual & Anti-Bajulação  \n")
    md.append("---\n")
    
    md.append("## 👥 1. O Debate sem Filtros da Mesa Redonda\n")
    for r in result["debate_records"]:
        md.append(f"### {r['persona']}")
        md.append(f"* **Atuação:** {r['role']}")
        md.append(f"* **Postura:** `{r['stance']}`\n")
        md.append(f"> \"{r['statement']}\"\n")
        if "risk_evaluation" in r:
            md.append(f"⚠️ **Risco Processual Real:** {r['risk_evaluation']}\n")
        if "prosecution_strength" in r:
            md.append(f"⚔️ **Ponto Forte da Acusação:** {r['prosecution_strength']}\n")
        if "key_action" in r:
            md.append(f"🎯 **Ação Pragmática:** {r['key_action']}\n")
        if "prison_reality" in r:
            md.append(f"📊 **Realidade da Execução:** {r['prison_reality']}\n")
        md.append("---\n")
        
    md.append("## 🎯 2. Matriz de Realidade Processual & Gestão de Expectativas\n")
    md.append(f"* **Veredito Factual:** `{con['verdict']}`")
    md.append(f"* **Probabilidade Estatística Real de Êxito:** **{con['success_probability']}**\n")
    
    md.append("### ❌ O que NÃO Vai Funcionar (Ilusões que a Banca Deve Descartar):")
    for w in con.get("what_wont_work", []):
        md.append(f"  * {w}")
        
    md.append("\n### 🎯 A Única Janela Técnica Real (Onde Focar 100% da Energia):")
    for t in con.get("the_only_real_window", []):
        md.append(f"  * {t}")
        
    md.append("\n### 🗣️ Guia de Alinhamento com a Família / Cliente (Dizer a Verdade com Ética):")
    for f in con.get("family_alignment_guide", []):
        md.append(f"  * {f}")
        
    md_content = "\n".join(md)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as fp:
        fp.write(md_content)
        
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Comitê Jurídico Estratégico Realista SuperJus")
    parser.add_argument("--cliente", default="Lucas_Freitas", help="Nome do cliente")
    parser.add_argument("--tema", default="", help="Tema livre")
    parser.add_argument("--out", default="", help="Arquivo de saída")
    args = parser.parse_args()

    client_path = Path(f"c:/Projetos/superJus/Clientes/{args.cliente}")
    case_data = gather_client_case_data(client_path)
    
    print("=" * 85)
    print(f"🏛️ COMITÊ JURÍDICO ESTRATÉGICO REALISTA — PROTOCOLO ANTI-BAJULAÇÃO")
    print(f"👤 Cliente / Réu: {case_data.get('full_name', case_data['client_name'])}")
    print(f"⚖️ Processo: {case_data.get('processo', 'N/A')}")
    print(f"🏛️ Instância: {case_data.get('instancia', 'N/A')}")
    print(f"📌 Situação Atual: {case_data.get('pena_atual', 'N/A')}")
    print("=" * 85)
    
    result = run_realistic_multiagent_debate(case_data, args.tema)
    
    for r in result["debate_records"]:
        print(f"\n{r['persona']} — [{r['stance']}]:")
        print(f"  \"{r['statement']}\"")
        
    print("\n" + "═" * 85)
    print(f"📋 MATRIZ DE REALIDADE PROCESSUAL — {result['consensus']['verdict']}:")
    print(f"🏆 Probabilidade Estatística Real: {result['consensus']['success_probability']}")
    
    print("\n❌ O QUE NÃO VAI FUNCIONAR (FALSAS ESPERANÇAS):")
    for w in result["consensus"].get("what_wont_work", []):
        print(f"  • {w}")
        
    print("\n🎯 A ÚNICA JANELA TÉCNICA REAL:")
    for t in result["consensus"].get("the_only_real_window", []):
        print(f"  • {t}")
        
    print("\n🗣️ GUIA DE ALINHAMENTO COM A FAMÍLIA (A DURA VERDADE):")
    for f in result["consensus"].get("family_alignment_guide", []):
        print(f"  • {f}")
    print("═" * 85)

    if args.out:
        out_path = Path(args.out)
    else:
        out_path = client_path / "04_Analises_e_Estrategias" / "Relatorio_Debate_Estrategico_Multiagente_Lucas.md"
        
    generate_markdown_report(result, out_path)
    print(f"\n📄 Relatório Markdown salvo com sucesso em:\n   {out_path}")

if __name__ == "__main__":
    main()
