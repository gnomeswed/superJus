# Handoff Report - M1 Scraping Strategy Analysis

## 1. Observation

Direct observations made in the workspace include:

1.  **Project contracts and layout** in `c:\Projetos\Super Analista Jurídico\PROJECT.md`:
    *   Line 20: `- Função: scrape_process_documents(process_number: str, save_dir: str) -> list[str]`
    *   Line 28: `- scripts/tjrj_scraper_auto.py - Scraper automático.`
2.  **Metadata queries** in `c:\Projetos\Super Analista Jurídico\scripts\court_scraper.py`:
    *   Line 34: `clean_number = re.sub(r'\D', '', process_number)`
    *   Line 39: `url = f'https://api-publica.datajud.cnj.jus.br/api_publica_{tribunal_alias}/_search'`
3.  **Playwright scraping logic** in `c:\Projetos\Super Analista Jurídico\scripts\tjrj_extractor.py`:
    *   Line 72: `ctypes.windll.user32.MessageBoxW(` (forces blocking GUI prompt)
    *   Line 83: `browser = p.chromium.launch(headless=bool(headless))`
    *   Line 96: `el = page.query_selector("iframe#mainframe")`
    *   Line 205: `const m = document.querySelector("#descricaoDetalhadaModal .modal-body");`
4.  **Lucas Freitas Mock Case Metadata** in `c:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\case_meta.json`:
    *   Line 3: `"numero_processo": "0011857-95.2024.8.19.0002"`
5.  **Lucas Freitas Mock Case Document files** in `c:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\`:
    *   Contains 27 files including:
        *   `03-04-2025_Audiência Instrução e Julgamento.txt`
        *   `03-04-2025_Sentença em Audiência  - Proferida Sentença de Pronúncia.txt`
        *   `hrhe.pdf`
        *   `rad5CCBF.html`

---

## 2. Logic Chain

1.  **Contract Fulfillment**: The target function `scrape_process_documents` must output a list of file paths saved to `save_dir`. It is matched to `scripts/tjrj_scraper_auto.py` (Observation 1).
2.  **Automation Requirement**: The current implementation in `tjrj_extractor.py` relies on `ctypes.windll.user32.MessageBoxW` to notify the user, and an interactive Chromium loop that blocks execution (Observation 3). To automate this without GUI prompts, we must remove all user dialogues and launch Playwright in headless mode (`headless=True`), automating the input filling and submission.
3.  **Demo Fallback Routing**: In "Integrity mode: demo" under offline/blocked scenarios (Observation 1 & 4), the scraper must detect if the target process number matches the Lucas Freitas case `0011857-95.2024.8.19.0002` (Observation 4).
4.  **Mock Document Retrieval**: If the process number matches `0011857-95.2024.8.19.0002`, the Fallback Provider will locate all document files in `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/` (Observation 5), copy them to `save_dir`, and return their updated paths.
5.  **Clean Reusable Architecture**: By separating input cleaning (from `court_scraper.py` - Observation 2) and extraction logic (from `tjrj_extractor.py` - Observation 3) into helper modules, we can create a resilient system that executes online headless Playwright scraping and falls back on error or demo conditions.

---

## 3. Caveats

*   **Offline Mode Restrictions**: Because we are in CODE_ONLY offline mode, we cannot test the live Playwright selectors on the active TJRJ website during design. We assume the selector schema (`iframe#mainframe` and `#descricaoDetalhadaModal`) matches `tjrj_extractor.py`.
*   **CAPTCHA Blockage**: The TJRJ website frequently uses reCAPTCHA. A fully automated headless Playwright scraper will fail if it encounters CAPTCHA. In production, a captcha-bypass tool or semi-headless mode might be required. For this milestone, the fallback mechanism in `demo` mode satisfies the requirements during offline/blocked scenarios.

---

## 4. Conclusion

We have analyzed `court_scraper.py` and `tjrj_extractor.py` and formulated a clean architecture for `scripts/tjrj_scraper_auto.py`.
*   The script should automatically download process documents without GUI prompts using headless Playwright.
*   In demo mode, it will fall back to copying mock documents from `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/` to the target `save_dir` when offline or if the process number matches `0011857-95.2024.8.19.0002`.

---

## 5. Verification Method

Once implemented, the behavior can be verified using the following steps:
1.  **Environment Setup**: Set `INTEGRITY_MODE="demo"` in the environment variables.
2.  **Run Command**: Execute the following Python test script to call the scraper:
    ```powershell
    python -c "from scripts.tjrj_scraper_auto import scrape_process_documents; paths = scrape_process_documents('0011857-95.2024.8.19.0002', 'test_output_dir'); print(len(paths), paths)"
    ```
3.  **Inspect Results**:
    *   Verify that `test_output_dir/` is created.
    *   Verify that it contains the 20+ mock files from Lucas Freitas' folder.
    *   Verify that the console prints a list of valid absolute paths.
4.  **Invalidation Conditions**:
    *   Execution prints a Windows MessageBox or prompts the user.
    *   Files are not copied, or returned paths do not exist.
