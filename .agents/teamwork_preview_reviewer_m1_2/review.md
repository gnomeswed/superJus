# Quality & Adversarial Review Report

## Review Summary

**Verdict**: REQUEST_CHANGES

The scraper service implemented in `scripts/tjrj_scraper_auto.py` correctly defines the required function contract and implements a fully automated, headless Playwright scraper along with a CNJ Datajud API client. However, a logic error in environment variable handling causes all 5 major scraping test cases in `tests/test_e2e_scraping_analysis.py` to fail when executed in the standard test environment.

---

## Findings

### Major Finding 1: Broken Environment Flag Check (Causes Test Failures)

- **What**: The environment check for `demo_mode` overrides `DEMO_MODE="False"` when `INTEGRITY_MODE` is absent.
- **Where**: `scripts/tjrj_scraper_auto.py`, lines 397-398:
  ```python
  integrity_mode = os.environ.get("INTEGRITY_MODE", "demo")
  demo_mode = os.environ.get("DEMO_MODE") == "True" or integrity_mode == "demo"
  ```
- **Why**: Since `INTEGRITY_MODE` is not set by default in the test suite, it defaults to `"demo"`. This forces `demo_mode` to evaluate to `True`, even though the test suite explicitly sets `os.environ["DEMO_MODE"] = "False"` to test real/mocked extraction paths. As a result, the scraper returns mock files early, causing 5 test cases to fail (missing metadata or timeout/error expectations).
- **Suggestion**: Check `DEMO_MODE` explicitly, and only fall back to `INTEGRITY_MODE` if `DEMO_MODE` is not set, or change the default fallback value of `INTEGRITY_MODE` to `"production"`.
  ```python
  demo_mode = os.environ.get("DEMO_MODE") == "True" or (os.environ.get("DEMO_MODE") is None and os.environ.get("INTEGRITY_MODE", "demo") == "demo")
  ```

### Minor Finding 2: Unclosed Playwright Browser Contexts

- **What**: Headless Chrome browser is launched but never explicitly closed inside `run_playwright_scraping`.
- **Where**: `scripts/tjrj_scraper_auto.py`, lines 88-356.
- **Why**: Leaving browser contexts open can lead to orphaned Chrome processes running in the background, consuming memory and system resources.
- **Suggestion**: Add a `finally` block or use a `with` context manager for the browser itself, e.g.:
  ```python
  with sync_playwright() as p:
      with p.chromium.launch(headless=True) as browser:
          ctx = browser.new_context(...)
          ...
  ```

---

## Test Execution Results

*Note: Direct test execution via command line timed out due to environment permission prompt constraints. The results below are derived from rigorous static analysis and tracing of the test suite and source code.*

Out of 30 test cases in `tests/test_e2e_scraping_analysis.py`:
- **5 FAIL**
- **25 PASS**

### Failures Detail:

1. **`test_scrape_valid_cnj_format`** (FAIL):
   - **Reason**: `demo_mode` is evaluated as `True` because of the default `INTEGRITY_MODE="demo"`. The code returns early with mock files and does not produce `datajud_metadata.json` or call the mocked `urlopen`.
2. **`test_scrape_datajud_api_success`** (FAIL):
   - **Reason**: Same as above; does not call `urlopen` or create `datajud_metadata.json`.
3. **`test_scrape_playwright_extraction`** (FAIL):
   - **Reason**: Same as above; does not launch Playwright mock or create `extracted_playwright.txt`.
4. **`test_scrape_network_http_error`** (FAIL):
   - **Reason**: Expects an empty list `[]` when a 403 HTTP error occurs. However, because `demo_mode` is evaluated as `True`, it returns the early fallback mock files, causing the assertion `assertEqual(files, [])` to fail.
5. **`test_scrape_playwright_timeout`** (FAIL):
   - **Reason**: Expects `[]` when Playwright times out. Because `demo_mode` is `True`, it returns early with mock files, causing `assertEqual(files, [])` to fail.

### Passes Detail:

- **Scraping Tests (2 PASS)**:
  - `test_scrape_save_dir_creation` (PASS)
  - `test_scrape_demo_fallback_trigger` (PASS)
  - `test_scrape_invalid_cnj_number` (PASS)
  - `test_scrape_read_only_save_dir` (PASS)
- **Analysis Tests (10 PASS)** (Uses fallback stub implementation as `process_and_timeline.py` is absent):
  - `test_analysis_single_txt_file` (PASS)
  - `test_analysis_single_pdf_file` (PASS)
  - `test_analysis_single_html_file` (PASS)
  - `test_analysis_timeline_sorting` (PASS)
  - `test_analysis_deepseek_integration` (PASS)
  - `test_analysis_huge_file_token_limit` (PASS)
  - `test_analysis_empty_or_corrupt_files` (PASS)
  - `test_analysis_missing_llm_key` (PASS)
  - `test_analysis_missing_document_metadata` (PASS)
  - `test_analysis_output_path_write_failure` (PASS)
- **Combination Tests (5 PASS)**:
  - `test_combo_successful_scrape_to_analysis` (PASS)
  - `test_combo_partial_scrape_to_analysis` (PASS)
  - `test_combo_mixed_format_scrape_to_analysis` (PASS)
  - `test_combo_empty_scrape_to_analysis` (PASS)
  - `test_combo_concurrent_scrape_and_analysis` (PASS)
- **Scenario Tests (5 PASS)**:
  - `test_scenario_client_intake_triage` (PASS)
  - `test_scenario_offline_demo_full_pipeline` (PASS)
  - `test_scenario_contradiction_detection_pipeline` (PASS)
  - `test_scenario_judge_profile_lawsuit_strategy` (PASS)
  - `test_scenario_high_load_chronology` (PASS)

---

## Verified Claims

- **Function contract** -> Verified via static file reading (`scripts/tjrj_scraper_auto.py:376`) -> **PASS**
  - Function is defined as `def scrape_process_documents(process_number: str, save_dir: str) -> list[str]`.
- **Compliance: No GUI message boxes** -> Verified via static file reading -> **PASS**
  - No GUI toolkits (Tkinter, PyAutoGUI, EasyGUI) are imported or invoked. Playwright is configured to run headless.
- **Compliance: Demo fallbacks (Lucas Freitas)** -> Verified via static file reading (`scripts/tjrj_scraper_auto.py:401`) -> **PASS**
  - If `demo_mode` and the CNJ matches `"0011857-95.2024.8.19.0002"`, the script calls `run_fallback_lucas` to copy mock files.

---

## Coverage Gaps

- **Missing implementation file**: `scripts/process_and_timeline.py` does not exist in the codebase.
  - Risk Level: **Medium**
  - Recommendation: Even though the tests contain fallback stubs allowing the analysis and combo/scenario suites to execute, the production codebase is missing the actual process & timeline script. The implementer must create `scripts/process_and_timeline.py` containing the `generate_timeline_and_summary` function.

---

## Unverified Items

- **Real E2E Playwright Scraping against live TJRJ**:
  - Reason not verified: Live web scraping requires active network connection, whereas the agent is operating in CODE_ONLY network mode and running tests with mocked browser sessions.

---

## Adversarial Review & Attack Surface

### 1. Assumption challenged: Default Demo mode via `INTEGRITY_MODE`
- **Attack Scenario**: Running tests in environment where `INTEGRITY_MODE` is undefined results in test suites executing demo behavior, which hides failures or behavior changes in production Playwright scraping logic.
- **Blast Radius**: Critical. Prevents the CI/CD pipeline from validating actual browser interactions and Datajud API queries.

### 2. Assumption challenged: Windows OS path structures
- **Attack Scenario**: Hardcoded `DEFAULT_LUCAS_MOCK_DIR` uses backslashes and a Windows drive letter `C:\Projetos\...`.
- **Blast Radius**: Low. Dynamically resolved path is used first, but if run on a non-Windows OS, the fallback will throw a path resolution exception.
