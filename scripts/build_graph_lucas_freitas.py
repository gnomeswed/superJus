# -*- coding: utf-8 -*-
"""
Gerador de Extração Semântica e Estrutural para Graphify
Cliente: Lucas de Souza Freitas (Lucas Motoboy)
"""
import os
import json
from pathlib import Path
from graphify.validate import validate_extraction

BASE_DIR = Path(r"C:\Projetos\superJus\Clientes\Lucas_Freitas")

nodes = []
edges = []
seen_nodes = set()

def add_node(node_id, label, file_type, source_file, rationale=None):
    if node_id in seen_nodes:
        return
    seen_nodes.add(node_id)
    n = {
        "id": node_id,
        "label": label,
        "file_type": file_type,
        "source_file": str(source_file)
    }
    if rationale:
        n["rationale"] = rationale
    nodes.append(n)

def add_edge(source, target, relation, confidence, source_file, weight=1.0):
    if source not in seen_nodes or target not in seen_nodes:
        return
    edges.append({
        "source": source,
        "target": target,
        "relation": relation,
        "confidence": confidence,
        "source_file": str(source_file),
        "weight": weight
    })

# --- 1. ENTIDADES PRINCIPAIS (PESSOAS E PARTES) ---
f_meta = BASE_DIR / "01_Dados_do_Cliente" / "case_meta.json"
f_dossie = BASE_DIR / "04_Analises_e_Estrategias" / "DOSSIÊ_COMPLETO_LUCAS_MOTOBOY_17_08_2026.md"

add_node("lucas_de_souza_freitas", "Lucas de Souza Freitas (Lucas Motoboy / LC)", "concept", f_meta,
         rationale="Réu primário à época do fato de 2017, motoboy, condenado pelo Júri de Niterói a 22 anos em regime fechado.")
add_node("ronny_batalha_fernandes", "Ronny Batalha Fernandes (Pretinho)", "concept", f_meta,
         rationale="Corréu no homicídio e na ocultação de cadáver, condenado conjuntamente pelo Júri.")
add_node("marcos_de_souza_freitas", "Marcos de Souza Freitas (Vítima)", "concept", f_meta,
         rationale="Vítima fatal, tio de Lucas de Souza Freitas, morto no interior de sua residência na Comunidade do Preventório.")
add_node("mprj", "Ministério Público do Estado do Rio de Janeiro (MPRJ)", "concept", f_meta,
         rationale="Órgão acusador responsável pela denúncia, sustentação em plenário e contrarrazões de apelação.")
add_node("dra_nearis_carvalho_arce", "Dra. Nearis dos Santos Carvalho Arce (Juíza Presidente)", "concept", f_meta,
         rationale="Magistrada da 3ª Vara Criminal de Niterói que presidiu o Júri e dosou a pena com excesso na pena-base e sem compensação de confissão.")
add_node("des_flavio_itabaiana", "Des. Flávio Itabaiana de Oliveira Nicolau (Relator TJRJ)", "concept", f_dossie,
         rationale="Desembargador Relator da Apelação Criminal na 2ª Câmara Criminal do TJRJ; proferiu despacho 'Peço dia para julgamento'.")
add_node("des_katia_jangutta", "Desª Katia Maria Amaral Jangutta (Revisora TJRJ)", "concept", f_dossie,
         rationale="Desembargadora Revisora sorteada na 2ª Câmara Criminal do TJRJ para a Apelação.")
add_node("des_paulo_rangel", "Des. Paulo Sérgio Rangel do Nascimento", "concept", f_dossie,
         rationale="Desembargador da 3ª Câmara Criminal que concedeu a ordem de soltura no HC de 2017 de Lucas de Souza Freitas.")
add_node("defensoria_publica_rj", "Defensoria Pública do Estado do Rio de Janeiro (DPRJ)", "concept", f_meta,
         rationale="Patrona técnica de Lucas no plenário do Júri e responsável pelas Razões de Apelação.")

