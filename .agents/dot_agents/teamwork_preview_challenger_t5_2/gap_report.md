# Gap Report: Adversarial Coverage Hardening

This report details untested execution paths, boundary conditions, edge cases, and potential bugs in the `scripts/tjrj_scraper_auto.py` and `scripts/process_and_timeline.py` scripts, along with recommendations and concrete designs for adversarial test cases to cover them.

---

## Summary of Identified Gaps

| ID | Component | Severity | Description |
|---|---|---|---|
| **GAP-01** | Scraper / Processor | **Critical** | Filename truncation truncates `.txt` extension, causing the processor to silently skip documents. |
| **GAP-02** | Processor | **High** | Heuristic judge extraction regex fails on uppercase names, extracting only a single letter. |
| **GAP-03** | Processor | **High** | LLM judge extraction regex matches only `"Dr"` or `"Dra"` if a dot and space follow. |
| **GAP-04** | Processor | **High** | Direct LLM API calls lack error handling/fallback, causing total crashes if the API is down. |
| **GAP-05** | Scraper | **Medium** | Short court documents (<= 50 characters) are ignored and not scraped. |
| **GAP-06** | Scraper | **Medium** | Consecutive documents with identical content are skipped as duplicates, wasting 15 seconds. |
| **GAP-07** | Processor | **Medium** | Non-UTF-8 files (CP1252/ISO-8859-1) are read with `errors='ignore'`, causing text corruption and broken regexes. |
| **GAP-08** | Scraper | **Medium** | Playwright fallback to Lucas Freitas files in demo mode is completely untested. |
| **GAP-09** | Scraper | **Medium** | Playwright search form submission failure handling is untested. |
| **GAP-10** | Scraper | **Low** | HTTP errors other than 403/500 and network timeouts (`URLError`) in Datajud query are untested. |
| **GAP-11** | Processor | **Low** | API token waste: calling DeepSeek API with empty text content when no documents exist. |

---

## Detailed Gap Analysis & Test Designs

### GAP-01: Filename Truncation Truncates Extensions (Critical)
* **Untested Path / Condition Details**: Scraping documents with long movement titles (e.g., > 110 characters) when saving to disk.
* **The Risk / Potential Bug**: In `tjrj_scraper_auto.py`, `_sanitize` truncates filenames to 120 characters:
  ```python
  def _sanitize(name: str) -> str:
      return re.sub(r'[<>:"/\\|?*\n\r]', '_', name).strip()[:120]
  ```
  If `f"{date_str}_{tipo}.txt"` exceeds 120 characters, the truncation cuts off the `.txt` extension (e.g., saving as `..._001.t` or `..._001`). In `process_and_timeline.py`, files are filtered by extension (`.txt`, `.pdf`, `.html`). Because the extension is truncated, the file is silently skipped, resulting in missing critical documents in the timeline.
* **Adversarial Test Case Design**:
  - **Inputs**: A document with type `tipo` = `"Decisao_de_pronuncia_e_desclassificacao_para_outro_crime_de_competencia_de_outro_juizo_competente_e_remessa_de_autos_de_processo_criminal_longo"` (136 characters).
  - **Mocks Needed**: Mock Playwright to return this long document type.
  - **Expected Outcome**: Assert that the scraper writes a file, check its extension (it will be truncated). Assert that `generate_timeline_and_summary` runs on this directory and fails to ingest the document.
  - **Mitigation**: Modify `_sanitize` to truncate the base name and append the extension separately.

---

### GAP-02: Heuristic Judge Regex Fails on Uppercase Names (High)
* **Untested Path / Condition Details**: Extracting the judge's name in heuristic (offline/no-API-key) mode when the name is written in ALL CAPS.
* **The Risk / Potential Bug**: The heuristic judge extraction regex is:
  ```python
  match = re.search(rf"{indicator}\s*(?:[Dd]r\(a\)\.?)?\s*([A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇÃÕ][a-záéíóúâêîôûàèìòùçãõ\s]+)", text_content)
  ```
  The character class for the rest of the name only allows lowercase letters and spaces (`[a-z... \s]+`). If a judge's name is in ALL CAPS (e.g., `"Juiz de Direito DR. CARLOS SILVA"`), the regex matches the first capital letter `"C"` and stops because `"A"` is uppercase. As a result, the extracted judge name is just `"C"` instead of `"Carlos Silva"`.
* **Adversarial Test Case Design**:
  - **Inputs**: Text document containing `"Juiz de Direito DR. MARCOS SILVA proferiu a sentença."`
  - **Mocks Needed**: None (disable DeepSeek API key to trigger heuristic mode).
  - **Expected Outcome**: Assert that `result["judge"]` is `"MARCOS SILVA"` (under current regex it will output `"M"`).
  - **Mitigation**: Update the regex to allow uppercase characters in the name body, or convert text to title case before matching.

