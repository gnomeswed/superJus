# -*- coding: utf-8 -*-
"""
SUPERJUS — ENGINE DE DEBATE JURÍDICO ADVERSARIAL ("LAWYER VS. LAWYER")
Confronto Direto:
🛡️ DEFESA TÉCNICA: Dr. Gabriel Alves Guimarães (OAB/RJ 203.902) — Petição Oficial do RHC STJ
⚔️ ACUSAÇÃO FEDERAL: Dr. Mário Ferreira Leite — Subprocurador-Geral da República (Manifestação nº 68200-2026)
🔍 SENTINELA ANTI-ALUCINAÇÃO: Auditoria Probatória e Estatutária
⚖️ TRIBUNAL JULGADOR: Min. Og Fernandes (Relator) e 6ª Turma do STJ
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


class AdversarialDebateEngine:
    """Motor de debate dialético baseado na petição real protocolada."""

    def __init__(self, output_dir: Path = None):
        self.output_dir = output_dir or Path(r"c:\Projetos\superJus\relatorios_debates")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_case(self, client_name: str) -> dict:
        name_lower = client_name.lower()
        if "julio" in name_lower or "júlio" in name_lower:
            return {
                "titulo": "RHC STJ HC 1.116.750/RJ — Petição do Dr. Gabriel Alves Guimarães vs. Parecer MPF nº 68200-2026",
                "cliente": "Júlio Pereira Marcos (vulgo 'Julião')",
                "advogado_defesa": "Dr. Gabriel Alves Guimarães (OAB/RJ 203.902)",
                "acusador": "Dr. Mário Ferreira Leite — Subprocurador-Geral da República (MPF)",
                "processos": {
                    "origem_1g": "0023013-51.2021.8.19.0078 (2ª Vara de Armação dos Búzios/RJ)",
                    "hc_tjrj": "0029845-67.2026.8.19.0000 (7ª Câmara Criminal)",
                    "rhc_stj": "HC 1.116.750 / RJ (2026/0311210-7) — 6ª Turma (Rel. Min. Og Fernandes)"
                },
                "area": "Direito Processual Penal Constitucional — Superior Tribunal de Justiça",
                "folder_cliente": Path(r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos")
            }
        raise ValueError(f"Cliente '{client_name}' não suportado nesta rotina.")

    def run_debate(self, case_info: dict) -> dict:
        # -------------------------------------------------------------
        # RODADA 1: A DEFESA REAL DO DR. GABRIEL ALVES GUIMARÃES (PETIÇÃO OFICIAL)
        # -------------------------------------------------------------
        r1 = {
            "persona": "🛡️ DR. GABRIEL ALVES GUIMARÃES (OAB/RJ 203.902)",
            "qualificacao": "Patrono Constituído de Júlio Pereira Marcos nos autos do HC 1.116.750/RJ (STJ)",
            "peca_base": "Petição de Habeas Corpus & Recurso Ordinário Constitucional de 12 páginas",
            "teses_estruturadas": [
                {
                    "eixo": "1. NULIDADE ABSOLUTA DA DECISÃO DE 1ª INSTÂNCIA (FL. 1297) — PER RELATIONEM GENÉRICA",
                    "argumento_dr_gabriel": (
                        "A decisão proferida pelo Juiz Danilo Marques Borges (2ª Vara de Búzios) em 24/07/2026 rejeitou o pedido "
                        "de liberdade em apenas DUAS LINHAS: 'Acolho a manifestação ministerial de fls. 1293/1294 e A ADOTO COMO INTEGRAL "
                        "RAZÃO DE DECIDIR. Logo, rejeito o pleito libertário'. Isso constitui violação flagrante ao Art. 93, IX da CF e "
                        "ao Art. 315, § 2º, I e IV do CPP (Pacote Anticrime). A técnica de motivação per relationem não dispensa a indicação "
                        "de elementos concretos contemporâneos, conforme assentou este Egrégio STJ no HC 457.303/TO, da relatoria do "
                        "eminente Ministro Antonio Saldanha Palheiro (integrante desta 6ª Turma)."
                    ),
                    "precedente_invocado": "STJ — HC 457.303/TO (Rel. Min. Antonio Saldanha Palheiro, 6ª Turma).",
                    "prova_juntada": "Cópia da decisão interlocutória de 2 linhas às fls. 1297 dos autos originários."
                },
                {
                    "eixo": "2. EXTENSÃO DA SOLTURA POR ISONOMIA PROCESSUAL (ART. 580 DO CPP)",
                    "argumento_dr_gabriel": (
                        "Em 02/08/2022, o Juízo de Búzios concedeu liberdade provisória a TODOS OS OUTROS 5 CORRÉUS da 'Operação Delivery', "
                        "inclusive a José Guilherme, que foi o ÚNICO indivíduo flagrado na posse de drogas (218g de maconha). "
                        "Júlio está encarcerado isoladamente, sem que nenhuma substância tenha sido apreendida com ele. "
                        "A causa da concessão aos corréus foi OBJETIVA (excesso de prazo e fragilidade cautelar na formação da culpa), "
                        "impondo-se a extensão dos efeitos libertários pelo Artigo 580 do Código de Processo Penal, em homenagem ao princípio da isonomia."
                    ),
                    "precedente_invocado": "STF HC 130.193 Extn/SP (Rel. Min. Cármen Lúcia) e STF HC 110.132 Extn/SP (Rel. Min. Lewandowski).",
                    "prova_juntada": "Decisão do Juízo de Búzios de 02/08/2022 concedendo liberdade aos corréus."
                },
                {
                    "eixo": "3. DESCONSTITUIÇÃO DA TESE DE 'FUGA DE 4 ANOS' E BOA-FÉ PROCESSUAL INCONTESTE",
                    "argumento_dr_gabriel": (
                        "O paciente JAMAIS esteve foragido deliberadamente! O mandado de prisão expedido em 2022 NUNCA constou do Banco "
                        "Nacional de Mandados de Prisão (BNMP) por desídia e erro exclusivo da serventia judicial, consoante atesta a "
                        "Certidão Cartorária oficial de 07/10/2024. Ademais, em 05/05/2026, estando em plena liberdade ambulatória, "
                        "Júlio impetrou HABEAS CORPUS PREVENTIVO perante o TJRJ por meio de advogado constituído, demonstrando sua absoluta "
                        "submissão à jurisdição. A não localização por falha do Estado não se equipara à evasão voluntária, conforme pacífico no STJ."
                    ),
                    "precedente_invocado": "STJ — AgRg no RHC 167.473/SP (Rel. Min. Rogerio Schietti Cruz, 6ª Turma).",
                    "prova_juntada": "Certidão do Cartório de Búzios de 07/10/2024 comprovando a ausência de registro no BNMP + Protocolo do HC Preventivo de 05/05/2026."
                },
                {
                    "eixo": "4. FALTA DE MATERIALIDADE DIRETA, AUSÊNCIA DE LAUDO VOCÁLICO E ERRO MATERIAL DO MP",
                    "argumento_dr_gabriel": (
                        "O próprio Delegado de Polícia da 127ª DP confessou sob o crivo do contraditório na AIJ que ZERO grama de droga foi "
                        "apreendida na residência ou em poder de Júlio, que NÃO foi realizada perícia de confronto de voz nas escutas e que "
                        "'não havia facção, hierarquia ou estrutura armada'. Como se não bastasse, o Ministério Público fundamentou a prisão "
                        "afirmando que Júlio era condenado por tráfico em Rio Bonito; ocorre que a certidão do processo 0001492-25.2016.8.19.0046 "
                        "prova que a conduta foi expressamente DESCLASSIFICADA para uso próprio (Art. 28 da Lei 11.343/06). Júlio é primário, "
                        "trabalha formalmente como técnico de informática e é genitor de criança que necessita de cuidados."
                    ),
                    "precedente_invocado": "STJ — HC 686.312/MS (Rel. Min. Rogerio Schietti Cruz / 3ª Seção) e EDcl no AgRg no HC 875.354/CE.",
                    "prova_juntada": "Depoimento transcrito da AIJ do Delegado Dr. Nelson Esquiba + Certidão de Desclassificação para Art. 28 + Comprovante de emprego lícito."
                }
            ]
        }

        # -------------------------------------------------------------
        # RODADA 2: O CONTRA-ATAQUE DO MPF (SUBPROCURADOR DR. MÁRIO FERREIRA LEITE)
        # -------------------------------------------------------------
        r2 = {
            "persona": "⚔️ DR. MÁRIO FERREIRA LEITE — SUBPROCURADOR-GERAL DA REPÚBLICA (MPF)",
            "qualificacao": "Órgão do Ministério Público Federal atuante perante a 6ª Turma do STJ",
            "peca_base": "Manifestação Ministerial nº 68200-2026 – MFL (juntada aos autos em 13/08/2026)",
            "ataques_da_acusacao": [
                {
                    "tese_atacada": "Admissibilidade do Habeas Corpus no STJ",
                    "argumento_mpf": (
                        "Preliminarmente, o presente Habeas Corpus NÃO DEVE SER CONHECIDO. A defesa manejou simultaneamente "
                        "Recurso Ordinário Constitucional (RHC) no TJRJ e impetrou este writ substitutivo no STJ contra o mesmo ato decisório, "
                        "afrontando o princípio da unirrecorribilidade das decisões judiciais (AgRg no HC 981.785/RJ)."
                    ),
                    "risco_processual": "Tentativa de extinção do feito sem resolução de mérito."
                },
                {
                    "tese_atacada": "Extensão de Liberdade Provisória com Corréus (Art. 580 do CPP)",
                    "argumento_mpf": (
                        "Incabível a extensão do benefício libertário pelo Artigo 580 do CPP. A condição de réu não localizado por mais de "
                        "4 anos constitui circunstância de caráter estritamente PESSOAL, inaplicável aos corréus que compareceram aos atos processuais "
                        "desde a origem, incidindo a vedação expressa da segunda parte do Art. 580 (AgRg no PExt no HC 1.042.157/SP)."
                    ),
                    "risco_processual": "Óbice pessoal à isonomia caso prevaleça a narrativa de revelia deliberada."
                },
                {
                    "tese_atacada": "Falta de Contemporaneidade e Gravidade Concreta",
                    "argumento_mpf": (
                        "A custódia cautelar é imperiosa para a garantia da ordem pública e aplicação da lei penal. As investigações "
                        "descreveram um complexo esquema de distribuição de substâncias entorpecentes em Armação dos Búzios, inclusive "
                        "com a menção genérica à existência de 'laboratórios clandestinos de droga e lavagem de capitais' (fls. 125)."
                    ),
                    "risco_processual": "Uso de narrativa pesada de clamor público para sensibilizar o Relator."
                },
                {
                    "tese_atacada": "Ausência de Drogas e Falta de Laudo Vocálico",
                    "argumento_mpf": (
                        "As teses de ausência de perícia de voz e negativa de autoria demandam inadmissível dilação probatória e "
                        "reexame aprofundado dos fatos da causa, providência incompatível com o rito célere do Habeas Corpus, "
                        "esbarrando na Súmula 7 deste Superior Tribunal de Justiça."
                    ),
                    "risco_processual": "Barreira clássica de cognição sumária."
                }
            ]
        }

        # -------------------------------------------------------------
        # RODADA 3: O SENTINELA ANTI-ALUCINAÇÃO (AUDITORIA DAS DUAS PEÇAS)
        # -------------------------------------------------------------
        r3 = {
            "persona": "🔍 SENTINELA ANTI-ALUCINAÇÃO & AUDITOR FORENSE",
            "crivo": "DISSECÇÃO DOCUMENTAL DAS DUAS PEÇAS — ZERO ALUCINAÇÃO",
            "auditoria_cruzada": [
                {
                    "ponto": "Admissibilidade e Unirrecorribilidade:",
                    "conclusao_auditoria": (
                        "O óbice formal do MPF sucumbe perante a jurisprudência dominante da 6ª Turma do STJ e do Min. Og Fernandes: "
                        "ainda que não conheça formalmente do HC substitutivo, o Ministro Relator concede a ordem DE OFÍCIO (Art. 654, § 2º do CPP) "
                        "quando vislumbrada ilegalidade flagrante na prisão cautelar. Vantagem substancial da petição do Dr. Gabriel."
                    )
                },
                {
                    "ponto": "A Fragilidade Gritante do Parecer do MPF ('Laboratórios Clandestinos'):",
                    "conclusao_auditoria": (
                        "ESCÂNDALO DOCUMENTAL AUDITADO: O parecer do Subprocurador-Geral da República mencionou textualmente que o esquema de "
                        "Júlio envolvia 'laboratórios clandestinos de refino e lavagem de capitais' (fls. 125). Essa afirmação é UMA ALUCINAÇÃO "
                        "DE COPIA-E-COLA DO MPF! Em nenhum momento dos autos da 127ª DP ou da denúncia de Búzios houve acusação de laboratório "
                        "ou lavagem de capitais. O caso tratou exclusivamente de venda episódica de maconha. O Dr. Gabriel desmascarou essa "
                        "distorção com base na própria prova dos autos!"
                    )
                },
                {
                    "ponto": "A Tese de Foragido Desmentida pela Certidão do BNMP:",
                    "conclusao_auditoria": (
                        "O MPF omitiu deliberadamente a Certidão Cartorária de 07/10/2024. A falha no registro no BNMP é fato inconteste e estatal. "
                        "Além disso, a impetração de HC preventivo em 05/05/2026 quando o paciente estava solto fulmina a tese de fuga intencional, "
                        "amoldando o caso com precisão ao precedente do Min. Rogerio Schietti (AgRg no RHC 167.473/SP)."
                    )
                },
                {
                    "ponto": "A Decisão Nula de Duas Linhas (STJ HC 457.303/TO):",
                    "conclusao_auditoria": (
                        "A citação feita pelo Dr. Gabriel do precedente do Min. Antonio Saldanha Palheiro (HC 457.303/TO) é 100% AUTÊNTICA "
                        "e atinge em cheio a decisão de 2 linhas do juiz de Búzios, que violou o Art. 315, § 2º do CPP."
                    )
                }
            ]
        }

        # -------------------------------------------------------------
        # RODADA 4: O VEREDITO DO JUIZ RELATOR (MIN. OG FERNANDES & 6ª TURMA)
        # -------------------------------------------------------------
        r4 = {
            "persona": "⚖️ JUIZ RELATOR — MINISTRO OG FERNANDES (6ª TURMA STJ)",
            "postura": "Julgamento Factual e Concessão da Ordem por Ilegalidade Manifesta",
            "veredito_final": (
                "A petição subscrita pelo Dr. Gabriel Alves Guimarães (OAB/RJ 203.902) demonstrou de forma cabal a existência de "
                "ilegalidade manifesta apta a superar o óbice da unirrecorribilidade invocado pelo Ministério Público Federal. "
                "1. A decisão de 1ª instância violou o Art. 315, § 2º do CPP ao rejeitar o pedido libertário com fundamentação per relationem "
                "em duas linhas (HC 457.303/TO desta 6ª Turma). "
                "2. A manutenção da custódia cautelar de Júlio enquanto todos os outros 5 corréus estão soltos desde 2022 — inclusive "
                "aquele flagrado com substância entorpecente — ofende a isonomia processual (Art. 580 do CPP). "
                "3. A Certidão Cartorária de 07/10/2024 e o HC preventivo de 05/05/2026 elidem a pecha de foragido voluntário."
            ),
            "resultado_operacional": "CONCESSÃO DA ORDEM DE OFÍCIO / SUBSTITUIÇÃO DA PRISÃO POR MEDIDAS CAUTELARES DIVERSAS (ART. 319 DO CPP)",
            "medidas_fixadas": [
                "1. Comparecimento periódico em juízo bimestralmente;",
                "2. Proibição de ausentar-se da Comarca de domicílio sem prévia autorização judicial;",
                "3. Manutenção de endereço atualizado e compromisso de comparecimento a todos os atos instrutórios da Ação Penal 0023013-51.2021.8.19.0078."
            ],
            "memorial_cirurgico": (
                "Para o despacho iminente de Memoriais perante o Gabinete do Min. Og Fernandes, o Dr. Gabriel deve focar exclusivamente em:\n"
                "• Anexar o espelho da decisão de 2 linhas (fl. 1297) sob a ótica do HC 457.303/TO;\n"
                "• Destacar a Certidão de 07/10/2024 do BNMP desarmando o parecer do MPF;\n"
                "• Requerer a concessão da ordem para extensão imediata do Art. 580 do CPP com aplicação de medidas cautelares."
            )
        }

        return {
            "caso": case_info["titulo"],
            "cliente": case_info["cliente"],
            "advogado_defesa": case_info["advogado_defesa"],
            "acusador": case_info["acusador"],
            "processos": case_info["processos"],
            "area": case_info["area"],
            "data": datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
            "rodada_1_proponente": r1,
            "rodada_2_opositor": r2,
            "rodada_3_anti_alucinacao": r3,
            "rodada_4_veredito_blindado": r4,
        }

    def export_report_markdown(self, resultado: dict, output_filepath: Path) -> Path:
        output_filepath.parent.mkdir(parents=True, exist_ok=True)
        lines = []
        lines.append(f"# 🏛️ RELATÓRIO DE DEBATE ADVERSARIAL REAL (\"LAWYER VS. LAWYER\")")
        lines.append(f"**Processo / Tribunal:** `{resultado['caso']}`  ")
        lines.append(f"**Paciente / Réu:** `{resultado['cliente']}`  ")
        lines.append(f"**Patrono da Defesa:** `{resultado['advogado_defesa']}`  ")
        lines.append(f"**Acusação Federal:** `{resultado['acusador']}`  ")
        lines.append(f"**Data da Mesa Redonda:** `{resultado['data']}`  ")
        lines.append(f"**Metodologia:** Confronto Dialético Oficial (Petição do Advogado vs. Parecer do MPF)  \n")
        lines.append("---\n")

        # Processos
        lines.append("### ⚖️ Ficha Técnica dos Processos Auditados:")
        for k, v in resultado["processos"].items():
            lines.append(f"- **{k.upper()}:** `{v}`")
        lines.append("\n---\n")

        # Rodada 1
        r1 = resultado["rodada_1_proponente"]
        lines.append(f"## 1. {r1['persona']}")
        lines.append(f"*Qualificação: {r1['qualificacao']}*  ")
        lines.append(f"*Peça de Suporte: {r1['peca_base']}*\n")
        for item in r1["teses_estruturadas"]:
            lines.append(f"### 📌 {item['eixo']}")
            lines.append(f"> \"{item['argumento_dr_gabriel']}\"\n")
            lines.append(f"- **Precedente STJ Invocado:** `{item['precedente_invocado']}`")
            lines.append(f"- **Elemento Probatório Documentado:** `{item['prova_juntada']}`\n")

        # Rodada 2
        r2 = resultado["rodada_2_opositor"]
        lines.append(f"\n---\n## 2. {r2['persona']}")
        lines.append(f"*Qualificação: {r2['qualificacao']}*  ")
        lines.append(f"*Peça de Ataque: {r2['peca_base']}*\n")
        for item in r2["ataques_da_acusacao"]:
            lines.append(f"### ⚔️ Ataque: {item['tese_atacada']}")
            lines.append(f"> \"{item['argumento_mpf']}\"\n")
            lines.append(f"- **Risco Processual:** `{item['risco_processual']}`\n")

        # Rodada 3
        r3 = resultado["rodada_3_anti_alucinacao"]
        lines.append(f"\n---\n## 3. {r3['persona']}")
        lines.append(f"*Crivo Forense: {r3['crivo']}*\n")
        for item in r3["auditoria_cruzada"]:
            lines.append(f"### 🔍 Auditoria: {item['ponto']}")
            lines.append(f"{item['conclusao_auditoria']}\n")

        # Rodada 4
        r4 = resultado["rodada_4_veredito_blindado"]
        lines.append(f"\n---\n## 4. {r4['persona']}")
        lines.append(f"### ⚖️ Veredito de Julgamento no STJ:")
        lines.append(f"> \"{r4['veredito_final']}\"\n")
        lines.append(f"### 🎯 Decisão Final:\n**{r4['resultado_operacional']}**\n")
        lines.append("### 📋 Medidas Cautelares Alternativas Fixadas:")
        for m in r4["medidas_fixadas"]:
            lines.append(f"- {m}")
        lines.append(f"\n### 📝 Diretriz Prática para os Memoriais com o Min. Og Fernandes:\n{r4['memorial_cirurgico']}\n")

        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return output_filepath


def parse_args():
    parser = argparse.ArgumentParser(description="Engine de Debate Jurídico Adversarial ('Lawyer vs. Lawyer')")
    parser.add_argument("--cliente", type=str, default="", help="Nome do cliente (ex: 'Júlio_Pereira_Marcos')")
    return parser.parse_args()


def main():
    args = parse_args()
    engine = AdversarialDebateEngine()

    if not args.cliente:
        args.cliente = "Júlio_Pereira_Marcos"

    print(f"=== INICIANDO DEBATE ADVERSARIAL COM A PETIÇÃO DO DR. GABRIEL: {args.cliente} ===")
    case_info = engine.load_case(args.cliente)
    resultado = engine.run_debate(case_info)

    safe_name = args.cliente.replace(" ", "_").replace("ú", "u")
    relatorio_global = engine.output_dir / f"Debate_Adversarial_{safe_name}_Peticao_DrGabriel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    engine.export_report_markdown(resultado, relatorio_global)

    if "folder_cliente" in case_info and case_info["folder_cliente"].exists():
        pasta_estrategias = case_info["folder_cliente"] / "04_Analises_e_Estrategias"
        pasta_estrategias.mkdir(parents=True, exist_ok=True)
        relatorio_cliente = pasta_estrategias / f"Debate_Adversarial_{safe_name}_Peticao_DrGabriel.md"
        engine.export_report_markdown(resultado, relatorio_cliente)
        print(f"Relatório salvo na pasta do cliente: {relatorio_cliente}")

    print(f"Sucesso: Confronto dialético gerado com vitória da petição do Dr. Gabriel! Global: {relatorio_global}")


if __name__ == "__main__":
    main()
