# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

client_dir = r"C:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima"
docs_dir = os.path.join(client_dir, "03_Documentos_do_Processo")
strat_dir = os.path.join(client_dir, "04_Analises_e_Estrategias")

os.makedirs(docs_dir, exist_ok=True)
os.makedirs(strat_dir, exist_ok=True)

# 1. Salvar Contrarrazões Indexadas em Markdown
doc_path = os.path.join(docs_dir, "contrarrazoes_apelacao_mprj_10-06-2026_index1743-1754.md")

content_doc = """# MINISTÉRIO PÚBLICO DO ESTADO DO RIO DE JANEIRO (MPRJ)
## 2ª Promotoria de Justiça de Guapimirim – RJ
**Processo:** `0004301-33.2018.8.19.0073`  
**Juízo:** 2ª Vara Criminal da Comarca de Guapimirim / RJ (Tribunal do Júri)  
**Peça:** CONTRARRAZÕES DE APELAÇÃO (Art. 600 do CPP)  
**Apelante:** Daniel Ferreira Lima  
**Apelado:** Ministério Público do Estado do Rio de Janeiro  
**Promotora de Justiça Subscritora:** Luiza Lange Rosa Klöppel (Matrícula 8627)  
**Data da Peça:** 10 de junho de 2026 | **Juntada Eletrônica:** 12/06/2026 às 13:47h (Index 1743 a 1754)  

---

### 📌 1. Dados da Condenação Revelados no Documento
- **Dispositivo Penal:** Artigo 121, § 2º, inciso II (Motivo Fútil) do Código Penal.
- **Pena Fixada na Sentença:** **13 anos e 04 meses de reclusão**, em **regime inicial fechado**.
- **Dosimetria Aplicada na Origem:**
  - **Pena-Base:** Exasperada em 2/6 acima do mínimo legal (12 anos + 4 anos = 16 anos) com base em 2 circunstâncias judiciais desfavoráveis do Art. 59 do CP:
    1. *Culpabilidade acentuada:* Relação prévia de amizade entre réu e vítima.
    2. *Circunstâncias do crime:* Emprego sucessivo de múltiplos meios agressivos (disparos de arma de fogo + pauladas + chutes).
  - **Segunda Fase (Atenuantes/Agravantes):** Reconhecida a atenuante da **menoridade relativa (Art. 65, I, do CP)**, com redução de 1/6 (reduzindo de 16 anos para **13 anos e 4 meses de reclusão**).
  - **Terceira Fase:** Inexistência de causas de aumento ou de diminuição.
  - **Regime Inicial:** Fechado (Art. 33, § 2º, 'a', do CP).
  - **Detração Penal (Art. 387, § 2º, CPP):** Não aplicada na sentença pelo Juiz Presidente; remetida à Vara de Execuções Penais (VEP).
  - **Status Cautelar:** Prisão preventiva mantida para apelar, indeferido o direito de recorrer em liberdade, fundamentada no histórico de 4 anos foragido (risco de evasão).

---

### 📑 2. Síntese das Teses Recursais da Defesa e Contrapontos do MPRJ

| Item / Tese | Fundamento da Defesa (Index 1711 e 1734) | Posição e Tese do MPRJ (Contrarrazões) |
| :--- | :--- | :--- |
| **Tese 1: Nulidade por Cerceamento / Plenitude de Defesa** | Advertência judicial indevida impedindo menção à FAC de terceira pessoa e à sentença do julgamento do corréu. | Exercício regular do poder de polícia da Juíza Presidente (Art. 497, CPP) para evitar desequilíbrio e introdução de elementos estranhos aos autos. Ausência de prejuízo. |
| **Tese 2: Nulidade por Paridade de Armas (Prova Emprestada)** | Utilização do depoimento da testemunha Jonathan colhido em processo conexo. | Prova emprestada regularmente admitida sob contraditório; foi requerida pela própria defesa (venire contra factum proprium) e houve inércia após intimação. |
| **Tese 3: Nulidade por Falta de Degravação da Sentença/Audiência** | Indeferimento de transcrição dos depoimentos colhidos em plenário. | Jurisprudência consolidada do STJ (AgRg no HC 902.892/PI e HC 462.253/SC) de que a mídia audiovisual gravada dispensa transcrição literal integral. |
| **Tese 4: Veredito Contrário à Prova dos Autos (Art. 593, III, 'd', CPP)** | Causa mortis decorreu de espancamento efetuado pelo corréu Júlio Leonam, e não de tiros; falta de apreensão da arma/projétil; in dubio pro reo. | Soberania dos veredictos (Art. 5º, XXXVIII, CF); jurados julgam por íntima convicção; unidade de desígnios na execução conjunta; pluralidade de condutas causadoras do óbito. |
| **Tese 5: Desclassificação para Homicídio Tentado** | Ausência de nexo entre a conduta de Daniel e a morte consumada. | Inadmissibilidade de fragmentar o iter criminis; todos os agentes responderam pelo evento lesivo. |
| **Tese 6: Participação de Menor Importância (Art. 29, § 1º, CP)** | Daniel não praticou a agressão letal final; nulidade por falta de quesito. | Daniel concorreu ativamente para a agressão contínua; quesitos formulados conforme teses sem protesto oportuno em ata. |
| **Tese 7: Afastamento do Motivo Fútil** | Ausência de dolo individualizado quanto ao motivo qualificador. | Desavença originada por volume de som automotivo; o agente que adere à conduta assume a futilidade da motivação. |
| **Tese 8: Dosimetria da Pena-Base** | Redução ao mínimo legal de 12 anos, afastando aumento de 2/6. | Culpabilidade acentuada (amizade prévia) e circunstâncias graves (sucessão de agressões) justificam fração de 2/6. |
| **Tese 9: Detração Penal (Art. 387, § 2º, CPP)** | Prisão cautelar desde 14/03/2024 para fins de abrandamento do regime. | Competência da VEP (Art. 66, LEP c/c Lei 14.843/2024 e STF HC 233.825/SP); matéria executória. |
| **Tese 10: Liberdade Provisória / Revogação da Preventiva** | Direito de recorrer em liberdade (Art. 319 do CPP). | Risco de fuga concreto evidenciado pelo período de 4 anos foragido. |
"""

