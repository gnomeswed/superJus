# Handoff Report — Analisador Jurídico do Raspador Automatizado (M1 Explorer 3)

## 1. Observation
We have inspected the workspace, directory structures, and the codebase files. The key observations include:

1. **Interface Contract and File Layout** (`c:\Projetos\Super Analista Jurídico\PROJECT.md`):
   - Line 20: `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`
   - Line 28: `- `scripts/tjrj_scraper_auto.py` - Scraper automático.`
2. **GUI Prompt & Playwright Setup** (`c:\Projetos\Super Analista Jurídico\scripts\tjrj_extractor.py`):
   - Lines 56-57: `def extract_tjrj(process_number: str, save_dir: str, headless: bool = False) -> str:`
   - Lines 72-80: `ctypes.windll.user32.MessageBoxW(0, "Uma NOVA JANELA do Chromium será aberta...", "Extrator TJRJ", 0x40 | 0x10000)`
3. **Datajud CNJ metadata extractor** (`c:\Projetos\Super Analista Jurídico\scripts\court_scraper.py`):
   - Lines 8-31: Maps clean CNJ numbers to specific tribunal aliases like `tjrj`.
4. **Mock case folder and metadata** (`c:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\case_meta.json`):
   - Line 3: `"numero_processo": "0011857-95.2024.8.19.0002"`
5. **Project request constraint** (`c:\Projetos\Super Analista Jurídico\ORIGINAL_REQUEST.md`):
   - Line 8: `Integrity mode: demo`
6. **Network Mode Restriction**:
   - The subagent runs in `CODE_ONLY` network mode, which denies external network traffic and prevents actual connections to TJRJ portal.

---

## 2. Logic Chain
1. Based on Observation 1, the new scraper must implement `scripts/tjrj_scraper_auto.py` and export a public function `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`.
2. Based on Observation 2, `tjrj_extractor.py` relies on `ctypes.windll.user32.MessageBoxW` to pause and alert users, and runs with `headless=False` by default. To fulfill the requirement of "downloading process documents automatically without GUI prompts", we must configure Playwright to run in `headless=True` by default and automate both the search text filling and form submission instead of pausing for manual user action.
3. Based on Observation 4 and Observation 5, in `Integrity mode: demo` and when offline/blocked (which is guaranteed in this sandbox due to the `CODE_ONLY` network restriction in Observation 6), the scraper must fallback to mock documents.
4. We can design a dynamic mock mapper that parses the folder structure under `Clientes/` and looks at `case_meta.json` (as observed in Observation 4) to resolve the correct case directory and copy mock documents (PDF, TXT, HTML) to the target directory. If the process matches `0011857-95.2024.8.19.0002`, it resolves to `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/`.

---

## 3. Caveats
- **Selector changes**: Since the real TJRJ website could update its layout, the automatic selectors used for filling the process number and clicking search (e.g. `input#numeroProcesso`, `button:has-text('Pesquisar')`) must degrade gracefully. If they fail, the scraper logs the warning and falls back to mock documents when `INTEGRITY_MODE == "demo"`.
- **Playwright availability**: Since Playwright requires browser binaries to run, headless execution could fail if chromium is not installed. The design handles this by checking if `playwright` is installed and falling back to mocks if unavailable under demo mode.

---

## 4. Conclusion
We propose the complete implementation strategy and architecture code for `scripts/tjrj_scraper_auto.py`, written in `analysis.md` in the working directory. It handles:
- Unified and split CNJ inputs.
- Auto-expansion of movements and pagination to 500 items per page.
- Clean modal navigation and cleanup based on `tjrj_extractor.py`.
- Dynamic offline fallback resolving to `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo` for the target test process.

---

## 5. Verification Method
To verify the implementation of the proposed strategy:
1. Confirm that `scripts/tjrj_scraper_auto.py` exists and implements `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`.
2. Run the test command:
   ```powershell
   python -m pytest -v tests/test_e2e_scraping_analysis.py
   ```
3. Verify that running `scrape_process_documents("0011857-95.2024.8.19.0002", "./test_save_dir")` in a disconnected state successfully populates `./test_save_dir` with the mock files and returns their absolute paths.
