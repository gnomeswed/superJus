## 2026-07-04T05:01:44Z

Implement the bug fixes in `scripts/tjrj_scraper_auto.py` and `scripts/process_and_timeline.py` and add adversarial test cases to `tests/test_e2e_scraping_analysis.py` to cover all identified gaps from the two Challenger gap reports (located in `.agents/teamwork_preview_challenger_t5_1/gap_report.md` and `.agents/teamwork_preview_challenger_t5_2/gap_report.md`).

MANDATORY INTEGRITY WARNING:
> DO NOT CHEAT. All implementations must be genuine. DO NOT
> hardcode test results, create dummy/facade implementations, or
> circumvent the intended task. A Forensic Auditor will independently
> verify your work. Integrity violations WILL be detected and your
> work WILL be rejected.

Gaps to Address:
1. Filename Truncation Truncates Extensions: Ensure `_sanitize` or file saving truncates only the base name so the extension `.txt` is always preserved.
2. Heuristic Judge Regex Fails on Uppercase Names: Modify the regex pattern in `process_and_timeline.py` to correctly extract judge names in all-caps (e.g. "DR. MARCOS SILVA").
3. LLM Judge Extraction Regex matches only "Dr" / "Dra" when a dot is present. Fix the regex in `process_and_timeline.py` to not terminate lazily at the dot of "Dr.".
4. LLM API Failure/Timeout: In `process_and_timeline.py`, wrap OpenAI client creation and `create` calls in try/except blocks to fall back to heuristic analysis when the API is down or unavailable.
5. Short Court Document Loss: In `tjrj_scraper_auto.py`, modify the modal extraction loop so it doesn't ignore documents containing <= 50 characters, and avoids hanging for 15 seconds.
6. Consecutive Identical Document Skip: In `tjrj_scraper_auto.py`, avoid skipping consecutive documents with identical content or hanging for 15 seconds on them.
7. Non-UTF-8 Encoding Corruption: In `process_and_timeline.py`, decode Latin-1/CP1252 files correctly (try decoding as UTF-8 first, and fall back to CP1252/Latin-1 if there's a decoding error, rather than blindly ignoring characters with errors='ignore').
8. Playwright Fallback to Lucas Freitas: Ensure paths resolve correctly and handle directory access exceptions.
9. Playwright Search Form Submission Failure: Ensure form submission errors are handled/logged correctly.
10. Datajud API Swallowed Exceptions & HTTP / URLError: Ensure exceptions are logged instead of swallowed with `pass`. Handle URLErrors/other codes gracefully.
11. API Token Waste on Empty Content: Do not call the DeepSeek API if there is no text content to analyze.
12. Playwright fallback to Lucas Freitas in demo mode: ensure this path is robustly covered by tests.

Verification:
Write new test cases in `tests/test_e2e_scraping_analysis.py` for each of these scenarios. Run the entire test suite (using `python -m unittest tests/test_e2e_scraping_analysis.py` or similar command) to verify all tests pass.
Write your findings and test execution output to `.agents/worker_t5_1/handoff.md` and send a message when done.
