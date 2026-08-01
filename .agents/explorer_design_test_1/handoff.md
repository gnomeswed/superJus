# Handoff Report — E2E Test Design for Super Analista Jurídico

## 1. Observation
We have inspected the workspace, directory structures, and the codebase files. The key findings include:

1. **Project Architecture and Contracts** (`PROJECT.md`):
   - Milestone 1 is the "E2E Testing Track" (Status: `PLANNED`).
   - The Scraping Service contract is:
     ```python
     scrape_process_documents(process_number: str, save_dir: str) -> list[str]
     ```
   - The Analysis Service contract is:
     ```python
     generate_timeline_and_summary(doc_path: str, output_path: str) -> dict
     ```
   - Planned files are: `scripts/tjrj_scraper_auto.py`, `scripts/process_and_timeline.py`, and `tests/test_e2e_scraping_analysis.py`.

2. **Scraper Code** (`scripts/court_scraper.py`):
   - Uses `urllib.request.Request` and `urllib.request.urlopen` (lines 53-56) to query the Datajud public API.
   - Example request headers include `Authorization: DATAJUD_API_KEY` (lines 40-43).

3. **Playwright Extractor** (`scripts/tjrj_extractor.py`):
   - Uses `playwright.sync_api` (line 14) and opens a Chromium browser to scrape TJRJ documents.
   - Relies on frames (`page.query_selector("iframe#mainframe")` in line 96) and modals (`#descricaoDetalhadaModal` in lines 165, 205).
   - Writes extracted documents as `.txt` files in a given directory (lines 232-243).

4. **DeepSeek AI Engine** (`scripts/ai_engine.py`):
   - Initializes an OpenAI client targeting the DeepSeek API (`https://api.deepseek.com` in lines 5-9).
   - Features include Chat with Case (`chat_with_case`), Contradiction Detector (`detect_contradictions`), Legal Piece Generator (`generate_legal_piece`), and PDF Facts Extractor (`extract_pdf_facts`).

5. **Document Ingestion** (`core/document_processor.py`):
   - Parses `.pdf` files using `PyPDFLoader` (line 15), `.html` files using `BeautifulSoup` (line 10), and `.txt` files using `TextLoader` (line 19).

6. **Current Tests Directory** (`tests/`):
   - Contains only `test_search_motoboy.py`, which is an execution script and not structured as a standard `pytest` suite.

---

## 2. Logic Chain
1. Since the codebase uses external APIs (Datajud, DeepSeek) and interactive UI scraping (Playwright), running E2E tests in a strict offline `CODE_ONLY` environment and 'demo' mode requires complete mock coverage.
2. The Scraping Service depends on network calls (urllib for Datajud API) and automated UI browser interactions (Playwright). Therefore, we must design mocks that intercept `urllib.request.urlopen` and mock Playwright's Page/Frame evaluation.
3. The Analysis Service depends on the DeepSeek OpenAI client and local document parsing (PDF, HTML, TXT). Therefore, we must design tests using mock file objects (e.g. temporary directories with dummy text/PDF/HTML fixtures) and mock the OpenAI completion client responses.
4. Structuring the tests around a 4-tier methodology ensures that we cover simple happy paths (Tier 1), error and boundary conditions (Tier 2), the handoff interface between scraper and analyzer (Tier 3), and complex, real-world user scenarios (Tier 4) such as triage reports and contradiction detection.

---

## 3. Caveats
- **Offline / Network Restrictions**: Since the system operates under a CODE_ONLY network block, no real Datajud or DeepSeek endpoints can be resolved. Tests must be 100% mocked or run in offline fallback mode.
- **Playwright Environment**: Playwright requires browser binaries to run. In headless CI environments without these binaries installed, importing or launching Playwright may fail. Tests must gracefully handle `RuntimeError` or check browser availability before running browser-specific E2E tests, or mock the browser wrapper completely.
- **LLM Non-Determinism**: Real LLM responses are non-deterministic. By using mock responses, we ensure tests are stable, reproducible, and fast, but we cannot test LLM reasoning accuracy.

---

## 4. Conclusion

Below is the detailed E2E test design based on the 4-tier methodology, including runner commands and mock structures.

### 4.1 E2E Test Design (Tiers 1-4)

#### Tier 1: Feature Coverage (>=5 tests per feature)
##### Feature A: Scraping Service
1. **`test_scrape_valid_cnj_format`**: Verify that `scrape_process_documents` parses a valid CNJ process number format (e.g. `0029845-67.2026.8.19.0000`), maps to the correct tribunal endpoint, and returns a non-empty file path list.
2. **`test_scrape_datajud_api_success`**: Verify that a successful response from the Datajud API public endpoint (mocked) is correctly parsed (classe, assunto, ultimas movimentações) and stored.
3. **`test_scrape_playwright_extraction`**: Verify that the Playwright scraping routine correctly extracts text contents from raw elements (iframe, button clicks, modals) and writes files.
4. **`test_scrape_save_dir_creation`**: Verify that the service automatically creates the target `save_dir` directory structure if it does not exist and saves documents inside it.
5. **`test_scrape_demo_fallback_trigger`**: Verify that in 'demo' integrity mode, if no internet connection is available, the scraper copies a pre-defined set of local fallback mock files.

