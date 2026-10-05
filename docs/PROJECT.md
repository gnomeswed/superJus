# Project: Super Analista Jurídico — Scraping e Análise (superJus)

## Arquitetura
- `core/app.py`: Interface Web Streamlit (entrada).
- `core/config.py`, `core/process_model.py`: configuração central e contratos de movimentações.
- `scripts/tjrj_scraper_auto.py`: scraping automático TJRJ + DataJud (`scrape_process_documents`).
- `scripts/process_and_timeline.py`: geração de timeline/resumo (`generate_timeline_and_summary`).
- `scripts/telegram_monitor_julio.py`, `scripts/telegram_bridge.py`: monitoramento e ponte Telegram.
- `core/`: document_processor, jurisprudence_tool, legal_agent, vector_store.

## Execução
- App: `python -m streamlit run core/app.py` ou `scripts/INICIAR_SISTEMA.bat` (usa %~dp0, .venv na raiz).
- Pipeline: `python -m scripts.run_pipeline 0011857-95.2024.8.19.0002 --out Clientes/Processo_X`
- Diagnóstico: `python scripts/doctor.py`
- Playwright: `python -m playwright install chromium`
- Testes: `python -m pytest tests -m "not live" -q` e `python -m pytest --cov=core --cov=scripts --cov-report=term-missing`

## Contratos
- `scrape_process_documents(process_number, save_dir) -> list[str]` — lista de arquivos salvos.
- `generate_timeline_and_summary(doc_path, output_path) -> dict` — escreve JSON/Markdown com `{version, summary, timeline, judge, analysis_source, documents}`.

## Layout
- `core/app.py`, `scripts/*`, `tests/*`, `.agents/*` (estado local), `.env` (segredos não versionados).

Agrupa milestones em fases do plano (segurança → configuração → monitor → pipeline → dependências/testes → documentação).
