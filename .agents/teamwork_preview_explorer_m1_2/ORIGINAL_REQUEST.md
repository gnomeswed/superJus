## 2026-07-03T19:14:07Z
You are M1 Explorer 2. Your working directory is: c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_explorer_m1_2\
Please read c:\Projetos\Super Analista Jurídico\PROJECT.md and analyze how to implement scripts/tjrj_scraper_auto.py.
Your goal is to propose an implementation strategy for the scraping service:
- Function contract: scrape_process_documents(process_number: str, save_dir: str) -> list[str]
- Requirements: Download process documents automatically without GUI prompts. In 'Integrity mode: demo', handle offline/blocked scenarios with a fallback to mock documents (e.g. from Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/ if the process number matches 0011857-95.2024.8.19.0002).
- Investigate scripts/tjrj_extractor.py and scripts/court_scraper.py to see if there is any code or logic to reuse or adapt.
- Propose a clean architecture for scripts/tjrj_scraper_auto.py.
- Write your analysis and implementation strategy to c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_explorer_m1_2\analysis.md and notify me (the sub-orchestrator).
