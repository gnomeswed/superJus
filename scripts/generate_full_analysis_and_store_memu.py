# -*- coding: utf-8 -*-
import os
import sys
import json
import sqlite3
import uuid
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

target_dir = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\analises"
os.makedirs(target_dir, exist_ok=True)
md_path = os.path.join(target_dir, "Dossie_Analise_Integral_Pontos_Fortes_e_Brechas_Julio.md")
db_path = r"C:\Users\Administrator\.memu\memu.sqlite3"

doc_content = """# DOSSIÊ DE ANÁLISE INTEGRAL DO PROCESSO — JÚLIO PEREIRA MARCOS
**Cliente:** Júlio Pereira Marcos (vulgo "Julião")
**Ação Penal 1ª Instância (Búzios):** `0023013-51.2021.8.19.0078` (desmembrado da `0022975-39.2021.8.19.0078`)
**Habeas Corpus TJRJ (7ª Câmara):** `0029845-67.2026.8.19.0000`
**Recurso Ordinário em HC no STJ:** `HC 1.116.750 / RJ (2026/0311210-7)` — 6ª Turma (Rel. Min. Og Fernandes)
**Data da Auditoria Integral:** 03/08/2026

---

## 📋 1. SÍNTESE FÁTICA E PROCESSUAL COMPLETA

1. **A Operação policial:** A acusação deriva da chamada "Operação Delivery" (Inquérito 127-00370/2021 e Cautelar 0000568-39.2021.8.19.0078), deflagrada pela 127ª DP em Armação dos Búzios/RJ, imputando a Júlio os crimes do **Artigo 33, caput** (Tráfico) e **Artigo 35** (Associação para o Tráfico) da Lei 11.343/06, c/c **Artigo 61, II, "j"** do CP (calamidade/pandemia).
2. **Histórico da Prisão Preventiva:** Decretada originalmente em **27/01/2022**.
3. **O Desmembramento Processual:** Ocorrido em **30/05/2022** quanto a Júlio e o corréu Rodrigo.
4. **Liberdade Concedida aos Demais Corréus:** Em **02/08/2022**, a MM. Juíza Maíra Valéria concedeu **LIBERDADE PROVISÓRIA a TODOS os 5 corréus** do processo principal (`0022975-39.2021.8.19.0078`), por excesso de prazo na instrução.
5. **Cumprimento do Mandado:** Efetuado em **12/05/2026**.
6. **Denegação no TJRJ:** Habeas Corpus denegado por unanimidade pela 7ª Câmara Criminal do TJRJ em **11/06/2026** (Rel. Des. Sidney Rosa da Silva).
7. **Indeferimento da Revogação na 1ª Instância (Búzios):** Decisão de **24/07/2026 (fl. 1297)** proferida pelo Juiz Dr. Danilo Marques Borges indeferindo o pedido de liberdade por garantia da ordem pública (Publicada no DJERJ em **29/07/2026**).
8. **Recurso Ordinário em Trâmite no STJ:** Remetido formalmente pelo TJRJ ao STJ em **29/07/2026** (`HC 1.116.750/RJ`). Vista aberta ao Ministério Público Federal (MPF) em **31/07/2026**.

---

## 💪 2. PONTOS FORTES DA DEFESA

### 🛡️ Ponto Forte 1: Quebra Flagrante de Isonomia Processual (Art. 580 do CPP)
* **Argumento:** É incontroverso que **TODOS OS OUTROS 5 CORRÉUS** responderam em liberdade a partir de 02/08/2022. O corréu José Guilherme (único em cuja posse foram efetivamente encontradas 218g de maconha no flagrante) está solto.
* **Impacto:** A manutenção exclusiva da prisão cautelar contra Júlio configura tratamento anti-isonômico e desproporcional, violando frontalmente o Art. 580 do Código de Processo Penal e a jurisprudência pacificada do STF e STJ.

### 🛡️ Ponto Forte 2: Ausência Absoluta de Materialidade Física com o Cliente
* **Argumento:** **Nenhuma grama de droga** foi apreendida em poder de Júlio Pereira Marcos na deflagração da operação ou em diligências anteriores.
* **Impacto:** Aplicação do precedente vinculante do **STJ no HC 568.211/SP** (Min. Laurita Vaz), que assenta: *"A ausência de apreensão da droga com o acusado inviabiliza a condenação pelo crime de tráfico de entorpecentes, dada a falta de comprovação da materialidade delitiva"*.

### 🛡️ Ponto Forte 3: Confissão do Delegado Afastando a Associação Criminosa (Art. 35)
* **Argumento:** Em depoimento colhido sob o crivo do contraditório (transcrição de audiência, ~45min), a própria autoridade policial que presidiu o inquérito (**Delegado Dr. Nelson Esquiba**) declarou em juízo:
  > *"Eu não indiciei eles no crime de organização criminosa... não havia aquela divisão hierarquizada nem estrutura armada..."*
* **Impacto:** Ruína do crime de Associação para o Tráfico (Art. 35), demonstrando que o suposto "delivery" tratava-se de mero concurso eventual de agentes/usuários.

### 🛡️ Ponto Forte 4: Condições Pessoais Favoráveis Comprovadas
* **Argumento:** Juntada aos autos da Carteira de Trabalho (CTPS anotada com emprego formal ativo), Comprovante de Residência Fixa e primariedade técnica.

---

## 🚨 3. BRECHAS LEGAIS E NULIDADES MAPEADAS

### ⚖️ Brecha 1: Nulidade da Prova Telemática / WhatsApp sem Preservação de Hash (Tema 1.062/STF)
* **Fundamentação:** A imputação de autoria se apoia em supostas mensagens e áudios de WhatsApp. O perito/polícia não realizou a extração forense com preservação de hash nem confronto vocálico dos áudios.
* **Aplicação:** Jurisprudência da 6ª Turma do STJ e Tema 1.062 do STF (prints de WhatsApp e transcrições unilaterais sem espelhamento periciado são nulos).

### ⚖️ Brecha 2: Vício na Notificação / Tentativa de Intimação Informal por WhatsApp
* **Fundamentação:** O Delegado admitiu em juízo ter tentado intimar o acusado por aplicativo de mensagens WhatsApp e por recados a familiares.
* **Aplicação:** Nulidade dos atos de citação/intimação informal no processo penal (Art. 564, III, "e" do CPP).

### ⚖️ Brecha 3: Inaplicabilidade da Agravante da Pandemia (Art. 61, II, "j" do CP)
* **Fundamentação:** O MP imputou a agravante da calamidade pública pelo fato dos eventos ocorrerem durante a pandemia de COVID-19.
* **Aplicação:** A jurisprudência do STJ exige a comprovação de que o agente se aproveitou conscientemente do estado de calamidade para facilitar a empreitada criminosa, vedada a incidência automática pelo mero critério temporal.

---

## ⚡ 4. PLANO DE AÇÃO ESTRATÉGICO DA DEFESA

1. **Frente 1 — STJ (Brasília):** Acompanhamento diário da juntada do Parecer do MPF no `HC 1.116.750/RJ` e sustentação oral / entrega de memoriais no gabinete do Relator Min. Og Fernandes focando no Art. 580 do CPP.
2. **Frente 2 — 1ª Instância (Búzios):** Elaboração de Alegações Finais focando na descaracterização do Art. 35 (com base no depoimento do Delegado Nelson Esquiba) e na absolvição/desclassificação do Art. 33 por falta de materialidade direta.

"""

with open(md_path, "w", encoding="utf-8") as f:
    f.write(doc_content)

print(f"Relatório Mestre salvo em {md_path}")

# Gravar no memU SQLite
mem_id = str(uuid.uuid4())
now_str = datetime.now().isoformat()

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO memu_recall_files (id, created_at, updated_at, name, track, description, content, user_id, agent_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, 'default_user', 'antigravity')
    """, (
        mem_id,
        now_str,
        now_str,
        "Dossie_Analise_Integral_Pontos_Fortes_e_Brechas_Julio",
        "Julio_Pereira_Marcos_Caso_Principal",
        "Análise estratégica integral do processo de Júlio Pereira Marcos: Síntese fática, 4 Pontos Fortes, 3 Brechas Legais/Nulidades e Plano de Ação",
        doc_content
    ))
    conn.commit()
    conn.close()
    print(f"SUCESSO: Memória registrada no memU SQLite com ID: {mem_id}")
except Exception as e:
    print(f"Erro no memU: {e}")
