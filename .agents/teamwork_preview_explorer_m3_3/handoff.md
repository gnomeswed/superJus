# Handoff Report: Integration of TJRJ Scraper and Timeline Generator

## 1. Observation

Direct observations from codebase inspection:

- **Old Import & Call Location**: In `app.py` (lines 768–778):
  - Line 768: `from scripts.tjrj_extractor import extract_tjrj`
  - Line 772: `result = extract_tjrj(process_number_tjrj.strip(), save_dir)`
  - The extraction results are outputted directly to the screen via `st.text(result)`.

- **Automated Scraper Signature**: In `scripts/tjrj_scraper_auto.py` (lines 382–459):
  - Function: `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`
  - Behavior: Runs Playwright headless chrome to extract documents or falls back on mock documents when in `demo` mode.

- **Timeline Generator Signature**: In `scripts/process_and_timeline.py` (lines 17–181):
  - Function: `generate_timeline_and_summary(doc_path: str, output_path: str) -> dict`
  - Return structure: 
    ```python
    {
        "summary": summary,
        "timeline": [{"date": "DD/MM/YYYY", "event": "...", "description": "..."}],
        "contradictions": [...],
        "judge": "..."
    }
    ```

- **Timeline Ingest and Display**: In `app.py` (lines 189–205 and 533–535):
  - Line 191: `tl_path = os.path.join(case_path, "timeline.json")`
  - Line 533: `timeline = load_timeline(case_path)`
  - Line 534: `dates = [e["date"] for e in timeline]`
  - Line 535: `events = [e["event"] for e in timeline]`

---

## 2. Logic Chain

1. **Automation without blocker**: The old `extract_tjrj` function blocks execution with a GUI MessageBox (`ctypes.windll.user32.MessageBoxW`). To run headlessly and automatically, we must replace it with the new `scrape_process_documents` function.
2. **Generating Report**: After documents are scraped to `save_dir`, calling `generate_timeline_and_summary(save_dir, out_path)` parses all documents in that directory, compiles a dict structure, and writes the full report to a JSON file (specified as `os.path.join(case_path, "analises", "Relatorio_Processo.json")`).
3. **Updating Case Timeline**: `load_timeline(case_path)` expects `timeline.json` to contain a list of objects with `"date"` and `"event"` keys.
   - The returned `result["timeline"]` is formatted with dates as `"DD/MM/YYYY"` and generic event names like `"Movimentação"`.
   - Transforming the date format to `"YYYY-MM-DD"` or `"YYYY-MM"` avoids Plotly timeline rendering/sorting issues.
   - Refining generic event labels using their descriptions (e.g. first sentence) makes the Plotly text tags descriptive and legible.
   - Writing the list of transformed items via `save_timeline` allows the UI to render the new timeline automatically upon calling `st.rerun()`.

---

## 3. Caveats

- **No live web execution**: Due to offline `CODE_ONLY` restrictions, Playwright was not executed against the live TJRJ court portal. Verification relies on the mock outputs of `scrape_process_documents` and `generate_timeline_and_summary`.
- **Plotly Label Clustering**: Multiple events falling on the same date node (e.g. `"2026-05"`) will render overlapping text on the scatter chart. Using the `"YYYY-MM-DD"` resolution helps scatter the points chronologically on the x-axis.

---

## 4. Conclusion

The integration of `scrape_process_documents` and `generate_timeline_and_summary` should replace the manual chrome launcher button in `app.py`. The scraper downloads the files, the timeline generator processes them to produce a JSON analysis report under `analises/`, and the extracted timeline is transformed and written to `timeline.json` to dynamically update the UI widget.

---

## 5. Verification Method

- **Static Analysis**: Verify in `app.py` that `scrape_process_documents` is imported and called, followed by `generate_timeline_and_summary`.
- **E2E Tests**: Run the existing scraper/analyzer test suite to ensure the underlying logic remains healthy:
  ```powershell
  python -m unittest tests/test_e2e_scraping_analysis.py
  ```
