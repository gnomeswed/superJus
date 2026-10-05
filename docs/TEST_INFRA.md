# Test Infrastructure (TEST_INFRA.md)

This document describes the 4-Tier Test Suite structure designed for verifying the **Super Analista Jurídico** Scraping and Analysis services.

## Test Directory Layout
- `tests/test_e2e_scraping_analysis.py`: Contains the 30 E2E and unit test cases spanning all four tiers.
- `tests/test_search_motoboy.py`: Pre-existing document search script.

## 4-Tier Test Architecture

### Tier 1: Feature Coverage (>= 5 Scraping, >= 5 Analysis)
Verifies the happy path, core features, and correct parameters of the modules.

#### Scraping Service
1. **`test_scrape_valid_cnj_format`**: Validates that the scraper correctly parses standard CNJ numbers, resolves the tribunal endpoint, and returns a list of files.
2. **`test_scrape_datajud_api_success`**: Verifies processing of a successful Datajud API response (extracting process class, subject, movements).
3. **`test_scrape_playwright_extraction`**: Verifies the browser-based Playwright routine extracts document details from iframe and modal structures.
4. **`test_scrape_save_dir_creation`**: Assures that if the designated `save_dir` does not exist, it is created automatically.
5. **`test_scrape_demo_fallback_trigger`**: Verifies that when network requests fail or demo mode is active, the scraper copies fallback demo files.

#### Analysis Service
6. **`test_analysis_single_txt_file`**: Parses a mock text document, invokes LLM analysis, and verifies the generated summary output structure.
7. **`test_analysis_single_pdf_file`**: Validates PDF document parsing (via PyPDF2 or PyPDFLoader patch) and extraction of structured text.
8. **`test_analysis_single_html_file`**: Assures HTML parsing correctly extracts text content (removing tags) for LLM prompts.
9. **`test_analysis_timeline_sorting`**: Ensures events with different dates are sorted chronologically.
10. **`test_analysis_deepseek_integration`**: Asserts prompt formats, parameters (temperature, max_tokens), and openai client integration.

### Tier 2: Boundary & Corner Cases (>= 5 Scraping, >= 5 Analysis)
Ensures robustness against erroneous, extreme, or empty inputs.

#### Scraping Service
11. **`test_scrape_invalid_cnj_number`**: Confirms that a malformed CNJ number raises a `ValueError` immediately.
12. **`test_scrape_datajud_empty_response`**: Gracefully handles situations where Datajud returns no hits (e.g., secret cases).
13. **`test_scrape_network_http_error`**: Assures that HTTP network errors (403, 500) from Datajud do not crash the script and return empty results.
14. **`test_scrape_playwright_timeout`**: Verifies that Playwright scraping exits cleanly with a default handler when elements time out.
15. **`test_scrape_read_only_save_dir`**: Checks that directory write permission errors are caught and raise a clean `PermissionError`.

#### Analysis Service
16. **`test_analysis_huge_file_token_limit`**: Assures very large documents (exceeding context limit) are chunked or truncated safely.
17. **`test_analysis_empty_or_corrupt_files`**: Validates that 0-byte or corrupted files are skipped without halting the queue.
18. **`test_analysis_missing_llm_key`**: Checks that if `DEEPSEEK_API_KEY` is absent, the system falls back to rule-based analysis or raises a specific configuration error.
19. **`test_analysis_missing_document_metadata`**: Handles documents with missing dates by placing them under a fallback default date (e.g., "sem_data").
20. **`test_analysis_output_path_write_failure`**: Verifies that if the target report directory is locked/unwritable, a handled exception is raised.

### Tier 3: Cross-Feature Combinations (>= 5 Combo Tests)
Verifies components interaction, data passing, and pipeline integrity.

21. **`test_combo_successful_scrape_to_analysis`**: Scrapes process files and directly pipes them into the analysis engine to output a final timeline report.
22. **`test_combo_partial_scrape_to_analysis`**: Handles partial scraper success (e.g., 3 out of 5 documents downloaded) and runs analysis on available files.
23. **`test_combo_mixed_format_scrape_to_analysis`**: Pipelines a mixture of PDF, TXT, and HTML files into the analyzer.
24. **`test_combo_empty_scrape_to_analysis`**: Gracefully handles an empty scrape result without executing the analysis.
25. **`test_combo_concurrent_scrape_and_analysis`**: Verifies that running multiple instances concurrently does not result in file/directory lock contentions.

### Tier 4: Real-World Application Scenarios (>= 5 Application Tests)
Verifies full pipelines, client workflows, and complex legal scenarios.

26. **`test_scenario_client_intake_triage`**: Simulates the complete triage flow from receiving a new CNJ number to outputting a structured legal triage report.
27. **`test_scenario_offline_demo_full_pipeline`**: Verifies the application's offline mode, executing scraping and timeline creation via local fallback assets.
28. **`test_scenario_contradiction_detection_pipeline`**: Verifies feeding two contradictory witness testimonies (e.g., differing facts/dates) generates a report flagging inconsistencies.
29. **`test_scenario_judge_profile_lawsuit_strategy`**: Analyzes decisions to extract the judge's name, profile history, and output customized strategic recommendations.
30. **`test_scenario_high_load_chronology`**: Stresses the system with 30+ documents to verify timeline ordering, performance time, and stability.

---

## Running the Tests
To execute the E2E test suite in the standard Python environment:
```powershell
python -m unittest tests/test_e2e_scraping_analysis.py
```

### Offline / CODE_ONLY Execution
The test suite utilizes extensive mocking of external networks, browser sessions (Playwright), and AI APIs (DeepSeek). No live internet connection is required.
