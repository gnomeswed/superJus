---
name: "Dossiê para a Família (Gerador de PDF)"
description: "Cria um relatório em PDF com linguagem clara para apresentar à família do réu a situação do processo, incluindo pontos fracos e favoráveis da defesa."
---

# Diretrizes da Skill: Dossiê para a Família

Você foi acionado para gerar um dossiê voltado para a família do cliente. O objetivo não é ser uma peça jurídica, mas um documento claro, acolhedor e estratégico para que os familiares entendam a real situação do processo, sem o "juridiquês" excessivo.

## 1. Estrutura do Dossiê

O documento deve obrigatoriamente conter as seguintes seções:
1. **Cabeçalho:** Nome do cliente, número do processo, e fase atual (ex: Aguardando Recurso de Apelação).
2. **Resumo da Situação:** Uma explicação simples de 1 ou 2 parágrafos sobre onde o processo está parado agora e o que aconteceu recentemente (ex: "Ocorreu o júri e ele foi condenado, mas já recorremos").
3. **A Ameaça (Pontos Fracos do Processo):** O que está pesando contra o cliente (provas desfavoráveis, depoimentos de acusação, decisões duras do juiz). Seja realista para alinhar as expectativas da família.
4. **A Esperança (Coisas Favoráveis e Estratégia):** O que a defesa descobriu de errado no processo (ex: contradições, provas nulas, pena calculada errada) e qual é o plano de ação exato que estamos executando para reverter a situação.
5. **Próximos Passos:** O que vai acontecer agora e uma estimativa de prazos (ex: "Julgamento do Habeas Corpus em 30 dias").

## 2. Instruções de Execução

1. **Gere o Conteúdo:** Primeiro, rascunhe internamente o conteúdo do dossiê baseado na análise prévia do processo.
2. **Gere o Arquivo Markdown:** Salve o conteúdo em um arquivo temporário `.md` na pasta do cliente, ex: `dossie_familia.md`.
3. **Converta para PDF:** Execute o script Python `gerar_pdf.py` (localizado na pasta `scripts` desta skill) passando o arquivo markdown gerado como parâmetro para transformá-lo em um PDF apresentável.

## 3. Script Auxiliar

Use o comando abaixo no terminal para rodar o script (substituindo pelos caminhos reais):
```bash
python "c:\Projetos\Super Analista Jurídico\.agents\skills\dossie_familia\scripts\gerar_pdf.py" "c:\caminho\para\o\dossie_familia.md" "c:\caminho\para\o\Dossie_Familia_Nome_do_Cliente.pdf"
```
