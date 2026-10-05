# Gap Report — Adversarial Coverage Hardening (Tier 5)

This report details untested execution paths, edge cases, boundary conditions, and potential bugs identified in `scripts/tjrj_scraper_auto.py` and `scripts/process_and_timeline.py`.

---

## Identified Gaps and Adversarial Test Designs

### Gap 1: Short Document Content Triggers 15-Second Timeout and Failure to Save

- **Untested Path / Condition**:
  In `scripts/tjrj_scraper_auto.py`, inside the Playwright document extraction loop (lines 291–314):
  ```python
  if txt and len(txt) > 50 and txt != old_content:
  ```
  If a document is valid but short (e.g., a simple dispatch or ruling like `"Indefiro o pedido."` containing $\le 50$ characters), the condition `len(txt) > 50` evaluates to `False`. The loop does not break, waiting for all 15 retries (sleeping 1 second per iteration, totaling 15 seconds), and the content is never saved because `content` remains `None`.
- **Risk**: 
  - **Performance Degradation**: Wastes 15 seconds per short document.
  - **Data Loss**: Valid court documents with short texts are entirely discarded and never saved.
- **Adversarial Test Case Design**:
  - **Inputs**: CNJ process number and a save directory.
  - **Mocks Needed**: Mock Playwright's `frame.evaluate` for the modal body text to return a string of length $\le 50$ (e.g., `"Despacho: Cumpra-se."` — 20 characters).
  - **Expected Outcome**: The test asserts that the document is successfully written to a file and that the function executes without a 15-second hang.

---

### Gap 2: Uppercase Judge Names Truncated or Missed by Heuristic Extraction

- **Untested Path / Condition**:
  In `scripts/process_and_timeline.py` (line 144), the regex used to extract the judge's name is:
  ```python
  rf"{indicator}\s*(?:[Dd]r\(a\)\.?)?\s*([A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇÃÕ][a-záéíóúâêîôûàèìòùçãõ\s]+)"
  ```
  This pattern expects a single uppercase letter followed exclusively by lowercase letters and spaces.
  - If a judge name is in all-uppercase (e.g., `"Juiz de Direito Dr. MARCOS SILVA"`), the match fails because uppercase letters (except the first character) are not matched.
  - If a judge name has standard uppercase initials (e.g., `"Juiz de Direito Dr. Marcos Silva"`), the regex matches `"Marcos "`, but stops immediately at the uppercase `"S"`, truncating the extracted name to `"Marcos"`.
- **Risk**: 
  - **Incomplete/Incorrect Extraction**: Judge names in reports are either truncated or completely missed (defaulting to `"Juiz Heurístico"`). All-caps is extremely common in Brazilian legal documents.
- **Adversarial Test Case Design**:
  - **Inputs**: A text file containing `"Juiz de Direito Dr. MARCOS SILVA"` and another containing `"Magistrado Dr. Marcos Silva"`.
  - **Mocks**: None required (pure unit test of heuristic extraction).
  - **Expected Outcome**: The extracted judge name in the result must be exactly `"MARCOS SILVA"` and `"Marcos Silva"`, respectively.

---

### Gap 3: Non-existent Input Directory/File evaluated as Empty Ingestion without Error

- **Untested Path / Condition**:
  In `scripts/process_and_timeline.py` (lines 21–30), if the input `doc_path` does not exist on disk, both `os.path.isdir(doc_path)` and `os.path.isfile(doc_path)` evaluate to `False`. The file list `docs` remains empty, no files are processed, and the function silently continues, creating a timeline report with a mock fallback entry:
  ```json
  {"date": "sem_data", "event": "Ingestão", "description": "Documento importado."}
  ```
- **Risk**: 
  - **Silent Failure**: The user/system is led to believe that the document was successfully processed but contained no dates, when in reality the input file path was invalid or missing.
- **Adversarial Test Case Design**:
  - **Inputs**: A non-existent path (e.g. `"non_existent_file_path.txt"`).
  - **Mocks**: None.
  - **Expected Outcome**: The function should raise a `FileNotFoundError` rather than silently returning a mock report indicating a successful "Ingestão".

---

### Gap 4: Silent Unicode Corruption on Latin-1/CP1252 Encoded Files

- **Untested Path / Condition**:
  In `scripts/process_and_timeline.py` (lines 53 and 63), HTML and TXT files are opened using:
  ```python
  with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
  ```
  If the source files are encoded in Latin-1 or CP1252 (very common in older Brazilian Windows environments and court exports), non-UTF-8 characters (e.g., `ã`, `ç`, `í`) will be silently dropped.
