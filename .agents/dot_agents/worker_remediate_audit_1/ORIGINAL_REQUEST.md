## 2026-07-03T19:25:12Z

You are teamwork_preview_worker.
Your working directory is: c:\Projetos\Super Analista Jurídico\.agents\worker_remediate_audit_1\
Please create this directory and write your briefing.md / progress.md.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Tasks:
1. Create the production script `scripts/process_and_timeline.py` to genuinely implement `generate_timeline_and_summary(doc_path: str, output_path: str) -> dict`.
   Features of this implementation:
   - Accept either a single file path or a directory of files.
   - For each file:
     * If `.pdf`, use `pypdf` (PdfReader) to genuinely extract text from all pages. Handle/log read exceptions and corrupted/empty PDF files gracefully.
     * If `.html` or `.htm`, use `bs4` (BeautifulSoup) to strip tags and extract plain text.
     * If `.txt` or `.md`, read the file as plain text.
   - Aggregate all extracted text. If the aggregated text exceeds 100,000 characters, truncate it and append `... [TRUNCATED]`.
   - Timeline & Metadata Extraction:
     * If `DEEPSEEK_API_KEY` is present in `os.environ`, use `openai.OpenAI` client targeting `https://api.deepseek.com` and model `deepseek-chat` to get summary, timeline, judge name, and contradictions.
     * If `DEEPSEEK_API_KEY` is absent/empty, run a genuine heuristic fallback:
       - Use regex `\d{2}/\d{2}/\d{4}` to find all dates in the text.
       - Extract the surrounding sentence/line as the event description.
       - Sort timeline events chronologically.
       - Scan the text for judge indicators (e.g. "Juiz de Direito", "Magistrado") to extract a judge name, defaulting to "Juiz Heurístico".
       - Create a summary from the first 200 characters of the text.
   - Save the results as JSON (if `output_path` ends with `.json`) or Markdown/text otherwise.
   - Return the structured dict.

2. Modify `tests/test_e2e_scraping_analysis.py`:
   - Remove ALL fallback stub implementations of `scrape_process_documents` and `generate_timeline_and_summary`.
   - Import the contract functions directly from `scripts.tjrj_scraper_auto` and `scripts.process_and_timeline`.
   - Update any test case that generated dummy files to generate genuine test files. Specifically, for PDF test cases (such as `test_analysis_single_pdf_file` and `test_combo_mixed_format_scrape_to_analysis`), use `fpdf2` (`from fpdf import FPDF`) to dynamically generate valid PDF files containing target test text (like "Denúncia oferecida em 10/05/2026").
   - Ensure `setUp` defines `os.environ["INTEGRITY_MODE"] = "production"` and `os.environ["DEMO_MODE"] = "False"`.

3. Run the test command: `python -m unittest tests/test_e2e_scraping_analysis.py`. Respond to the system shell permission prompt immediately to execute successfully.
4. Verify all 30 tests pass.
5. Write your handoff report (c:\Projetos\Super Analista Jurídico\.agents\worker_remediate_audit_1\handoff.md) showing the command execution output and status, and send a message when done.