##### Feature B: Analysis Service
6. **`test_analysis_single_txt_file`**: Verify that analyzing a single `.txt` document loads its text, makes a mocked DeepSeek call, and outputs a facts summary to the target folder.
7. **`test_analysis_single_pdf_file`**: Verify that PyPDF2/PyPDFLoader correctly parses a mock PDF and outputs the structured facts list.
8. **`test_analysis_single_html_file`**: Verify that BeautifulSoup correctly strips HTML formatting and extracts text to feed into the analysis prompt.
9. **`test_analysis_timeline_sorting`**: Verify that when multiple files with different dates in the header (e.g., "10/05/2026", "02/05/2026") are parsed, the timeline is generated in strict chronological order.
10. **`test_analysis_deepseek_integration`**: Verify that the system prompt, user prompt, and parameters (temperature, max_tokens) sent to the DeepSeek client match the specified contract, and that the returned dictionary is correctly populated.

#### Tier 2: Boundary & Corner Cases (>=5 tests per feature)
##### Feature A: Scraping Service
1. **`test_scrape_invalid_cnj_number`**: Verify that a malformed process number (e.g. incorrect length, alphabetic characters) raises `ValueError` immediately.
2. **`test_scrape_datajud_empty_response`**: Verify that if Datajud returns no hits (e.g. process is in "segredo de justiça" or does not exist), the service returns an empty list gracefully.
3. **`test_scrape_network_http_error`**: Verify that HTTP error codes (e.g., 403 Forbidden, 500 Server Error) from Datajud are caught and logged, returning an empty list gracefully.
4. **`test_scrape_playwright_timeout`**: Verify that if Playwright fails to find the iframe or modal buttons (reaches timeout), it exits cleanly, returning a descriptive error message.
5. **`test_scrape_read_only_save_dir`**: Verify that if the target `save_dir` is read-only or permission-denied, the scraper raises a clean `PermissionError` or log warning.

##### Feature B: Analysis Service
6. **`test_analysis_huge_file_token_limit`**: Verify that files larger than the maximum LLM input context (e.g. >100KB) are truncated or chunked before calling the DeepSeek API to prevent API crash.
7. **`test_analysis_empty_or_corrupt_files`**: Verify that if a file is empty or corrupt (e.g. 0-byte TXT or invalid PDF bytes), the analyzer logs a warning, skips the file, and proceeds with other documents.
8. **`test_analysis_missing_llm_key`**: Verify that if `DEEPSEEK_API_KEY` is missing or invalid, the analysis falls back to a rule-based heuristics engine or returns a descriptive error message.
9. **`test_analysis_missing_document_metadata`**: Verify that files lacking clear date headers are grouped under a default fallback date (e.g., "sem_data") and sorted accordingly without throwing a `ValueError`.
10. **`test_analysis_output_path_write_failure`**: Verify that if the target `output_path` directory is unwritable or the file is locked, the function raises an explicit, handled error.

#### Tier 3: Cross-Feature Combinations (pairwise coverage of features)
1. **`test_combo_successful_scrape_to_analysis`**: Mock scrape returns files, analysis runs on those files and successfully outputs a timeline.
2. **`test_combo_partial_scrape_to_analysis`**: Scraper successfully extracts 3/5 files, analysis runs on those 3 files and outputs a timeline without failure.
3. **`test_combo_mixed_format_scrape_to_analysis`**: Scraper downloads `.txt`, `.html`, and `.pdf` files, analysis integrates them all.
4. **`test_combo_empty_scrape_to_analysis`**: Scraper downloads nothing, analysis handles empty input directory gracefully.
5. **`test_combo_concurrent_scrape_and_analysis`**: Verifies directory isolation (file locking/namespace) when running two concurrent processes.

#### Tier 4: Real-World Application Scenarios (at least 5 application-level tests)
1. **`test_scenario_client_intake_triage`**: Full client triage flow (Datajud + Playwright extract -> AI summary/timeline -> Triage Report PDF/MD generation).
2. **`test_scenario_offline_demo_full_pipeline`**: Simulates running the entire system offline under 'demo' integrity mode using mock inputs and a deterministic LLM mock.
3. **`test_scenario_contradiction_detection_pipeline`**: Verifies the system parses multiple witness statements and successfully flags inconsistencies using the contradiction detector.
4. **`test_scenario_judge_profile_lawsuit_strategy`**: Verifies magistrate extraction from decisions, profile lookup, and combined strategic defense recommendation.
5. **`test_scenario_high_load_chronology`**: Processes 30+ mock document files, verifying memory stability, execution time under budget, and correct timeline ordering.

---

### 4.2 Recommendations

#### 1. Test Runner and Execution Command
We recommend using **`pytest`** as the test runner, along with the **`pytest-mock`** extension for handling dependency injection and patching.
- **Execution Command**:
  ```powershell
  python -m pytest -v tests/test_e2e_scraping_analysis.py
  ```