# --- 2. PROCESSOS E ÓRGÃOS JUDICIAIS ---
add_node("proc_principal_0011857_2024", "Ação Penal do Júri nº 0011857-95.2024.8.19.0002", "document", f_meta,
         rationale="Processo-crime de competência do Júri que apura o homicídio triplamente qualificado e ocultação de cadáver.")
add_node("apelacao_2026_050_14194", "Apelação Criminal TJRJ nº 2026.050.14194", "document", f_dossie,
         rationale="Recurso de Apelação autuado em 10/08/2026 na 2ª Câmara Criminal para reforma da dosimetria e anulação do júri.")
add_node("tria_vara_criminal_niteroi", "3ª Vara Criminal da Comarca de Niterói / Tribunal do Júri", "concept", f_meta,
         rationale="Juízo de 1º grau competente pelo processo de origem.")
add_node("segunda_camara_criminal_tjrj", "2ª Câmara Criminal do Tribunal de Justiça do Rio de Janeiro", "concept", f_dossie,
         rationale="Órgão fracionário de 2º grau competente pelo julgamento da Apelação Criminal.")
add_node("proc_antigo_0000253_2017", "Processo Histórico nº 0000253-78.2017.8.19.0004 (Roubo)", "document", f_dossie,
         rationale="Ação penal anterior de 2017 na 2ª Vara Criminal de Niterói, arquivada definitivamente em 08/11/2017 (Maço 1310262).")
add_node("hc_0046418_2017_tjrj", "Habeas Corpus TJRJ nº 0046418-98.2017.8.19.0000", "document", f_dossie,
         rationale="HC impetrado em 2017 com concessão de liberdade por decisão do Des. Paulo Rangel.")

# --- 3. ATOS PROCESSUAIS E DOCUMENTOS DO CASO ---
f_juri = BASE_DIR / "Caso_Principal" / "documentos_processo" / "22-04-2026_Audiência Juri.txt"
f_sent = BASE_DIR / "Caso_Principal" / "documentos_processo" / "22-04-2026_Sentenca_Completa_Dosimetria.txt"
f_mutirao = BASE_DIR / "Caso_Principal" / "documentos_processo" / "17-06-2026_Recebimento.txt"
f_rec_apel = BASE_DIR / "Caso_Principal" / "documentos_processo" / "10-06-2026_Recebimento.txt"
f_pronuncia = BASE_DIR / "Caso_Principal" / "documentos_processo" / "03-04-2025_Sentença em Audiência  - Proferida Sentença de Pronúncia.txt"
f_atual_26set = BASE_DIR / "04_Analises_e_Estrategias" / "atualizacao_26_09_2026.md"
f_parecer_dosim = BASE_DIR / "Caso_Principal" / "analises" / "analise_dosimetria_e_recurso_lucas.md"

add_node("sessao_juri_22_04_2026", "Sessão de Julgamento do Tribunal do Júri (22/04/2026)", "document", f_juri,
         rationale="Sessão plenária realizada em 22/04/2026 na qual os jurados condenaram os réus e foi interposta apelação imediata.")
add_node("sentenca_condenatoria_22_anos", "Sentença Condenatória de 22 Anos de Reclusão", "document", f_sent,
         rationale="Sentença lavrada pela Juíza Presidente aplicando 21 anos pelo homicídio qualificado e 1 ano pela ocultação de cadáver.")
add_node("despacho_mutirao_cnj_17_06_2026", "Despacho do Mutirão Processual Penal do CNJ (17/06/2026)", "document", f_mutirao,
         rationale="Decisão proferida no âmbito da Portaria Conjunta TJ/CGJ/2VP nº 03/2026 mantendo a prisão preventiva sem oitiva prévia da defesa.")
add_node("despacho_recebimento_apelacao_10_06", "Despacho de Recebimento das Apelações (10/06/2026)", "document", f_rec_apel,
         rationale="Despacho da magistrada de origem recebendo as apelações interpostas em plenário e abrindo vista para razões.")
add_node("sentenca_pronuncia_03_04_2025", "Sentença de Pronúncia (03/04/2025)", "document", f_pronuncia,
         rationale="Decisão interlocutória mista que admitiu a acusação nos termos do Art. 413 do CPP e pronunciou Lucas e Ronny.")
