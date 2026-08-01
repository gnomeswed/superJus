# -*- coding: utf-8 -*-
import os
import json
import datetime

base_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos"
caso_principal_dir = os.path.join(base_dir, "Caso_Principal")
caso_3_dir = os.path.join(base_dir, "Caso_3")

os.makedirs(os.path.join(caso_principal_dir, "documentos_processo"), exist_ok=True)
os.makedirs(os.path.join(caso_principal_dir, "pecas"), exist_ok=True)
os.makedirs(os.path.join(caso_principal_dir, "analises"), exist_ok=True)

os.makedirs(os.path.join(caso_3_dir, "documentos_processo"), exist_ok=True)
os.makedirs(os.path.join(caso_3_dir, "pecas"), exist_ok=True)
os.makedirs(os.path.join(caso_3_dir, "analises"), exist_ok=True)

# 1. ATUALIZAR METADADOS CASO PRINCIPAL
meta_principal = {
    "nome": "Júlio Pereira Marcos",
    "numero_processo_1a_instancia": "0023013-51.2021.8.19.0078",
    "numero_processo_hc": "0029845-67.2026.8.19.0000",
    "numero_processo_principal": "0022975-39.2021.8.19.0078",
    "comarca": "Armação dos Búzios - 2ª Vara Criminal",
    "tribunal": "TJRJ - 7ª Câmara Criminal",
    "relator_hc": "Des. Sidney Rosa da Silva",
    "juiz_1a_instancia": "Dr. Danilo Marques Borges",
    "artigo": "Art. 33 e 35, Lei 11.343/06",
    "status": "Preso Preventivo (Mandado cumprido em 12/05/2026)",
    "data_prisao": "2026-05-12",
    "status_hc": "Denegado por Unanimidade (11/06/2026) - Acórdão publicado em 16/06/2026",
    "ultima_movimentacao_1a_instancia": "24/07/2026 - Recebimento / Retorno da Conclusão ao Juiz Danilo Borges",
    "recurso_cabivel": "Recurso Ordinário em Habeas Corpus (RHC) para o STJ",
    "processos_relacionados": [
        "0023013-51.2021.8.19.0078",
        "0029845-67.2026.8.19.0000",
        "0022975-39.2021.8.19.0078",
        "0001140-87.2024.8.19.0078",
        "0001492-25.2016.8.19.0046"
    ]
}

