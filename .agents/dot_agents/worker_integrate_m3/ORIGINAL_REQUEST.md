## 2026-07-04T00:12:43Z

You are the Streamlit Integration Worker.
Your working directory is: c:\Projetos\Super Analista Jurídico\.agents\worker_integrate_m3\
Your task is to integrate the automated scraping and timeline processing services into app.py (Milestone 3), run the E2E test suite, and ensure everything functions perfectly.

Specifically:
1. View app.py around lines 755-779 where "Atualização Eletrônica TJRJ" is implemented.
2. Modify app.py to:
   - Import `scrape_process_documents` from `scripts.tjrj_scraper_auto` and `generate_timeline_and_summary` from `scripts.process_and_timeline`.
   - When the user clicks the update button (e.g. "Abrir Extrator TJRJ" or you can update/rename it to "Executar Atualização TJRJ"), it should call `scrape_process_documents(process_number_tjrj.strip(), save_dir)` to fetch documents.
   - Then, it should call `generate_timeline_and_summary(save_dir, out_path)` (where out_path is `os.path.join(case_path, "analises", "Relatorio_Processo.json")`) to process the downloaded documents, extract the timeline and summary.
   - Update the case's `timeline.json` using the timeline returned in `result["timeline"]` by transforming and writing it via the `save_timeline` helper in app.py.
   - Provide clean error handling and progress indicators (using `st.spinner`, `st.success`, `st.error`).
3. Run the E2E test suite to verify that your changes did not break any test scenarios:
   python -m unittest tests/test_e2e_scraping_analysis.py
4. If there are any test failures, investigate and resolve them.
5. Once completed, write a detailed handoff.md in your directory.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
