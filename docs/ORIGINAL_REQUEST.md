# Original User Request

## Initial Request — 2026-07-03T16:12:21-03:00

Otimizar e expandir o Super Analista Jurídico para que ele seja capaz de baixar automaticamente os documentos de processos, analisá-los e extrair as informações jurídicas relevantes.

Working directory: c:\Projetos\Super Analista Jurídico
Integrity mode: demo

## Requirements

### R1. Scraping de Documentos
O sistema deve ser capaz de realizar web scraping diretamente dos sistemas públicos dos tribunais para baixar as peças e documentos originais do processo (lidando com possíveis bloqueios/captchas).

### R2. Análise e Linha do Tempo
Após baixar os documentos, o sistema deve processá-los automaticamente para extrair um resumo dos fatos e montar uma linha do tempo detalhada (cronologia processual).

## Verification Resources
Processo de Teste: 0011857-95.2024.8.19.0002

## Acceptance Criteria

### Scraping
- [ ] O script consegue receber um número de processo de teste e realizar o download bem-sucedido de pelo menos um documento (PDF ou HTML) da pasta do processo, salvando-o localmente.

### Processamento e Análise
- [ ] O script processa o documento baixado com sucesso e gera um arquivo (ex: markdown ou json) contendo uma linha do tempo e um resumo legível dos fatos do processo.