add_node("remessa_ao_tjrj_06_08_2026", "Remessa dos Autos em Grau de Recurso (06/08/2026)", "document", f_atual_26set,
         rationale="Certificação e remessa eletrônica dos autos da 3ª Vara Criminal de Niterói para o Tribunal de Justiça.")
add_node("despacho_peco_dia_02_09_2026", "Despacho 'Peço dia para julgamento' (02/09/2026)", "document", f_atual_26set,
         rationale="Despacho monocrático do Relator Des. Flávio Itabaiana liberando os autos para inclusão na pauta de julgamento.")
add_node("movimento_pedindo_dia_03_09_2026", "Movimento 'Observações Pedindo Dia' (03/09/2026)", "document", f_atual_26set,
         rationale="Fase atual do processo na 2ª Câmara Criminal, aguardando publicação da data da sessão de julgamento.")

# --- 4. NÚCLEO DOGMÁTICO E TESES JURÍDICAS (CONCEITOS E RATIONALE) ---
add_node("homicidio_triplamente_qualificado", "Homicídio Triplamente Qualificado (Art. 121, § 2º, I, III e IV CP)", "concept", f_sent,
         rationale="Motivo torpe (vingança familiar por furtos), meio cruel (múltiplas facadas) e recurso que impossibilitou defesa da vítima.")
add_node("crime_ocultacao_cadaver", "Ocultação de Cadáver (Art. 211 do CP)", "concept", f_sent,
         rationale="Concretação do corpo da vítima sob o piso da área externa da residência, descoberto em adiantado estado de putrefação.")
add_node("excesso_pena_base_9_anos", "Tese: Excesso Desproporcional na Pena-Base (+9 Anos)", "rationale", f_parecer_dosim,
         rationale="A magistrada elevou a pena-base em 9 anos (de 12 para 21 anos). A jurisprudência do STJ adota a fração de 1/6 por vetor desfavorável (limite de 18 anos).")
add_node("compensacao_confissao_reincidencia", "Tese: Compensação Integral da Confissão com Reincidência (Súmula 545 e Tema 585 STJ)", "rationale", f_parecer_dosim,
         rationale="A recusa da compensação violou a jurisprudência pacífica da 3ª Seção do STJ; a confissão de Lucas deve neutralizar a agravante.")
add_node("potencial_reducao_pena", "Perspectiva de Redução da Pena (22 anos para 17-19 anos)", "concept", f_parecer_dosim,
         rationale="Impacto prático da apelação: redução de 3 a 5 anos de reclusão com a correção das ilegalidades trifásicas.")
add_node("violacao_contraditorio_mutirao_cnj", "Tese: Nulidade por Violação do Contraditório Prévio no Mutirão CNJ", "rationale", f_mutirao,
         rationale="A juíza confessou ter decidido de ofício sem ouvir a defesa para 'bater a meta de prazo do mutirão', violando o Art. 3º da Portaria 03/2026 e Art. 5º, LV da CF.")
add_node("decisao_contraria_prova_autos", "Tese: Decisão Manifestamente Contrária à Prova dos Autos (Art. 593, III, 'd' CPP)", "rationale", f_dossie,
         rationale="Alegação defensiva de fragilidade probatória quanto à autoria direta de Lucas e inexistência de confissão formal em sede policial.")
add_node("prisao_preventiva_manutencao", "Status Cautelar: Prisão Preventiva sem Trânsito em Julgado", "concept", f_atual_26set,
         rationale="Custódia estritamente cautelar mantida no regime fechado; inocorrência de execução definitiva na VEP.")
add_node("sumula_545_stj", "Súmula 545 do Superior Tribunal de Justiça", "concept", f_parecer_dosim,
         rationale="Quando a confissão for utilizada para a formação do convencimento do julgador, o réu fará jus à atenuante prevista no art. 65, III, 'd', do Código Penal.")
