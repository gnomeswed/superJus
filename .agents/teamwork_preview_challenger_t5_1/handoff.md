# Handoff Report — Adversarial Coverage Hardening

## 1. Observation
During the static analysis of the scraper and timeline/summary scripts, the following code-level issues were observed:
- In `scripts/tjrj_scraper_auto.py` (lines 291-314), the modal parsing loop checks `len(txt) > 50` and will sleep for 15 seconds without saving if a court document is short (length $\le 50$).
- In `scripts/process_and_timeline.py` (line 144), the judge heuristic regex is `rf"{indicator}\s*(?:[Dd]r\(a\)\.?)?\s*([A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇÃÕ][a-záéíóúâêîôûàèìòùçãõ\s]+)"`, which only allows lowercase letters after the first capital letter. This fails for all-caps judge names (e.g. `"MARCOS SILVA"`) and truncates names with uppercase initials (e.g. `"Marcos Silva"` is truncated to `"Marcos "`).
- In `scripts/process_and_timeline.py` (lines 21-30), if the input path does not exist, it silently appends a fallback timeline entry instead of raising a `FileNotFoundError`.
- In `scripts/process_and_timeline.py` (lines 53, 63), text and HTML files are read using `encoding='utf-8', errors='ignore'`, causing silent corruption on Latin-1/CP1252 files.
- In `scripts/process_and_timeline.py` (lines 36-50), the try-except block is outside the PDF page parsing loop, causing the reader to skip the entire PDF document if a single page raises an exception.
- In `scripts/tjrj_scraper_auto.py` (lines 404-408), `DEMO_MODE` is strictly compared to `"True"` (case-sensitive), skipping fallback mode if set to standard lowercase `"true"` or `"1"`.
- In `scripts/tjrj_scraper_auto.py` (lines 431-441), Datajud exception handling is wrapped in `except Exception: pass`, swallowing all errors.
- In `scripts/tjrj_scraper_auto.py` (lines 327-330), `extracted_playwright.txt` is overwritten with `"w"` for each document, losing all data except the final document.

## 2. Logic Chain
1. If a document has short content, it fails the `len(txt) > 50` check, meaning it won't break the loop, causing a 15-second loop and returning `None`.
2. A regex matching `([A-Z][a-z\s]+)` cannot match multiple uppercase letters in sequence (like `MARCOS`) because the repeating block specifies lowercase (`[a-z...]`). Thus, all-caps judge names fail completely.
3. Standard environments define boolean env vars in lowercase (like `true`). If this isn't caught, production mode will be entered unexpectedly, causing scraper failures.
4. Latin-1 encodes characters like `ã` as single bytes that are invalid in UTF-8, resulting in dropped letters when parsed with `errors='ignore'`, which breaks name extraction.

## 3. Caveats
- Terminal execution timed out due to approval latency, so no unit tests were run interactively. The findings rely on static analysis.
- Live Datajud API credentials and rate limits were not tested.

## 4. Conclusion
- There are 8 significant gaps in the existing code. Implementing unit tests matching the designs in `gap_report.md` will protect the codebase against these real-world failure modes.

## 5. Verification Method
- Inspect the gap report at: `c:\Projetos\Super Analista Jurídico\.agents\teamwork_preview_challenger_t5_1\gap_report.md`
- Inspect code files `scripts/tjrj_scraper_auto.py` and `scripts/process_and_timeline.py` to confirm observed lines.
- Run tests (once environment allows):
  `python -m unittest tests/test_e2e_scraping_analysis.py`