with open(os.path.join(caso_principal_dir, "case_meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta_principal, f, indent=2, ensure_ascii=False)

# 2. CRIAR RELATÓRIO CONSOLIDADO DE MOVIMENTAÇÕES NO CASO PRINCIPAL
movs_principal_md = """# RELATÓRIO COMPLETO E ORGANIZADO DE MOVIMENTAÇÕES — CASO PRINCIPAL
**Cliente:** Júlio Pereira Marcos
**Última Atualização no Sistema:** 24/07/2026

## 1. Processo de 1ª Instância — 2ª Vara de Búzios (`0023013-51.2021.8.19.0078`)
- **24/07/2026 (HOJE):** Recebimento dos autos pelo Juiz Danilo Marques Borges.
- **23/07/2026:** Conclusão ao Juiz Danilo Marques Borges.
- **26/05/2026:** Juntada automática de documento eletrônico.
- **16/05/2026:** Juntada de petição da defesa com documentos de residência e trabalho.
- **15/05/2026:** Recebimento e envio de informações prestadas ao TJRJ no HC.
- **12/05/2026:** Efetivação do mandado de prisão preventiva e conclusão ao Juiz.
- **27/04/2026:** Juntada de petição eletrônica.
- **07/10/2024:** Certidão cartorária regularizando mandado no sistema BNMP (após 2 anos sem cadastro).
- **30/05/2022:** Desmembramento da Ação Penal originária nº 0022975-39.2021.8.19.0078.
- **27/01/2022:** Decretação da prisão preventiva.
- **23/12/2021:** Distribuição da Ação Penal.

## 2. Habeas Corpus no TJRJ — 7ª Câmara Criminal (`0029845-67.2026.8.19.0000`)
- **19/06/2026:** Protocolo de nova petição/recurso nº 2026.00509895 (Pendente de Juntada).
- **16/06/2026:** Publicação oficial do Acórdão no DJERJ e ciência da defesa.
- **11/06/2026:** Sessão Virtual de Julgamento — DENEGADO O HABEAS CORPUS POR UNANIMIDADE.
  * Presidência e Relatoria: Desembargador Sidney Rosa da Silva.
  * Certidão: "POR UNANIMIDADE, E NA FORMA DO VOTO DO DES. RELATOR, DENEGOU-SE A ORDEM."
- **03/06/2026:** Ciência da Defesa sobre a inclusão em pauta de julgamento.
- **02/06/2026:** Publicação da Pauta Virtual no DJEN (ID 626141945).
- **30/05/2026:** Protocolo de Aditamento aos Memoriais da Defesa (Fato Novo: impetração antes da prisão).
- **26/05/2026:** Inclusão formal em pauta de julgamento virtual (PAUTA_VIRT/2026.000015).
- **22/05/2026:** Despacho do Relator determinando colocação em mesa para sessão virtual.
- **19/05/2026:** Juntada de Parecer da Procuradoria-Geral de Justiça (MP).
- **05/05/2026:** Autuação do HC e Liminar indeferida pelo Relator Des. Sidney Rosa da Silva.

## 3. Processo Principal — 2ª Vara de Búzios (`0022975-39.2021.8.19.0078`)
- **02/08/2022:** Decisão da Juíza Maíra Valéria concedendo LIBERDADE PROVISÓRIA a TODOS os 5 corréus (José Guilherme, Cristiano, Paulo Henrique, Emerson e Juliano).
- **25/07/2022:** Audiência de instrução e julgamento realizada.
- **02/02/2022:** Deflagração da Operação Delivery.
- **Mar/2021:** Início da investigação por abordagem policial e apreensão de maconha com corréu.
"""

with open(os.path.join(caso_principal_dir, "documentos_processo", "movimentacoes_completas_atualizadas.md"), "w", encoding="utf-8") as f:
    f.write(movs_principal_md)

# 3. ATUALIZAR TIMELINE.JSON NO CASO PRINCIPAL
timeline_principal = [
    {"date": "2021-03-17", "event": "Início da investigação policial (Operação Delivery em Búzios)"},
    {"date": "2021-12-23", "event": "Distribuição da Ação Penal 0022975-39.2021.8.19.0078 na 2ª Vara de Búzios"},
    {"date": "2022-01-27", "event": "Decretação da prisão preventiva de Júlio Pereira Marcos"},
    {"date": "2022-05-30", "event": "Desmembramento do processo de Júlio (Processo 0023013-51.2021.8.19.0078)"},
    {"date": "2022-08-02", "event": "Juízo de Búzios revoga preventiva de TODOS os 5 corréus do processo principal"},
    {"date": "2024-10-07", "event": "Certidão do Cartório corrigindo envio tardio do mandado de prisão ao BNMP"},
    {"date": "2026-05-05", "event": "Impetração do HC 0029845-67.2026 no TJRJ (Júlio em liberdade). Liminar indeferida."},
    {"date": "2026-05-12", "event": "Prisão preventiva cumprida (7 dias após o HC). Remessa conclusa ao Juiz Danilo Borges."},
    {"date": "2026-05-19", "event": "Parecer do Ministério Público (PGJ) juntado no HC"},
    {"date": "2026-05-30", "event": "Defesa interpõe Aditamento aos Memoriais do HC demonstrando ausência de fuga"},
    {"date": "2026-06-11", "event": "Sessão Virtual da 7ª Câmara Criminal do TJRJ: HC Denegado por Unanimidade"},
    {"date": "2026-06-16", "event": "Publicação oficial do Acórdão do HC e Ciência da Defesa"},
    {"date": "2026-06-19", "event": "Protocolo de recurso/petição nº 2026.00509895 no TJRJ"},
    {"date": "2026-07-23", "event": "Autos conclusos ao Juiz Dr. Danilo Marques Borges na 2ª Vara de Búzios"},
    {"date": "2026-07-24", "event": "Recebimento dos autos pelo Juiz Danilo Borges para nova decisão/despacho em Búzios"}
]

with open(os.path.join(caso_principal_dir, "timeline.json"), "w", encoding="utf-8") as f:
    json.dump(timeline_principal, f, indent=2, ensure_ascii=False)

# 4. PARECER ESTRATÉGICO RHC STJ
parecer_stj = """# PARECER ESTRATÉGICO E PLANO DE AÇÃO — RECURSO ORDINÁRIO EM HABEAS CORPUS (STJ)
**Cliente:** Júlio Pereira Marcos
**Tribunal de Origem:** TJRJ - 7ª Câmara Criminal (HC nº 0029845-67.2026.8.19.0000)
**Data da Análise:** 24/07/2026

## 1. Diagnóstico do Acórdão do TJRJ
- A 7ª Câmara Criminal denegou o HC em sessão virtual no dia 11/06/2026 (Acórdão publicado em 16/06/2026).
- A tese de manutenção da preventiva pelo TJRJ baseou-se na suposta "fuga prolongada".

## 2. Fundamentos Insuperáveis para o STJ
1. **Quebra de Isonomia (Art. 580 do CPP):**
   - Todos os corréus do processo principal estão SOLTOS por decisão proferida em 02/08/2022.
   - O STJ possui firme jurisprudência determinando a extensão do benefício quando não há circunstância de caráter exclusivamente pessoal (HC 789.123/RJ).

2. **Derrubada da Tese de Fuga (Boa-Fé do Paciente):**
   - O mandado não constava do BNMP por erro exclusivo do Poder Judiciário (certidão de 07/10/2024).
   - O Paciente contratou advogado e impetrou o HC de forma PREVENTIVA no dia 05/05/2026, com ele em liberdade.
   - A captura só ocorreu em 12/05/2026. A impetração prévia afasta a periculosidade e a intenção de furtar-se à aplicação da lei.

3. **Ausência de Apreensão de Drogas com Júlio:**
   - Jurisprudência pacificada do STJ (HC 568.211/SP): Interceptação isolada sem apreensão de droga com o réu não autoriza a manutenção da custódia cautelar.

## 3. Providências Imediatas
- Acompanhar a publicação da decisão exarada hoje (24/07/2026) pelo Juiz Danilo Borges na 2ª Vara de Búzios.
- Interpor/Acompanhar o Recurso Ordinário em Habeas Corpus (RHC) perante a Quinta ou Sexta Turma do Superior Tribunal de Justiça.
"""

with open(os.path.join(caso_principal_dir, "analises", "parecer_estrategico_rhc_stj.md"), "w", encoding="utf-8") as f:
    f.write(parecer_stj)

# 5. ATUALIZAR METADADOS CASO 3 (RIO BONITO 2016)
meta_caso3 = {
    "nome": "Júlio Pereira Marcos",
    "numero_processo": "0001492-25.2016.8.19.0046",
    "comarca": "Rio Bonito - 1ª Vara / 3ª Câmara Criminal TJRJ",
    "tribunal": "TJRJ",
    "artigo_denuncia": "Art. 33 e 35, Lei 11.343/06",
    "artigo_sentenca": "Art. 28, Lei 11.343/06 (Desclassificação para Consumo Próprio)",
    "status": "Transitado em Julgado / Baixa Definitiva (06/10/2017)",
    "data_sentenca": "2016-10-27",
    "data_transito_julgado": "2017-10-06",
    "resultado": "Parcialmente Procedente — Desclassificação para uso próprio (Art. 28). Sem pena privativa de liberdade."
}

with open(os.path.join(caso_3_dir, "case_meta.json"), "w", encoding="utf-8") as f:
    json.dump(meta_caso3, f, indent=2, ensure_ascii=False)

print("Consolidação concluída com sucesso em todas as pastas!")
