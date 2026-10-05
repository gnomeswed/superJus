## 2026-07-03T19:28:56Z
You are M1 Worker (Fix 2 Generation). Your working directory is: c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_worker_m1_fix2\
Please refine the input validation logic in `scripts/tjrj_scraper_auto.py` based on the challenger's feedback:
1. Strip leading and trailing whitespace from the input `process_number` string at the very beginning of `scrape_process_documents`.
2. Apply a strict CNJ format check. The stripped `process_number` must match either:
   - Exactly 20 digits: `^\d{20}$`
   - Or the standard CNJ mask: `^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$`
   If it matches neither, raise a `ValueError` with an appropriate message immediately.
3. Remove the old length/separators check logic so that it is replaced by this robust pattern.
4. Execute the test suite using `python -m unittest tests.test_e2e_scraping_analysis` to ensure it passes.
5. Save your changes report to c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_worker_m1_fix2\changes.md and handoff to handoff.md.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.