add_node("tema_585_stj", "Tema Repetitivo 585 do STJ", "concept", f_parecer_dosim,
         rationale="Fixa a equivalência de preponderância entre reincidência e confissão espontânea (Art. 67 CP), impondo a compensação integral.")
add_node("ausencia_vep", "Inexistência de Processo na VEP / SEEU", "concept", f_atual_26set,
         rationale="Inviabilidade de execução provisória ou definitiva antes do julgamento do recurso ordinário de apelação.")

# --- 5. LIGAÇÕES ESTRUTURAIS E SEMÂNTICAS (EDGES) ---
# Relações de autoria, acusação e partes
add_edge("lucas_de_souza_freitas", "proc_principal_0011857_2024", "réu_em", "EXTRACTED", f_meta)
add_edge("ronny_batalha_fernandes", "proc_principal_0011857_2024", "corréu_em", "EXTRACTED", f_meta)
add_edge("lucas_de_souza_freitas", "ronny_batalha_fernandes", "corréu_com", "EXTRACTED", f_meta)
add_edge("marcos_de_souza_freitas", "proc_principal_0011857_2024", "vítima_em", "EXTRACTED", f_meta)
add_edge("mprj", "proc_principal_0011857_2024", "promove_acusação_em", "EXTRACTED", f_meta)
add_edge("defensoria_publica_rj", "lucas_de_souza_freitas", "patrocina_defesa_de", "EXTRACTED", f_juri)
add_edge("tria_vara_criminal_niteroi", "proc_principal_0011857_2024", "juízo_de_origem_de", "EXTRACTED", f_meta)
add_edge("dra_nearis_carvalho_arce", "tria_vara_criminal_niteroi", "magistrada_titular_de", "EXTRACTED", f_meta)

# Relações de crimes e sentença
add_edge("proc_principal_0011857_2024", "homicidio_triplamente_qualificado", "imputa", "EXTRACTED", f_pronuncia)
add_edge("proc_principal_0011857_2024", "crime_ocultacao_cadaver", "imputa", "EXTRACTED", f_pronuncia)
add_edge("dra_nearis_carvalho_arce", "sentenca_condenatoria_22_anos", "proferiu", "EXTRACTED", f_sent)
add_edge("sessao_juri_22_04_2026", "sentenca_condenatoria_22_anos", "culminou_em", "EXTRACTED", f_juri)
add_edge("sentenca_condenatoria_22_anos", "lucas_de_souza_freitas", "condena", "EXTRACTED", f_sent)
add_edge("sentenca_condenatoria_22_anos", "ronny_batalha_fernandes", "condena", "EXTRACTED", f_sent)
add_edge("sentenca_condenatoria_22_anos", "prisao_preventiva_manutencao", "mantém", "EXTRACTED", f_sent)

# Relações de apelação e 2ª instância
add_edge("sessao_juri_22_04_2026", "despacho_recebimento_apelacao_10_06", "ensejou_interposição_de", "EXTRACTED", f_juri)
add_edge("despacho_recebimento_apelacao_10_06", "apelacao_2026_050_14194", "deu_origem_a", "EXTRACTED", f_rec_apel)
add_edge("remessa_ao_tjrj_06_08_2026", "apelacao_2026_050_14194", "encaminhou_autos_para", "EXTRACTED", f_atual_26set)
add_edge("segunda_camara_criminal_tjrj", "apelacao_2026_050_14194", "órgão_julgador_de", "EXTRACTED", f_dossie)
add_edge("des_flavio_itabaiana", "apelacao_2026_050_14194", "relator_de", "EXTRACTED", f_dossie)
add_edge("des_katia_jangutta", "apelacao_2026_050_14194", "revisora_de", "EXTRACTED", f_dossie)
add_edge("des_flavio_itabaiana", "despacho_peco_dia_02_09_2026", "proferiu", "EXTRACTED", f_atual_26set)
add_edge("despacho_peco_dia_02_09_2026", "movimento_pedindo_dia_03_09_2026", "gerou_fase", "EXTRACTED", f_atual_26set)
add_edge("movimento_pedindo_dia_03_09_2026", "apelacao_2026_050_14194", "fase_atual_de", "EXTRACTED", f_atual_26set)