- **Risk**: 
  - **Text Corruption**: Dropped characters corrupt word matches. For example, `"decisão"` becomes `"deciso"`, and `"Estevão"` becomes `"Estevo"`, which can break subsequent regex pattern matches or LLM context.
- **Adversarial Test Case Design**:
  - **Inputs**: A text file containing `"Juiz de Direito Dr. Estevão"` encoded in Latin-1 (`iso-8859-1`).
  - **Mocks**: None.
  - **Expected Outcome**: The file must be read without losing accented characters, and the judge's name must be successfully extracted as `"Estevão"`.

---

### Gap 5: Single Page Exception Skips Entire PDF Document

- **Untested Path / Condition**:
  In `scripts/process_and_timeline.py` (lines 36–50), the PDF text reader loops over all pages. If a single page raises an exception during `extract_text()`, the `try-except` block wrapping the entire PDF logic catches it and runs `continue` for the whole file.
- **Risk**:
  - **Fragility / Data Loss**: A minor parsing error or corrupt image on a single page of a large PDF causes the entire document's content to be skipped, losing all text from the remaining healthy pages.
- **Adversarial Test Case Design**:
  - **Inputs**: A multi-page PDF where page 1 is valid and page 2 raises an exception during text extraction.
  - **Mocks**: Mock `pypdf.PdfReader` to return a list of page mocks where page 2's `extract_text` method raises an `Exception`.
  - **Expected Outcome**: The text content of page 1 should be successfully preserved and included in the output summary, while logging the page 2 error.

---

### Gap 6: Boolean Case Sensitivity and Strict Format in `DEMO_MODE` Environment Variable

- **Untested Path / Condition**:
  In `scripts/tjrj_scraper_auto.py` (lines 404–408), the check for `DEMO_MODE` is case-sensitive and strictly expects the string `"True"`:
  ```python
  demo_env = os.environ.get("DEMO_MODE")
  if demo_env is not None:
      demo_mode = demo_env == "True"
  ```
  If `DEMO_MODE` is set to `"true"` (lowercase), `"1"`, or `"yes"`, `demo_mode` evaluates to `False`.
- **Risk**: 
  - **Unintended Execution**: Deployments setting standard lowercase boolean values (e.g. `DEMO_MODE=true` in docker-compose) will bypass the demo mode check and attempt real scraping, leading to scraping failures, rate limiting, or long delays.
- **Adversarial Test Case Design**:
  - **Inputs**: Environment variable `DEMO_MODE` set to `"true"` or `"1"`.
  - **Mocks**: Mock Playwright to ensure it is not invoked.
  - **Expected Outcome**: The scraper should activate demo fallback behavior (generating mock files) rather than trying to launch Playwright.

---

### Gap 7: Swallowed Exceptions in Datajud API Calls

- **Untested Path / Condition**:
  In `scripts/tjrj_scraper_auto.py` (lines 431–441), general exceptions thrown during the Datajud API query are caught and silently ignored:
  ```python
  except Exception:
      pass
  ```
- **Risk**: 
  - **Harder Debugging**: If there is an authentication key rotation issue, SSL certificate failure, or protocol change, developers and operators will receive no logs or indications of why the API failed.
- **Adversarial Test Case Design**:
  - **Inputs**: CNJ process number and a save directory.
  - **Mocks**: Mock `urllib.request.urlopen` to raise an connection error or JSON decode error.
  - **Expected Outcome**: The test verifies that the error is logged (e.g., using `unittest.TestCase.assertLogs`) rather than completely silenced.

---

### Gap 8: Data Overwrite in `extracted_playwright.txt` for Multi-Document Scraping

- **Untested Path / Condition**:
  In `scripts/tjrj_scraper_auto.py` (lines 327–330), when a document is scraped, its content is written to a unique filename and also written to `extracted_playwright.txt` with write mode `"w"`.
- **Risk**: 
  - **Information Loss**: If a process has multiple documents, each successive write to `extracted_playwright.txt` overwrites the previous ones. The final file will only contain the text of the very last document.
- **Adversarial Test Case Design**:
  - **Inputs**: A process number with multiple document buttons in the mock page.
  - **Mocks**: Mock Playwright to return 3 separate documents.
  - **Expected Outcome**: Assert that `extracted_playwright.txt` either accumulates all documents or that each document is stored separately without overwriting.