---

### GAP-03: LLM Judge Extraction Regex Matches Only "Dr" / "Dra" (High)
* **Untested Path / Condition Details**: Extracting the judge's name from the LLM output when it starts with `"Dr."` or `"Dra."` followed by a space.
* **The Risk / Potential Bug**: The LLM judge extraction regex is:
  ```python
  j_match = re.search(r'(?:Magistrado|Juiz):\s*([^.\n]*(?:\.[^.\n]+)*?)(?:\.\s|\n|$)', content, re.IGNORECASE)
  ```
  The inner group `([^.\n]*(?:\.[^.\n]+)*?)` is lazy (`*?`). The boundary pattern includes `(?:\.\s|\n|$)`. In the name `"Dr. Ronaldo"`, the dot is followed by a space (`. `), which matches `\.\s`. Since the group is lazy, it matches 0 repetitions of `(?:\.[^.\n]+)`, capturing only `"Dr"`. The boundary matches `. `, and `"Ronaldo"` is ignored.
* **Adversarial Test Case Design**:
  - **Inputs**: LLM output string `"O processo foi conduzido pelo Magistrado: Dr. Ronaldo."`
  - **Mocks Needed**: Mock OpenAI client response to return this string.
  - **Expected Outcome**: Assert that `result["judge"]` is `"Dr. Ronaldo"` (under current regex, it will output `"Dr"`).
  - **Mitigation**: Avoid lazy quantifiers that terminate at common abbreviations like `Dr.` or make the abbreviation explicitly handled.

---

### GAP-04: LLM API Failure/Timeout Handling (High)
* **Untested Path / Condition Details**: Running timeline analysis when `DEEPSEEK_API_KEY` is present but the API is unreachable, times out, or returns an error.
* **The Risk / Potential Bug**: In `process_and_timeline.py`, there is no `try...except` block wrapping the OpenAI client initialization or the `create` call. If the API is offline or the key is invalid, the script will crash completely, blocking timeline generation.
* **Adversarial Test Case Design**:
  - **Inputs**: Standard case document.
  - **Mocks Needed**: Mock `openai.OpenAI`'s `chat.completions.create` to raise `openai.APIConnectionError` or `AuthenticationError`.
  - **Expected Outcome**: Verify that the function catches the exception, logs a warning, and falls back to heuristic analysis instead of crashing.
  - **Mitigation**: Wrap the API call in a `try...except Exception:` block and log the failure, then proceed to the heuristic fallback code.

---

### GAP-05: Short Court Document Loss (Medium)
* **Untested Path / Condition Details**: Scraping process documents with very short descriptions or texts (e.g. <= 50 characters).
* **The Risk / Potential Bug**: In `tjrj_scraper_auto.py`, the modal content extractor has hardcoded size constraints:
  ```python
  if txt and len(txt) > 50 and txt != old_content:
      ...
      if len(txt) > 30:
  ```
  If a court decision or dispatch is very short (e.g. `"Indefiro a liminar."` - 19 characters, or `"Homologo a desistência."` - 23 characters), the scraper completely ignores and skips it. This leads to missing events in the timeline.
* **Adversarial Test Case Design**:
  - **Inputs**: Process with a modal document containing `"Sentença homologada pelo juízo."` (31 characters).
  - **Mocks Needed**: Mock Playwright to return this content when modal text is requested.
  - **Expected Outcome**: Verify if the scraper saves the document. (Currently it will ignore it).

---

### GAP-06: Consecutive Identical Document Skip (Medium)
* **Untested Path / Condition Details**: Scraping a process that contains consecutive documents with identical text content (e.g. duplicate system dispatches, standard templates, or notifications).
* **The Risk / Potential Bug**: The scraper skips text matching `old_content`:
  ```python
  if txt and len(txt) > 50 and txt != old_content:
  ```
  If document 2 has the exact same content as document 1, `txt != old_content` evaluates to False. The scraper will loop 15 times (wasting 15 seconds) and then fail to save the second document.
* **Adversarial Test Case Design**:
  - **Inputs**: A process with two consecutive document buttons having the same modal body text.
  - **Mocks Needed**: Mock Playwright to return the same text for two consecutive modal iterations.
  - **Expected Outcome**: Verify that both files are written to disk and no 15-second timeout is incurred for the second document.

---

### GAP-07: Non-UTF-8 Encoding Corruption (Medium)
* **Untested Path / Condition Details**: Processing documents encoded in Windows-1252 or ISO-8859-1 (very common in Brazilian court exports).
* **The Risk / Potential Bug**: The processor opens text/HTML files using:
  ```python
  with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
  ```
  Reading a Windows-1252 file as UTF-8 with `errors='ignore'` silently drops accented characters (e.g. `"Juíza"` becomes `"Juza"`, `"decisão"` becomes `"deciso"`). This corrupts the text, which degrades LLM prompts and breaks regex-based heuristic checks.
