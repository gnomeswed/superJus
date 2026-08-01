# Project: Super Analista Jurídico - Scraping e Análise

## Architecture
- `scripts/court_scraper.py`: Consulta metadados gerais via Datajud API.
- `scripts/tjrj_extractor.py`: Extrator de documentos via Playwright (atualmente semi-manual com GUI).
- `scripts/ai_engine.py`: Interface com DeepSeek API.
- `app.py`: Interface Web Streamlit.
- `core/`: Módulos internos para processamento de documentos e agentes.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | E2E Testing Track | Desenvolver infraestrutura de testes Tiers 1-4 e publicar TEST_READY.md | None | PLANNED |
| 2 | M1: Scraping Automatizado (R1) | Desenvolver download automático de documentos de processos (com mock/fallback demo) | E2E Testing Track | PLANNED |
| 3 | M2: Processamento e Linha do Tempo (R2) | Processar documentos baixados gerando resumo de fatos e linha do tempo | M1 | PLANNED |
| 4 | M3: Integração Streamlit | Integrar os fluxos de Scraping (R1) e Linha do Tempo (R2) na interface do Streamlit | M2 | PLANNED |

## Interface Contracts
### Scraping Service
- Função: `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`
- Retorna lista de caminhos locais dos arquivos baixados/salvos.

### Analysis Service
- Função: `generate_timeline_and_summary(doc_path: str, output_path: str) -> dict`
- Salva o resumo dos fatos e linha do tempo no `output_path` (Markdown/JSON) e retorna os dados estruturados.

## Code Layout
- `scripts/tjrj_scraper_auto.py` - Scraper automático.
- `scripts/process_and_timeline.py` - Processador de fatos e linha do tempo.
- `tests/test_e2e_scraping_analysis.py` - Testes E2E (Tiers 1-4).