- **Dependencies** (to add to development requirements):
  ```
  pytest==8.1.1
  pytest-mock==3.14.0
  ```

#### 2. Structure of Mock Inputs
To execute tests offline and protect system integrity, we must feed tests with deterministic inputs:

##### A. Datajud API Mock Response (JSON structure)
```json
{
  "hits": {
    "hits": [
      {
        "_source": {
          "numeroProcesso": "00298456720268190000",
          "classe": {"nome": "Habeas Corpus"},
          "assuntos": [{"nome": "Prisão Preventiva"}],
          "movimentos": [
            {"dataHora": "2026-07-03T12:00:00.000Z", "nome": "Decisão Proferida"},
            {"dataHora": "2026-07-01T10:00:00.000Z", "nome": "Distribuição por dependência"}
          ]
        }
      }
    ]
  }
}
```

##### B. Playwright Scraper Page Mock (Python code)
```python
class MockElement:
    def __init__(self, text="", tag=""):
        self._text = text
        self._tag = tag

    def inner_text(self):
        return self._text

    def query_selector_all(self, selector):
        return []

    def closest(self, selector):
        return self

    def query_selector(self, selector):
        return self

class MockFrame:
    def query_selector_all(self, selector):
        if "button" in selector:
            return [MockElement(text="original ver integra", tag="button")]
        return []

    def evaluate(self, script, *args):
        if "descricaoDetalhadaModal" in script:
            return "Este é um depoimento mockado do processo TJRJ contendo informações de autoria e materialidade."
        return {"date": "03/07/2026", "tipo": "Decisao"}

class MockPage:
    def goto(self, url, **kwargs):
        pass

    def query_selector(self, selector):
        if "iframe#mainframe" in selector:
            class FakeIframe:
                def content_frame(self):
                    return MockFrame()
            return FakeIframe()
        return None
```

##### C. DeepSeek API Mock Response (Python OpenAI object mock)
```python
class MockChoiceMessage:
    def __init__(self, content):
        self.content = content

class MockChoice:
    def __init__(self, content):
        self.message = MockChoiceMessage(content)

class MockCompletionsResponse:
    def __init__(self, content):
        self.choices = [MockChoice(content)]

# The mock returns this pre-formatted Markdown when prompt is matched
MOCK_ANALYSIS_MARKDOWN = """
## 1. Resumo dos Fatos
O réu foi preso em flagrante portando mercadorias sem nota fiscal.

## 2. Possível Tipificação Criminal
Art. 180, CP (Receptação).

## 3. Alertas de Nulidade
Busca pessoal realizada sem fundada suspeita.

## 4. Estratégia de Defesa
Impetração de Habeas Corpus por ilicitude de provas.
"""
```

##### D. Dummy PDF and HTML Files
- **Dummy HTML File**:
  ```html
  <html>
    <body>
      <div class="titulo-movimentacao">Tipo do Movimento: Decisao</div>
      <div id="descricaoDetalhadaModal">
        <div class="modal-body">
          Processo: 00298456720268190000. Data: 03/07/2026.
          Decisão: Indefiro a liberdade provisória com base na garantia da ordem pública.
        </div>
      </div>
    </body>
  </html>
  ```
- **Dummy PDF File** (Generated dynamically in tests using `fpdf2` or mock-injected via PyPDFLoader patch):
  - A simple 1-page PDF containing the text: "Denúncia: O Ministério Público oferece denúncia em face de Lucas Freitas pela prática do crime de roubo majorado no dia 10/05/2026."

#### 3. Fallback and Verification Mechanisms
- **Document Loading & Saving Verification**:
  - Tests should use `pytest`'s built-in `tmp_path` fixture to dynamically create a clean, sandboxed temporary folder directory.
  - Assert that all created file paths return `os.path.exists(path) == True` and that `os.path.getsize(path) > 0`.
  - Assert that file parsing libraries successfully return LangChain `Document` objects with correct string lengths and metadata schemas.
- **Offline / Demo Mode Verification**:
  - Implement a flag in the scraper script such as `demo_mode=True` or verify environment variables. If `demo_mode` is enabled, the code must skip network requests entirely, reading instead from a local directory of preset assets (`/tests/fixtures/`).
  - E2E tests will run with `demo_mode=True` and verify that the system creates complete, coherent timeline outputs even when disconnected.

---

## 5. Verification Method
To verify that this E2E test design is correctly implemented in subsequent phases:
1. Inspect the codebase for the creation of `tests/test_e2e_scraping_analysis.py` containing the 30 test cases outlined.
2. Execute the verification command:
   ```powershell
   python -m pytest -v tests/test_e2e_scraping_analysis.py
   ```
3. Invalidation conditions:
   - Tests fail to pass in an offline/disconnected environment.
   - Tests modify source code files outside of the `tests` directory.
   - The test suite has fewer than 5 tests per category for Tier 1 and Tier 2.