* **Adversarial Test Case Design**:
  - **Inputs**: A document file encoded in Windows-1252 containing `"Juíza de Direito Dra. Cláudia"`.
  - **Mocks Needed**: None (create file in Windows-1252 encoding).
  - **Expected Outcome**: Verify if the parsed text is correct and if the judge name `"Cláudia"` is correctly matched. (Currently, it will read `"Juza de Direito Dra. Cludia"`, failing the regex match).
  - **Mitigation**: Use a charset detection library (like `chardet` or `charset_normalizer`) or fallback to `latin-1` if UTF-8 decoding fails.

---

### GAP-08: Playwright Fallback to Lucas Freitas Files in Demo Mode (Medium)
* **Untested Path / Condition Details**: Triggering the fallback copier when requesting Lucas Freitas's CNJ number (`0011857-95.2024.8.19.0002` or `00118579520248190002`) under `DEMO_MODE=True`.
* **The Risk / Potential Bug**: The code tries to resolve `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo` relative to the script location:
  ```python
  base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
  ```
  If this directory does not exist or has permission/access issues, it falls back to `DEFAULT_LUCAS_MOCK_DIR`. If that also fails, it returns an empty list. Since this path is completely untested, issues like missing folders, file access errors, or incorrect path resolution are not covered.
* **Adversarial Test Case Design**:
  - **Inputs**: Process number `"0011857-95.2024.8.19.0002"`, environment `DEMO_MODE="True"`.
  - **Mocks Needed**: Mock the file system (`os.path.exists`, `os.listdir`, `shutil.copy2`) to simulate:
    - Target directory exists and has files.
    - Target directory does not exist.
  - **Expected Outcome**: Verify that it copies files correctly when they exist, and handles missing directories without throwing unhandled exceptions.

---

### GAP-09: Playwright Search Form Submission Failure (Medium)
* **Untested Path / Condition Details**: Scraping via Playwright when all form inputs are missing, or when form submission via JavaScript evaluate fails.
* **The Risk / Potential Bug**: In `run_playwright_scraping`:
  ```python
  if not clicked:
      try:
          frame.evaluate("document.querySelector('form').submit()")
      except Exception:
          raise RuntimeError("Não foi possível submeter a pesquisa.")
  ```
  If this error is raised, it is caught in the outer `scrape_process_documents` loop and silently ignored. We must ensure this error is correctly propagated or logged, and tested.
* **Adversarial Test Case Design**:
  - **Inputs**: Any process number.
  - **Mocks Needed**: Mock Playwright `frame.query_selector` to return `None` for all elements and mock `frame.evaluate` to raise an exception.
  - **Expected Outcome**: Assert that `run_playwright_scraping` raises `RuntimeError("Não foi possível submeter a pesquisa.")`.

---

### GAP-10: Datajud Non-403/500 HTTP Errors & URLError (Low)
* **Untested Path / Condition Details**: Querying Datajud when the service is completely offline (DNS resolution fails, `URLError` raised) or when the server returns status codes like 502/503.
* **The Risk / Potential Bug**: The scraper only has explicit error handling for HTTP 403/500 codes:
  ```python
  except urllib.error.HTTPError as e:
      if e.code in (403, 500) and not demo_mode:
          return []
  ```
  If a different status code (like 503 Service Unavailable) or `URLError` (network down) occurs, the scraper catches it in `except Exception:` and continues to Playwright scraping. If the network is down, Playwright will also fail, wasting a large amount of time (timeouts) unnecessarily.
* **Adversarial Test Case Design**:
  - **Inputs**: Valid CNJ.
  - **Mocks Needed**: Mock `urllib.request.urlopen` to raise `urllib.error.URLError("Connection refused")`.
  - **Expected Outcome**: Verify that the scraper handles the network failure quickly without crashing.

---

### GAP-11: DeepSeek API Token Waste on Empty Content (Low)
* **Untested Path / Condition Details**: Running timeline analysis on an empty directory or directory with only unreadable/empty files when `DEEPSEEK_API_KEY` is set.
* **The Risk / Potential Bug**: The script computes `text_content` from all files. If `text_content` is empty (`""`), it still creates the OpenAI client and sends the request `"Gere o resumo dos fatos e linha do tempo:\n"` to DeepSeek. This is a waste of API tokens and returns useless LLM output.
* **Adversarial Test Case Design**:
  - **Inputs**: Empty folder path.
  - **Mocks Needed**: Mock OpenAI client.
  - **Expected Outcome**: Verify that `generate_timeline_and_summary` detects empty content and returns early (or uses heuristic fallback) instead of calling the API.