# Relações com teses jurídicas e erros de dosimetria
add_edge("apelacao_2026_050_14194", "excesso_pena_base_9_anos", "fundamenta_se_em", "INFERRED", f_parecer_dosim, 0.95)
add_edge("apelacao_2026_050_14194", "compensacao_confissao_reincidencia", "fundamenta_se_em", "INFERRED", f_parecer_dosim, 0.95)
add_edge("apelacao_2026_050_14194", "decisao_contraria_prova_autos", "pleiteia_anulacao_por", "INFERRED", f_dossie, 0.90)
add_edge("compensacao_confissao_reincidencia", "sumula_545_stj", "apoia_se_em", "EXTRACTED", f_parecer_dosim)
add_edge("compensacao_confissao_reincidencia", "tema_585_stj", "apoia_se_em", "EXTRACTED", f_parecer_dosim)
add_edge("excesso_pena_base_9_anos", "potencial_reducao_pena", "viabiliza", "INFERRED", f_parecer_dosim, 0.95)
add_edge("compensacao_confissao_reincidencia", "potencial_reducao_pena", "viabiliza", "INFERRED", f_parecer_dosim, 0.95)

# Relações com Mutirão e Nulidades
add_edge("dra_nearis_carvalho_arce", "despacho_mutirao_cnj_17_06_2026", "prolatou", "EXTRACTED", f_mutirao)
add_edge("despacho_mutirao_cnj_17_06_2026", "violacao_contraditorio_mutirao_cnj", "apresenta_vício_de", "INFERRED", f_mutirao, 0.95)
add_edge("despacho_mutirao_cnj_17_06_2026", "prisao_preventiva_manutencao", "reiterou", "EXTRACTED", f_mutirao)

# Relações com Histórico 2017 e VEP
add_edge("lucas_de_souza_freitas", "proc_antigo_0000253_2017", "réu_em", "EXTRACTED", f_dossie)
add_edge("hc_0046418_2017_tjrj", "proc_antigo_0000253_2017", "oriundo_de", "EXTRACTED", f_dossie)
add_edge("des_paulo_rangel", "hc_0046418_2017_tjrj", "relatou_e_concedeu", "EXTRACTED", f_dossie)
add_edge("lucas_de_souza_freitas", "ausencia_vep", "situação_atual", "EXTRACTED", f_atual_26set)

data = {
    "nodes": nodes,
    "edges": edges,
    "hyperedges": [
        {
            "id": "hiperaresta_triade_recursiva_dosimetria",
            "label": "Tríade de Revisão da Pena (Pena-Base + Compensação = Redução)",
            "nodes": ["excesso_pena_base_9_anos", "compensacao_confissao_reincidencia", "potencial_reducao_pena"]
        },
        {
            "id": "hiperaresta_turma_julgadora_tjrj",
            "label": "Composição Julgadora da 2ª Câmara Criminal",
            "nodes": ["segunda_camara_criminal_tjrj", "des_flavio_itabaiana", "des_katia_jangutta", "apelacao_2026_050_14194"]
        }
    ],
    "input_tokens": 0,
    "output_tokens": 0
}

errors = validate_extraction(data)
if errors:
    print("ERROS DE VALIDAÇÃO:")
    for e in errors:
        print(" -", e)
    raise SystemExit(1)

out_sem = Path(r"C:\Projetos\superJus\graphify-out\.graphify_semantic.json")
out_extract = Path(r"C:\Projetos\superJus\graphify-out\.graphify_extract.json")

out_sem.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
out_extract.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"Sucesso! Extração semântica de Lucas Motoboy validada:")
print(f" - {len(nodes)} nós")
print(f" - {len(edges)} arestas ({sum(1 for e in edges if e['confidence'] == 'EXTRACTED')} EXTRACTED, {sum(1 for e in edges if e['confidence'] == 'INFERRED')} INFERRED)")
print(f" - {len(data['hyperedges'])} hiperarestas")
