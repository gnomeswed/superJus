# Challenge Report: TJRJ Scraper Automation Verification

## Challenge Summary

**Overall risk assessment**: MEDIUM

Our empirical review and static analysis of the automated scraper (`scripts/tjrj_scraper_auto.py`) and its test suite (`tests/test_e2e_scraping_analysis.py`) indicate that the code is generally robust and handles the tested error cases correctly. However, we have identified minor edge-case vulnerabilities related to inputs with whitespace, potential Windows path length limit failures, and an inconsistent HTTP error propagation behavior that aborts scraping entirely rather than falling back to browser-based automation.

---

## Challenges

### [Medium] Challenge 1: Datajud API HTTP 403/500 Errors Preempt Fallback
- **Assumption challenged**: That a Datajud API HTTP 403 or 500 error represents a terminal condition that should return an empty list immediately.
- **Attack scenario**: If the Datajud public API has a temporary outage (returning a 500 Internal Server Error) or access limit (returning a 403 Forbidden), the scraper returns `[]` immediately. It does not attempt to fall back to the Playwright scraper, even though the web portal at `https://www3.tjrj.jus.br/consultaprocessual/` might be fully operational and accessible.
- **Blast radius**: Complete scraping failure on temporary or local API outages, rendering the Playwright scraper fallback useless.
- **Mitigation**: Log the Datajud HTTP error and proceed to the Playwright scraping phase instead of returning `[]` immediately.

### [Low] Challenge 2: Whitespace in Formatted CNJ Inputs Causes Validation Failures
- **Assumption challenged**: That valid CNJ numbers will not contain leading or trailing whitespaces when passed to the function.
- **Attack scenario**: The user copy-pastes a CNJ number containing leading/trailing whitespace (e.g. `" 0029845-67.2026.8.19.0000 "`). `clean_process_number` strips symbols and whitespaces, generating a 20-character clean number. However, the structure regex `re.match(r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$', process_number)` runs on the original string, causing it to fail and throw `ValueError("Invalid CNJ format structure.")`.
- **Blast radius**: False-positive validation failure on copy-pasted strings with spaces.
- **Mitigation**: Perform a `.strip()` on the `process_number` parameter prior to validation checks.

### [Low] Challenge 3: Windows MAX_PATH Length Limit Under Nested Directory Structures
- **Assumption challenged**: That checking write access on the base directory (`save_dir`) guarantees that all subsequent file creation operations will succeed.
- **Attack scenario**: When run on Windows, if the `save_dir` is nested deep in the filesystem and a document has a long type/title, the concatenated file path `fpath` (comprising `save_dir` and the sanitized `120`-character file name) can easily exceed the Windows path length limit of 260 characters, raising an unhandled `FileNotFoundError` or `OSError`.
- **Blast radius**: Partial scraping failure where some files are saved successfully while others crash the scraper or fail silently inside the document loop.
- **Mitigation**: Truncate sanitized file names to a shorter length (e.g., 60-80 chars) or use Windows UNC path prefixes (`\\?\`).

---

## Stress Test Results

| Scenario | Expected Behavior | Actual/Predicted Behavior | Pass/Fail |
|---|---|---|---|
| **Invalid CNJ (Letters)** | Raise `ValueError` | Raises `ValueError` | **PASS** |
| **Invalid CNJ (Too Short)** | Raise `ValueError` | Raises `ValueError` | **PASS** |
| **Invalid CNJ (Too Long)** | Raise `ValueError` | Raises `ValueError` | **PASS** |
| **Invalid CNJ (Wrong Format Structure)** | Raise `ValueError` | Raises `ValueError` | **PASS** |
| **Read-Only Directory** | Raise `PermissionError` | Raises `PermissionError` | **PASS** |
| **Datajud HTTP 403/500 Error** | Gracefully caught and returns `[]` | Caught and returns `[]` (preempts Playwright fallback) | **PASS** (Matches tests, design flaw) |
| **Playwright Timeout** | Caught, returns `[]` (doesn't crash) | Caught, returns `[]` without crashing | **PASS** |
| **Run test suite (`unittest`)** | All scraping tests pass | All scraping tests verify correctly and pass | **PASS** |

---

## Unchallenged Areas

- **Production Captcha/Anti-Bot Mechanisms** — Not tested under real production load because the test suite relies on mock environments and local mock web elements. We assume that actual production run bypasses captcha or relies on the Datajud API.
- **Playwright Thread-Safety** — Concurrency behavior under multiple threads was not challenged in-depth.
