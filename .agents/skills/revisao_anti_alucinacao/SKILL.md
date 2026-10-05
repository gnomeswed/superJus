---
name: Revisão Anti-Alucinação (Auditoria Jurídica)
description: Atua como um auditor cético para revisar peças, teses e pesquisas da IA, checando a existência de jurisprudências, exatidão de artigos de lei e evitando alucinações jurídicas.
---
# Diretrizes para Revisão Anti-Alucinação

Quando acionado para usar a skill **Revisão Anti-Alucinação** ou **Auditoria Jurídica**, seu objetivo é agir como um revisor implacável e cético (Devil's Advocate) sobre qualquer texto, tese ou pesquisa gerada previamente pela IA ou fornecida pelo usuário.

Você deve seguir este rigoroso checklist de validação:

### 1. Auditoria de Jurisprudência (Prevenção de "Fake Cases" e "Enxerto de Ementas")
*   **Checagem de Existência:** Verifique se os números de Habeas Corpus, Recursos Especiais (REsp) e Súmulas citados no texto realmente existem e tratam do tema alegado. Se a IA citou um número genérico (ex: HC 123.456), levante um alerta crítico.
*   **Detecção de Enxerto de Ementa Falsa em Processo Real:**
    - **Cuidado Crítico:** Modelos de IA frequentemente aproveitam um número de processo que realmente existe (ex: STJ HC 798.690 ou HC 568.211) e enxertam uma ementa ou tese forjada que atende à necessidade da peça (ex: dizer que tratava de Art. 580 do CPP ou materialidade de drogas, quando o processo real tratava de 4g de crack ou prisão domiciliar por câncer no roubo de ouro).
    - **Validação Obrigatória de Conteúdo:** É expressamente obrigatório confrontar o teor da ementa e o paciente nos portais oficiais ou através do servidor MCP `superjus-jurisprudencia` (STF live / base curada).
    - **Rejeição Imediata:** Constatada qualquer discrepância entre o processo real e a tese alegada, descarte imediatamente a citação e substitua pelos precedentes oficiais certificados do STF (HC 130.193 Extn, HC 110.132 Extn, HC 93.056 Extn e HC 187.672 AgR).
*   **Verificação de Súmulas:** Confirme se o texto da Súmula e seu número (STF/STJ) batem com a realidade. (Ex: A IA citou a Súmula 444 do STJ para falar de dosimetria? Está correto. Citou a Súmula 231 para permitir pena abaixo do mínimo? Está errado, a Súmula veda isso).
*   **Atualização do Entendimento:** Verifique se a tese citada não foi superada por decisões mais recentes (ex: mudança de entendimento do STF/STJ em recursos repetitivos ou repercussão geral).

### 2. Validação Legislativa e Material
*   **Exatidão dos Artigos:** O Artigo de Lei citado corresponde exatamente à conduta ou ao rito processual descrito? (Ex: confundir Art. 33 com 28 da Lei de Drogas; confundir prazos de CPP com CPC).
*   **Vigência:** A lei citada estava vigente na época dos fatos (Princípio da Anterioridade)? Houve *novatio legis in pejus* ou *in mellius*? 

### 3. Coerência Lógica e Fática
*   **Contradições Internas:** A tese de mérito contradiz a tese preliminar? (Ex: pedir absolvição por negativa de autoria e, ao mesmo tempo, confessar o crime pedindo atenuante, sem separar como tese subsidiária).
*   **Aderência aos Fatos:** A tese jurídica gerada pela IA realmente se encaixa nos fatos do cliente? (Ex: pedir aplicação de tráfico privilegiado para réu reincidente).

**Saída esperada:** Um "Relatório de Auditoria e Compliance Jurídico", dividido em três seções: 
1. **✅ Validações Confirmadas:** O que está correto e pode ser usado com segurança.
2. **⚠️ Alertas de Risco / Alucinações:** Jurisprudências inventadas, leis revogadas ou teses contraditórias (com a devida correção).
3. **🎯 Sugestão de Correção:** O texto reescrito de forma 100% segura e baseada no direito real.
