## 2026-07-03T19:15:31Z

Your task is to implement `scripts/tjrj_scraper_auto.py` based on the synthesis strategy:
- Function contract: `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`
- Behavior: Clean the process number, check `INTEGRITY_MODE` (default to 'demo').
- Fallback flow: If `INTEGRITY_MODE == 'demo'` and the process number is '0011857-95.2024.8.19.0002' (or its cleaned version), copy all files from `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/` to `save_dir` and return their absolute paths.
- Scraping flow: Use headless Playwright without GUI prompts (no MessageBoxW). Automate process search by locating `iframe#mainframe`, entering process number, submitting, pagination ("Todos os Movimentos", "500 por página"), and modal scraping.
- Fallback on error: If online scraping fails, or Playwright is not installed, fallback to copying mock files if in demo mode.
- Report all changes in c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_worker_m1\changes.md and write a handoff report in c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_worker_m1\handoff.md.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
