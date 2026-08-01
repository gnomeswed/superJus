# Implementation Strategy: Automated TJRJ Scraper

This document outlines the analysis and implementation strategy for `scripts/tjrj_scraper_auto.py` based on existing code investigation (`scripts/tjrj_extractor.py` and `scripts/court_scraper.py`), system requirements, and the constraints of the `demo` integrity mode.

---

## 1. Architectural Context & Interface Contract

The scraper must implement the following function contract:

```python
def scrape_process_documents(process_number: str, save_dir: str) -> list[str]:
    """
    Downloads documents for the given process number, saves them to save_dir,
    and returns a list of local file paths of the saved documents.
    
    If running in 'Integrity mode: demo' and scraping fails (offline/blocked),
    it falls back to loading and copying mock files for the target test process.
    """
```

### Key Integration Points:
1. **Streamlit App Integration (`app.py`)**: Streamlit will invoke this function with user-provided process numbers.
2. **Analysis Service Integration (`scripts/process_and_timeline.py`)**: The return value of this scraper (a list of local file paths) will feed directly into the analyzer to parse and generate a timeline.
3. **E2E Testing Suite (`tests/test_e2e_scraping_analysis.py`)**: The testing suite will verify both the happy path (mocked Playwright flow) and the fallback path (triggering fallback mock file copying).

---

## 2. Investigation of Existing Codebase

### A. `scripts/court_scraper.py`
* **Purpose**: Fetches general metadata (status, class, subject, and the last 5 movements) via the public CNJ Datajud API.
* **Reusable Logic**:
  * Clean process number logic: `re.sub(r'\D', '', process_number)` which removes hyphens, dots, and other non-digit characters.
  * Tribunal mapping: `get_tribunal_endpoint` can be reused to determine if the process is from TJRJ.

### B. `scripts/tjrj_extractor.py`
* **Purpose**: A Playwright-based script to extract text contents of process movements and save them as individual files.
* **Limitations**:
  * **Requires User Action (Not Automated)**: Spawns a Windows GUI MessageBox requesting the user to manually search the process, select "Todos os Movimentos", and change pagination.
  * **Headless Limitation**: Designed for GUI mode; cannot easily run in headless test environments due to MessageBox blocking.
* **Reusable Logic**:
  * Playwright initialization and context creation.
  * Selector mapping inside the iframe: `page.query_selector("iframe#mainframe")`.
  * Modal handling and extraction: Evaluating JS on the iframe content frame to read the modal inner text from `#descricaoDetalhadaModal .modal-body`.
  * Document naming and sanitization: replacing invalid characters (`<>:"/\|?*`) and limiting filename length.

### C. Mock Documents Folder (`Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/`)
* **Purpose**: Contains mock files representing a real case (`0011857-95.2024.8.19.0002`).
* **Available Files**:
  * 15 `.txt` files containing process movements (e.g. `03-04-2025_Sentença em Audiência  - Proferida Sentença de Pronúncia.txt`).
  * 3 `.pdf` files (`motoboy.pdf`, `hrhe.pdf`, `jdsjs.pdf`).
  * 2 `.html` files (`rad5CCBF.html`, `radED68D.html`).
  * 2 temporary `.txt` files (`New Text Document.txt`, etc.).

---

## 3. Requirements & Solutions

| Requirement | Challenge | Proposed Solution |
|-------------|-----------|-------------------|
| **No GUI Prompts** | `MessageBoxW` blocks headless execution. | Remove `ctypes.windll.user32.MessageBoxW` entirely. |
| **Fully Automated Search** | Extrator currently waits for manual user input. | Use Playwright selectors inside the iframe to: <br>1. Fill the input field (e.g. `input#numProcesso` / `input[name="numProcesso"]`).<br>2. Click the search button (`button:has-text("Pesquisar")` / `input[type="submit"]`).<br>3. Wait for search results.<br>4. Click "Todos os Movimentos" and select "500 por página" pagination. |
| **Integrity Mode: Demo** | CODE_ONLY network block prevents loading external TJRJ site. | Implement a fallback mechanism: <br>1. Read `INTEGRITY_MODE` (from environment or config), defaulting to `demo`.<br>2. Catch any browser startup, navigation, or timeout error.<br>3. Check if cleaned `process_number` equals `"00118579520248190002"`. If yes, copy files from `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/` to `save_dir`. |

---

## 4. Proposed Clean Architecture for `tjrj_scraper_auto.py`

To separate concerns and ensure testability, the script should be organized into distinct components:

```
┌──────────────────────────────────────────────────────────┐
│             scrape_process_documents()                   │
│  (Entry Point / Orchester of Scraping & Fallback)        │
└────────────┬───────────────────────────────┬─────────────┘
             │                               │
             ▼ (Success path)                ▼ (Failure/Offline path)
┌──────────────────────────┐   ┌───────────────────────────┐
│  PlaywrightScraperEngine │   │    MockFallbackHandler    │
│  - headless browser      │   │  - checks process number  │
│  - automated search/DOM  │   │  - copies mock directory  │
│  - modal document extract│   │    to target save_dir     │
└──────────────────────────┘   └───────────────────────────┘
```

### Detailed Class/Function Design

#### 1. Configuration & Constants
```python
INTEGRITY_MODE = os.environ.get("INTEGRITY_MODE", "demo")
TEST_PROCESS_NUMBER = "00118579520248190002"
MOCK_DOCS_DIR = os.path.abspath(os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "Clientes", "Lucas_Freitas", "Caso_Principal", "documentos_processo"
))
```

#### 2. `MockFallbackHandler`
```python
def handle_demo_fallback(process_number: str, save_dir: str) -> list[str]:
    clean_number = re.sub(r"\D", "", process_number)
    if clean_number != TEST_PROCESS_NUMBER:
        print(f"[-] Fallback acionado, mas o processo {process_number} não é o caso de teste cadastrado.")
        return []
        
    if not os.path.exists(MOCK_DOCS_DIR):
        print(f"[-] Pasta de mocks não encontrada em: {MOCK_DOCS_DIR}")
        return []
        
    print(f"[*] Ativando fallback demo para processo: {process_number}")
    os.makedirs(save_dir, exist_ok=True)
    copied_files = []
    
    for filename in os.listdir(MOCK_DOCS_DIR):
        src_path = os.path.join(MOCK_DOCS_DIR, filename)
        if os.path.isfile(src_path):
            dst_path = os.path.join(save_dir, filename)
            shutil.copy2(src_path, dst_path)
            copied_files.append(dst_path)
            
    print(f"[+] Fallback concluído. Copiados {len(copied_files)} arquivos para {save_dir}.")
    return copied_files
```

#### 3. `PlaywrightScraperEngine` (Headless Scraping Flow)
```python
def run_headless_scraping(process_number: str, save_dir: str) -> list[str]:
    # 1. Start Playwright in headless=True mode
    # 2. Go to https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica
    # 3. Locate iframe#mainframe and get frame
    # 4. Fill search input (e.g. input#numProcesso) with process_number
    # 5. Click search button (e.g. button:has-text("Pesquisar"))
    # 6. Click "Todos os movimentos" link/button
    # 7. Select "500" from pagination sizing elements
    # 8. Fetch all "Original / Ver Íntegra" buttons
    # 9. Loop and extract each document modal's contents:
    #    - Click button
    #    - Wait for modal to update
    #    - Grab innerText of #descricaoDetalhadaModal .modal-body
    #    - Sanitize name and write to save_dir
    #    - Close modal
    # 10. Return list of paths
```

#### 4. Master Entry Point Logic
```python
def scrape_process_documents(process_number: str, save_dir: str) -> list[str]:
    clean_number = re.sub(r"\D", "", process_number)
    if not clean_number:
        raise ValueError("Número de processo inválido.")
        
    try:
        # Tenta realizar o scraping real no portal do TJRJ (headless)
        print(f"[*] Iniciando scraping real para processo: {process_number}")
        file_paths = run_headless_scraping(process_number, save_dir)
        if file_paths:
            return file_paths
        raise RuntimeError("Nenhum arquivo retornado pelo scraping real.")
        
    except Exception as e:
        print(f"[-] Erro ou indisponibilidade no scraping real: {e}")
        if INTEGRITY_MODE == "demo":
            return handle_demo_fallback(process_number, save_dir)
        else:
            # Em produção real, se falhar, propaga o erro ou retorna vazio
            raise e
```

---

## 5. Verification Method

To verify the correct operation of the scraper without relying on external servers, the following E2E unit tests will be implemented:

1. **Verify Fallback Triggering**:
   Call `scrape_process_documents("0011857-95.2024.8.19.0002", temp_dir)` under offline conditions (or by forcing browser failure). Assert that files are copied from `Clientes/Lucas_Freitas/...` and returned in the list.
2. **Verify Correct Paths**:
   Assert that every path returned in the list exists (`os.path.exists(path) == True`) and is within `save_dir`.
3. **Verify Invalid Input**:
   Assert that calling `scrape_process_documents("invalid-number", temp_dir)` raises `ValueError`.
