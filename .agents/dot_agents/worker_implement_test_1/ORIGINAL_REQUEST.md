## 2026-07-03T19:14:37Z
You are teamwork_preview_worker.
Your working directory is: c:\Projetos\Super Analista Jurídico\.agents\worker_implement_test_1\
Please create this directory and write your briefing.md / progress.md.

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A Forensic Auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

Tasks:
1. Read c:\Projetos\Super Analista Jurídico\.agents\explorer_design_test_1\handoff.md.
2. Create the file `TEST_INFRA.md` at the project root (`c:\Projetos\Super Analista Jurídico\TEST_INFRA.md`) based on the 4-tier test case design described in the handoff.
3. Implement the E2E test suite in `tests/test_e2e_scraping_analysis.py` containing 30 test cases:
   - Tier 1: Feature Coverage (>=5 tests for Scraping, >=5 tests for Analysis)
   - Tier 2: Boundary & Corner Cases (>=5 tests for Scraping, >=5 tests for Analysis)
   - Tier 3: Cross-Feature Combinations (>=5 combo tests)
   - Tier 4: Real-World Application Scenarios (>=5 application-level tests)
   
   To ensure that the test suite runs and can be verified immediately (even before the implementation track writes the actual code in scripts/tjrj_scraper_auto.py and scripts/process_and_timeline.py):
   - Import the contract functions (`scrape_process_documents` and `generate_timeline_and_summary`) from their respective modules.
   - Use `try/except ImportError` blocks so that if the modules or functions do not exist, the test suite falls back to a clean mock/stub implementation defined inside the test file itself (which emulates the expected contract behaviour using local files, simulated inputs/outputs, and mock APIs).
   - Ensure the tests use Python's built-in `unittest` module or `pytest` (standard unittest is preferred as it is dependency-free).
   - Use `unittest.mock` to mock external API requests (e.g. urllib requests to Datajud, openai client calls to DeepSeek) and browser-based Playwright scraping routines.
4. Verify that the tests run successfully by executing the test command (e.g. `python -m unittest tests/test_e2e_scraping_analysis.py`).
5. Write your handoff report (c:\Projetos\Super Analista Jurídico\.agents\worker_implement_test_1\handoff.md) showing the execution command and passing test output, and send a message when done.
