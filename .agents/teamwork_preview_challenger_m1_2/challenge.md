# Scraper Verification Findings & Adversarial Review

## Challenge Summary

**Overall risk assessment**: MEDIUM

- **Correctness & CNJ Validation**: There is a validation bypass vulnerability in the CNJ format checking. CNJ numbers that contain letters but lack separators (e.g. `00298456720268190000a`) will successfully pass the cleaning and validation steps without raising `ValueError`.
- **Read-Only Directories**: Exception handling for read-only directories is robust. The combination of `os.access` checks and try-except blocks wrapping `os.makedirs` successfully raises `PermissionError` in all target conditions.
- **Network & Playwright Errors**: HTTP errors (such as 403 or 500) and Playwright timeout conditions are caught and handled. General `except Exception` blocks prevent the scraper from crashing, though they may mask structural changes on the TJRJ website.
- **Test Suite**: The test suite in `tests/test_e2e_scraping_analysis.py` passes all scraping-related tests under simulated/mocked environments, but lacks coverage for the specific validation leak identified.

---

## Challenges

### [Medium] Challenge 1: CNJ Format Validation Leak

- **Assumption challenged**: The scraper assumes that all invalid CNJ numbers (including those containing letters, wrong formats, or incorrect lengths) will raise a `ValueError`.
- **Attack scenario**:
  - The function `clean_process_number` removes all non-numeric characters from the input.
  - If a user inputs `"00298456720268190000a"` (20 digits + 1 letter, no separators), the clean number becomes `"00298456720268190000"`, which has a length of 20.
  - The check `len(clean_num) != 20` passes (since `20 != 20` is False).
  - The check `if '-' in process_number or '.' in process_number:` is bypassed because the input contains no dashes or dots.
  - Thus, no `ValueError` is raised, and the scraper proceeds with the invalid process number.
- **Blast radius**: The scraper will execute unnecessary external API and headless browser routines with invalid parameters, wasting network bandwidth, browser cycles, and API quotas, potentially returning empty lists or failing downstream in unexpected ways.
- **Mitigation**:
  Refactor the validation logic in `scrape_process_documents` to validate the original string format before cleaning it, or assert that the original string is either a pure 20-digit string or conforms to the CNJ mask.
  ```python
  # Suggested replacement validation:
  if not re.match(r'^\d{20}$', process_number) and not re.match(r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$', process_number):
      raise ValueError("Invalid CNJ format. Must contain exactly 20 digits or follow standard masked format.")
  ```

---

### [Low] Challenge 2: Broad Exception Catching in Playwright Scraping

- **Assumption challenged**: Broad `except Exception:` handling is sufficient for Playwright errors.
- **Attack scenario**:
  - If the TJRJ web page layout changes (e.g. selectors `iframe#mainframe` or `app-movimento` are renamed), the scraping fails silently because all errors are swallowed in `except Exception: pass`.
- **Blast radius**: Silent failures. The tool returns an empty file list, and developers or calling systems cannot distinguish between a process having no documents and a broken scraper due to UI layout changes.
- **Mitigation**:
  Introduce specific logging or raise detailed exceptions for structural scraper failures (e.g. iframe not found) while keeping network timeouts graceful.

---

## Stress Test Results

| Scenario / Input | Expected Behavior | Actual Behavior | Pass/Fail |
|---|---|---|---|
| `"123"` (Too short) | Raise `ValueError` | Raises `ValueError` | **Pass** |
| `"123456789012345678901"` (Too long) | Raise `ValueError` | Raises `ValueError` | **Pass** |
| `"0029845-67.2026.8.19.000a"` (Letters + separators) | Raise `ValueError` | Raises `ValueError` | **Pass** |
| `"00298456720268190000a"` (Letters, no separators, 20 digits) | Raise `ValueError` | Bypasses checks without raising error | **Fail** |
| Read-only directory | Raise `PermissionError` | Raises `PermissionError` | **Pass** |
| HTTP 403 / 500 on Datajud | Caught and returns `[]` | Caught and returns `[]` | **Pass** |
| Playwright Timeout | Caught and handled gracefully | Caught and returns list (or empty list) | **Pass** |

---

## Unchallenged Areas

- **Real-World TJRJ Captcha / Cloudflare Block**: Scraper performance when TJRJ implements Cloudflare challenge pages or captchas was not stress-tested because we are in CODE_ONLY mode and no live internet access is permitted.
- **Concurrency & File Locks**: Writing to the same directory concurrently by multiple scraper instances was not fully stress-tested, though tests suggest isolation is maintained if distinct output directories are used.
