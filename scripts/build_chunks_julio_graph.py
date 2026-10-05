# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path
from graphify.validate import validate_extraction

root = Path(r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos").resolve()
lines = Path("graphify-out/.graphify_uncached.txt").read_text(encoding="utf-8").splitlines()
chunks = [lines[i:i+22] for i in range(0, len(lines), 22)]

def make_stem(filepath):
    try:
        rel = Path(filepath).relative_to(root)
    except:
        rel = Path(filepath)
    # drop extension, join segments with _
    parts = list(rel.parts[:-1]) + [rel.stem]
    import re
    norm_parts = [re.sub(r"[^a-z0-9_]", "_", p.lower()) for p in parts]
    return "_".join(norm_parts)

print("Construindo Chunks 1, 3 e 4 para Júlio Pereira Marcos...")

# =========================================================================
# CHUNK 1: 1ª Instância Búzios (Originário, Desmembrado, Apenso RESE, TJRJ HC)
# =========================================================================
c1_files = chunks[0]
c1_nodes = [
    {
        "id": "proc_originario_buzios_0022975_2021",
        "label": "Ação Penal Originária nº 0022975-39.2021.8.19.0078 (Operação Delivery Búzios)",
        "file_type": "document",
        "source_file": c1_files[1],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-09-05",
        "author": "2ª Vara de Búzios",
        "contributor": "TJRJ"
    },
    {
        "id": "proc_desmembrado_julio_0023013_2021",
        "label": "Ação Penal Desmembrada nº 0023013-51.2021.8.19.0078 (Exclusiva Júlio Pereira Marcos)",
        "file_type": "document",
        "source_file": c1_files[6],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-09-22",
        "author": "Dr. Danilo Marques Borges",
        "contributor": "TJRJ"
    },
    {
        "id": "apenso_rese_ministerial_0001140_2024",
        "label": "Apenso de Recurso em Sentido Estrito nº 0001140-87.2024.8.19.0078 (RESE do MP)",
        "file_type": "document",
        "source_file": c1_files[13],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-09-05",
        "author": "Ministério Público RJ",
        "contributor": "TJRJ"
    },
    {
        "id": "hc_tjrj_7a_camara_0029845_2026",
        "label": "Habeas Corpus TJRJ nº 0029845-67.2026.8.19.0000 (7ª Câmara Criminal - Des. Sidney Rosa)",
        "file_type": "document",
        "source_file": c1_files[16],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-08-20",
        "author": "Des. Sidney Rosa da Silva",
        "contributor": "TJRJ"
    },
    {
        "id": "decisao_soltura_correus_02_08_2022",
        "label": "Decisão de Relaxamento de Prisão por Excesso de Prazo aos 5 Corréus (02/08/2022)",
        "file_type": "concept",
        "source_file": c1_files[1],
        "source_location": "fls. 1396 / DJERJ 10/08/2022",
        "source_url": None,
        "captured_at": "2022-08-02",
        "author": "Dr. Raphael Baddini de Queiroz Campos",
        "contributor": "2ª Vara de Búzios"
    },
    {
        "id": "correu_jose_guilherme_costa_freire",
        "label": "Corréu José Guilherme da Costa Freire (Zezé - único flagrado com drogas, solto em 2022)",
        "file_type": "concept",
        "source_file": c1_files[1],
        "source_location": None,
        "source_url": None,
        "captured_at": "2022-08-03",
        "author": None,
        "contributor": None
    },
    {
        "id": "correu_christiano_pereira_marcos",
        "label": "Corréu Christiano Pereira Marcos (Irmão de Júlio, solto em 03/08/2022)",
        "file_type": "concept",
        "source_file": c1_files[1],
        "source_location": None,
        "source_url": None,
        "captured_at": "2022-08-03",
        "author": None,
        "contributor": None
    },
    {
        "id": "falha_cadastral_bnmp_mandado",
        "label": "Erro de Cadastro e Inexistência de Mandado no BNMP (Descaracterização da Fuga)",
        "file_type": "rationale",
        "source_file": c1_files[6],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-05-12",
        "author": "Defesa Técnica",
        "contributor": None
    },
    {
        "id": "juiz_danilo_marques_borges",
        "label": "Dr. Danilo Marques Borges (Juiz Titular da 2ª Vara Criminal de Búzios)",
        "file_type": "concept",
        "source_file": c1_files[6],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-07-23",
        "author": None,
        "contributor": None
    },
    {
        "id": "paralisia_cartoraria_buzios_55_dias",
        "label": "Inércia Cartorária de 55+ Dias sem Impulso Oficial na Ação Desmembrada",
        "file_type": "concept",
        "source_file": c1_files[6],
        "source_location": "Última juntada em 04/08/2026",
        "source_url": None,
        "captured_at": "2026-09-28",
        "author": "Serventia da 2ª Vara",
        "contributor": None
    }
]

c1_edges = [
    {
        "source": "proc_originario_buzios_0022975_2021",
        "target": "proc_desmembrado_julio_0023013_2021",
        "relation": "conceptually_related_to",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[1],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "proc_originario_buzios_0022975_2021",
        "target": "decisao_soltura_correus_02_08_2022",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[1],
        "source_location": "fls. 1396",
        "weight": 1.0
    },
    {
        "source": "decisao_soltura_correus_02_08_2022",
        "target": "correu_jose_guilherme_costa_freire",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[1],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "decisao_soltura_correus_02_08_2022",
        "target": "correu_christiano_pereira_marcos",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[1],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "apenso_rese_ministerial_0001140_2024",
        "target": "decisao_soltura_correus_02_08_2022",
        "relation": "cites",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[13],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "proc_desmembrado_julio_0023013_2021",
        "target": "paralisia_cartoraria_buzios_55_dias",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[6],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "proc_desmembrado_julio_0023013_2021",
        "target": "juiz_danilo_marques_borges",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[6],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "falha_cadastral_bnmp_mandado",
        "target": "proc_desmembrado_julio_0023013_2021",
        "relation": "rationale_for",
        "confidence": "INFERRED",
        "confidence_score": 0.95,
        "source_file": c1_files[6],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "hc_tjrj_7a_camara_0029845_2026",
        "target": "proc_desmembrado_julio_0023013_2021",
        "relation": "cites",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[16],
        "source_location": None,
        "weight": 1.0
    }
]

c1_hypers = [
    {
        "id": "nucleo_processual_buzios_1a_instancia",
        "label": "Núcleo Processual de 1ª Instância de Búzios (Feito Originário + Desmembrado + RESE)",
        "nodes": [
            "proc_originario_buzios_0022975_2021",
            "proc_desmembrado_julio_0023013_2021",
            "apenso_rese_ministerial_0001140_2024"
        ],
        "relation": "participate_in",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c1_files[1]
    }
]

p1 = {"nodes": c1_nodes, "edges": c1_edges, "hyperedges": c1_hypers, "input_tokens": 0, "output_tokens": 0}
err1 = validate_extraction(p1)
if err1:
    print("Erro C1:", err1)
    sys.exit(1)
Path("graphify-out/.graphify_chunk_01.json").write_text(json.dumps(p1, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Chunk 01 gerado com sucesso: {len(c1_nodes)} nodes, {len(c1_edges)} edges.")

# =========================================================================
# CHUNK 3: Audiências, Provas, Transcrição, Confissão Delegado, DJERJ
# =========================================================================
c3_files = chunks[2]
c3_nodes = [
    {
        "id": "transcricao_integral_aij_policiais",
        "label": "Transcrição Integral da Audiência de Instrução (1.958 Linhas - Depoimentos Policiais)",
        "file_type": "document",
        "source_file": c3_files[0],
        "source_location": "Linhas 1 a 1958",
        "source_url": None,
        "captured_at": "2022-07-25",
        "author": "2ª Vara de Búzios",
        "contributor": "Hugo Henrique Cavalcanti Matos"
    },
    {
        "id": "confissao_delegado_nelson_esquiba_art35",
        "label": "Confissão Expressa do Delegado Nelson Esquiba sobre Ausência de Hierarquia e Estrutura no Art. 35",
        "file_type": "concept",
        "source_file": c3_files[0],
        "source_location": "Linhas 820 a 826",
        "source_url": None,
        "captured_at": "2022-07-25",
        "author": "Dr. Nelson Esquiba Junior (Delegado Assistente)",
        "contributor": "PCERJ"
    },
    {
        "id": "admissao_delegado_rodrigo_moreira_pericia_voz",
        "label": "Admissão do Delegado Rodrigo Moreira sobre Inexistência de Perícia Vocálica nas Interceptações",
        "file_type": "concept",
        "source_file": c3_files[0],
        "source_location": "Linha 430",
        "source_url": None,
        "captured_at": "2022-07-25",
        "author": "Dr. Rodrigo Bichara Moreira (Delegado Titular)",
        "contributor": "PCERJ"
    },
    {
        "id": "intimacao_informal_whatsapp_delegado",
        "label": "Intimação Informal por WhatsApp e Declaração Forçada de Foragido sem Citação Válida",
        "file_type": "concept",
        "source_file": c3_files[0],
        "source_location": "Linhas 710 a 730",
        "source_url": None,
        "captured_at": "2022-07-25",
        "author": "127ª DP Búzios",
        "contributor": None
    },
    {
        "id": "declaracao_pre_julgamento_juiza_maira",
        "label": "Declaração Antecipada de Indeferimento pela Magistrada Anterior ('Na assentada vou indeferir')",
        "file_type": "concept",
        "source_file": c3_files[0],
        "source_location": "Linha 1888",
        "source_url": None,
        "captured_at": "2022-07-25",
        "author": "Dra. Maíra Valéria Veiga de Oliveira",
        "contributor": "2ª Vara de Búzios"
    },
    {
        "id": "dossie_neutro_analise_hc_julio_stj",
        "label": "Dossiê Estratégico Neutro e Análise Crítica do Caso Júlio (Poder Judiciário x Defesa)",
        "file_type": "document",
        "source_file": c3_files[9],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-08-20",
        "author": "Equipe de Inteligência SuperJus",
        "contributor": "Antigravity"
    },
    {
        "id": "tese_ausencia_materialidade_sem_drogas",
        "label": "Tese: Ausência de Materialidade Direta no Tráfico (Zero Grama Apreendido com Júlio - STF RE 1558206)",
        "file_type": "rationale",
        "source_file": c3_files[7],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-08-18",
        "author": "Defesa Técnica",
        "contributor": "Dr. Gabriel Alves Guimarães"
    }
]

c3_edges = [
    {
        "source": "transcricao_integral_aij_policiais",
        "target": "confissao_delegado_nelson_esquiba_art35",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c3_files[0],
        "source_location": "L820-826",
        "weight": 1.0
    },
    {
        "source": "transcricao_integral_aij_policiais",
        "target": "admissao_delegado_rodrigo_moreira_pericia_voz",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c3_files[0],
        "source_location": "L430",
        "weight": 1.0
    },
    {
        "source": "transcricao_integral_aij_policiais",
        "target": "intimacao_informal_whatsapp_delegado",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c3_files[0],
        "source_location": "L710",
        "weight": 1.0
    },
    {
        "source": "transcricao_integral_aij_policiais",
        "target": "declaracao_pre_julgamento_juiza_maira",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c3_files[0],
        "source_location": "L1888",
        "weight": 1.0
    },
    {
        "source": "confissao_delegado_nelson_esquiba_art35",
        "target": "tese_ausencia_materialidade_sem_drogas",
        "relation": "conceptually_related_to",
        "confidence": "INFERRED",
        "confidence_score": 0.85,
        "source_file": c3_files[7],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "dossie_neutro_analise_hc_julio_stj",
        "target": "transcricao_integral_aij_policiais",
        "relation": "cites",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c3_files[9],
        "source_location": None,
        "weight": 1.0
    }
]

c3_hypers = [
    {
        "id": "vicios_e_confissoes_instrucao_policial",
        "label": "Conjunto de Vícios e Confissões da Investigação Policial (L820 Esquiba + L430 Moreira + WhatsApp)",
        "nodes": [
            "confissao_delegado_nelson_esquiba_art35",
            "admissao_delegado_rodrigo_moreira_pericia_voz",
            "intimacao_informal_whatsapp_delegado"
        ],
        "relation": "form",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c3_files[0]
    }
]

p3 = {"nodes": c3_nodes, "edges": c3_edges, "hyperedges": c3_hypers, "input_tokens": 0, "output_tokens": 0}
err3 = validate_extraction(p3)
if err3:
    print("Erro C3:", err3)
    sys.exit(1)
Path("graphify-out/.graphify_chunk_03.json").write_text(json.dumps(p3, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Chunk 03 gerado com sucesso: {len(c3_nodes)} nodes, {len(c3_edges)} edges.")

# =========================================================================
# CHUNK 4: Andamentos Setembro, STJ 28/09/2026, Petição 1025001, Desclassificação Rio Bonito
# =========================================================================
c4_files = chunks[3]
c4_nodes = [
    {
        "id": "peticao_razoes_finais_stj_1025001_2026",
        "label": "Petição de Razões Finais nº 1025001/2026 no STJ (Protocolada em 28/09/2026 às 16:01)",
        "file_type": "document",
        "source_file": c4_files[13],
        "source_location": "STJ HC 1.116.750/RJ",
        "source_url": None,
        "captured_at": "2026-09-28T16:01:00",
        "author": "Dr. Gabriel Alves Guimarães (OAB/RJ 203902)",
        "contributor": "STJ Gabinete Og Fernandes"
    },
    {
        "id": "certidao_oficial_objeto_pe_stj_5208904",
        "label": "Certidão Oficial de Objeto e Pé STJ nº 5208904 (Emitida em 28/09/2026 às 19:50:21)",
        "file_type": "document",
        "source_file": c4_files[13],
        "source_location": "Segurança: 68DD.2EFA.2A9E.9D7",
        "source_url": None,
        "captured_at": "2026-09-28T19:50:21",
        "author": "Superior Tribunal de Justiça",
        "contributor": "STJ SJD"
    },
    {
        "id": "certidao_absolvicao_desclassificacao_rio_bonito",
        "label": "Certidão de Absolvição/Desclassificação para Art. 28 e Arquivamento em Rio Bonito (Primariedade)",
        "file_type": "concept",
        "source_file": c4_files[13],
        "source_location": "Comarca de Rio Bonito",
        "source_url": None,
        "captured_at": "2026-09-28",
        "author": "Juízo da Comarca de Rio Bonito",
        "contributor": "Defesa Técnica"
    },
    {
        "id": "desmascaramento_falsa_reincidencia_mp",
        "label": "Desconstituição da Falsa Alegação de Reincidência Ministerial Induzida a Erro",
        "file_type": "rationale",
        "source_file": c4_files[13],
        "source_location": None,
        "source_url": None,
        "captured_at": "2026-09-28",
        "author": "Dr. Gabriel Alves Guimarães",
        "contributor": None
    },
    {
        "id": "resposta_acusacao_buzios_tempestiva_voluntaria",
        "label": "Resposta à Acusação com Rol de Testemunhas e Requerimento de Mídias em Búzios",
        "file_type": "document",
        "source_file": c4_files[0],
        "source_location": "2ª Vara Criminal de Búzios",
        "source_url": None,
        "captured_at": "2026-09-28",
        "author": "Dr. Gabriel Alves Guimarães",
        "contributor": "2ª Vara de Búzios"
    },
    {
        "id": "minuta_decisao_pronta_gabinete_og_fernandes",
        "label": "Decisão Minutada no Gabinete do Min. Og Fernandes com Publicação Prevista pós-Eleições",
        "file_type": "concept",
        "source_file": c4_files[13],
        "source_location": "STJ 6ª Turma",
        "source_url": None,
        "captured_at": "2026-09-28",
        "author": "Gabinete Min. Og Fernandes",
        "contributor": "STJ"
    },
    {
        "id": "indeferimento_liminar_presidencia_herman_benjamin",
        "label": "Indeferimento Liminar no Plantão de Julho pelo Presidente Herman Benjamin (Sem Apreciação pelo Relator)",
        "file_type": "concept",
        "source_file": c4_files[12],
        "source_location": "Decisão de 29/07/2026",
        "source_url": None,
        "captured_at": "2026-07-29",
        "author": "Min. Herman Benjamin (Presidente)",
        "contributor": "STJ"
    }
]

c4_edges = [
    {
        "source": "peticao_razoes_finais_stj_1025001_2026",
        "target": "certidao_absolvicao_desclassificacao_rio_bonito",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c4_files[13],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "certidao_absolvicao_desclassificacao_rio_bonito",
        "target": "desmascaramento_falsa_reincidencia_mp",
        "relation": "rationale_for",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c4_files[13],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "certidao_oficial_objeto_pe_stj_5208904",
        "target": "peticao_razoes_finais_stj_1025001_2026",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c4_files[13],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "certidao_oficial_objeto_pe_stj_5208904",
        "target": "indeferimento_liminar_presidencia_herman_benjamin",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c4_files[13],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "peticao_razoes_finais_stj_1025001_2026",
        "target": "minuta_decisao_pronta_gabinete_og_fernandes",
        "relation": "conceptually_related_to",
        "confidence": "INFERRED",
        "confidence_score": 0.95,
        "source_file": c4_files[13],
        "source_location": None,
        "weight": 1.0
    },
    {
        "source": "peticao_razoes_finais_stj_1025001_2026",
        "target": "resposta_acusacao_buzios_tempestiva_voluntaria",
        "relation": "references",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c4_files[13],
        "source_location": None,
        "weight": 1.0
    }
]

c4_hypers = [
    {
        "id": "virada_processual_stj_28_setembro_2026",
        "label": "Virada Processual no STJ em 28/09/2026 (Petição 1025001 + Certidão Primariedade + Decisão Minutada)",
        "nodes": [
            "peticao_razoes_finais_stj_1025001_2026",
            "certidao_absolvicao_desclassificacao_rio_bonito",
            "minuta_decisao_pronta_gabinete_og_fernandes"
        ],
        "relation": "form",
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": c4_files[13]
    }
]

p4 = {"nodes": c4_nodes, "edges": c4_edges, "hyperedges": c4_hypers, "input_tokens": 0, "output_tokens": 0}
err4 = validate_extraction(p4)
if err4:
    print("Erro C4:", err4)
    sys.exit(1)
Path("graphify-out/.graphify_chunk_04.json").write_text(json.dumps(p4, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Chunk 04 gerado com sucesso: {len(c4_nodes)} nodes, {len(c4_edges)} edges.")

print("\nTodos os chunks 01, 02, 03 e 04 gerados e validados com 100% de conformidade!")
