# Synthesis: M1 Scraping Automatizado Strategy

## Consensus
All three explorers agree on the core design:
1. **API Signature**: `scrape_process_documents(process_number: str, save_dir: str) -> list[str]` in `scripts/tjrj_scraper_auto.py`.
2. **Sanitization**: Process number must be cleaned of non-digits using regex `re.sub(r'\D', '', process_number)`.
3. **Demo Mode / Fallback**: Check `os.environ.get("INTEGRITY_MODE", "demo")`. If `"demo"` and cleaned number matches `"00118579520248190002"`, copy all documents from `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo` to `save_dir`.
4. **No GUI Dialogs**: Remove all dialog boxes (like `MessageBoxW` used in `tjrj_extractor.py`) to prevent blocking headless/automated runners.
5. **Playwright Automation**: Use headless Playwright to automatically search, configure pagination ("Todos os Movimentos" and "500 por página"), and extract the modal texts.

## Resolved Conflicts
No conflicts identified. The design is unified.

## Gaps & Risk Management
1. **Playwright Availability**: The code must handle the absence of `playwright` library gracefully by falling back to mock files in demo mode and logging the warning.
2. **Demo Mode Fallback triggers**: Fallback must be triggered if real scraping fails (due to connection issues, captchas, etc.) OR if it's in demo mode and the test process number is requested.

## Action Plan
Dispatch a worker to implement `scripts/tjrj_scraper_auto.py` based on the design.