with open(doc_path, "w", encoding="utf-8") as f:
    f.write(content_doc)
print(f"[OK] Documento indexado em: {doc_path}")

# 2. Salvar Análise Estratégica da Apelação
strat_path = os.path.join(strat_dir, "analise_estrategica_contrarazoes_e_teses_tjrj.md")

content_strat = """# ANÁLISE ESTRATÉGICA DEFENSIVA — RESPOSTA ÀS CONTRARRAZÕES DO MPRJ
**Cliente:** Daniel Ferreira Lima | **Processo:** `0004301-33.2018.8.19.0073`  
**Órgão de Destino:** Tribunal de Justiça do Estado do Rio de Janeiro (TJRJ) — Câmaras Criminais  
**Fase:** Julgamento da Apelação Criminal (Art. 593, III do CPP)  

---

## 🎯 1. Pontos de Alta Vulnerabilidade da Tese Ministerial (Onde Golpear no TJRJ)

### 💥 PONTO CRÍTICO 1: Desavença Anterior Afasta Motivo Fútil (STJ)
- **O que disse o MPRJ:** O crime decorreu de *"desavença anterior envolvendo os agentes e a vítima, relacionada ao volume de som automotivo"* (página 9 das Contrarrazões).
- **Abre-se a Porteira para a Defesa:** O Superior Tribunal de Justiça (STJ) possui jurisprudência firmada e pacífica de que **a existência de animosidade, discussão ou desavença prévia entre as partes, ainda que por motivo de som ou somenos importância, DESCARACTERIZA O MOTIVO FÚTIL** (STJ: AgRg no REsp 1.849.201/SP, REsp 1.480.898/RS e HC 512.651/SP).
- **Impacto Prático:** Afastar a qualificadora do motivo fútil desclassifica o homicídio para **HOMICÍDIO SIMPLES (Art. 121, caput, CP: 6 a 20 anos)**, reduzindo a pena-base imediatamente de 12 para 6 anos, derrubando a condenação para a faixa de 6 a 8 anos!

### 💥 PONTO CRÍTICO 2: Ilegalidade da Detração Remetida à VEP (Violação Direta ao Art. 387, § 2º, do CPP)
- **O que disse o MPRJ:** Alegou que a detração é competência da Vara de Execuções Penais (página 11).
- **O Golpe Defensivo:** O Art. 387, § 2º, incluído no CPP pela Lei 12.736/2012, determina expressamente que **o tempo de prisão provisória SERÁ COMPUTADO pelo juiz sentenciante para fins de fixação do regime inicial de cumprimento de pena**.
- Daniel está preso ininterruptamente desde **14 de março de 2024** (mais de 2 anos e 3 meses de prisão cautelar cumprida).
- O STJ já pacificou que o magistrado **não pode se esquivar de aplicar o Art. 387, § 2º do CPP sob pretexto de competência da VEP** quando o cômputo influir na fixação do regime (STJ HC 720.675/SP e HC 693.308/MG).

### 💥 PONTO CRÍTICO 3: Plenitude de Defesa no Júri é Garantia Constitucional Maior (Art. 5º, XXXVIII, 'a', CF)
- **O que disse o MPRJ:** Afirmou que a Juíza exerceu mero "poder de polícia" ao advertir e impedir a menção à sentença do corréu Júlio Leonam.
- **O Golpe Defensivo:** O Tribunal do Júri não é regido pela mera "ampla defesa", mas pela **PLENITUDE DE DEFESA**. A defesa em plenário pode utilizar argumentos jurídicos, fáticos, sociológicos e decisões conexas para demonstrar que a autoria do ato letal foi exclusiva de terceiro. A censura em plenário quebra a espontaneidade da fala do advogado e induz os jurados a acreditarem que a defesa está agindo de má-fé, causando nulidade insanável (Art. 564, IV c/c Art. 593, III, 'a', CPP).

### 💥 PONTO CRÍTICO 4: Bis in Idem na Elevação da Pena-Base por "Amizade Prévia" e "Sucessão de Golpes"
- A exasperação de 2/6 foi abusiva:
  - *"Amizade prévia":* Relações interpessoais prévias são inerentes aos crimes passionais e de desavença comunitária, não revelando culpabilidade extremada extraordinária.
  - *"Meios sucessivos":* Se o próprio MP afirma que houve concurso de agentes e briga generalizada, valorar a multiplicidade de golpes contra Daniel sem individualizar quem desferiu as agressões contundentes constitui flagrante responsabilidade penal objetiva.

---

## 📋 2. Roteiro Prático de Intervenção para o Dr. Gabriel
1. **Acompanhar a Distribuição da Apelação na 2ª Instância do TJRJ:** Identificar a Câmara Criminal e o Desembargador Relator sorteado.
2. **Petição de Memorial de Despacho com o Relator:** Focar prioritariamente no **afastamento do motivo fútil** (com precedentes do STJ sobre desavença anterior de som) e na **retificação da pena com aplicação imediata do Art. 387, § 2º do CPP (Detração)**.
3. **Sustentação Oral em Sessão de Julgamento no TJRJ:** Sustentar a nulidade pela advertência judicial em plenário e a desproporcionalidade da dosimetria.
"""

with open(strat_path, "w", encoding="utf-8") as f:
    f.write(content_strat)
print(f"[OK] Análise estratégica salva em: {strat_path}")
