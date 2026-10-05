# plan.md - Project Orchestration Plan

## 1. Classificação do Problema
- **Categoria**: SWE (Software Engineering) / Scraping / Document Processing
- **Integrity Mode**: Demo (permite fallbacks robustos/mocks para fins de demonstração se houver indisponibilidade ou bloqueios insolúveis no tribunal real)

## 2. Decomposição do Projeto
O projeto será dividido em duas trilhas principais rodando em paralelo inicialmente:

### Trilha 1: E2E Testing Track (Criação de Testes)
- **Objetivo**: Criar o conjunto de testes de ponta a ponta (Tiers 1-4) para validar os requisitos R1 e R2.
- **Entregável**: `TEST_READY.md` e os arquivos de testes automatizados em `tests/`.

### Trilha 2: Implementation Track (Implementação das Funcionalidades)
- **Marco 1 (M1) - Scraping Automático (R1)**:
  - Otimizar ou criar um script de scraping que consiga obter um documento (PDF, HTML ou texto) para o processo `0011857-95.2024.8.19.0002` de forma não-bloqueante (sem necessidade de MessageBoxW ou intervenção humana direta, usando mock/fallback se a página do TJRJ estiver indisponível ou apresentar captcha intransponível).
- **Marco 2 (M2) - Processamento e Geração de Linha do Tempo (R2)**:
  - Desenvolver processador para ler o documento baixado e extrair fatos + gerar linha do tempo em formato markdown/json.
- **Marco 3 (M3) - Integração com Streamlit App**:
  - Integrar os novos fluxos automáticos na interface do dashboard `app.py`.

## 3. Estratégia de Verificação
- Execução de testes automatizados unitários e de integração.
- Auditoria de integridade para garantir que as implementações não contêm trapaças (mocking abusivo de testes ou bypass fictício).
