# Analysis & Implementation Strategy: Automated TJRJ Scraper

## 1. Executive Summary
This document proposes a design and implementation strategy for the automated scraping service in `scripts/tjrj_scraper_auto.py`. The scraper will implement the function contract:
```python
def scrape_process_documents(process_number: str, save_dir: str) -> list[str]:
```
The service will automatically scrape process documents from the TJRJ portal using headless Playwright without GUI prompts (avoiding message boxes and manual interaction). When running in **Integrity mode: demo** under offline or blocked scenarios (such as CAPTCHA blocks), it will seamlessly fallback to local mock documents. If the process number matches `0011857-95.2024.8.19.0002`, it will load documents from the Lucas Freitas mock folder:
`Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/`

---

## 2. Investigation of Existing Scripts

### 2.1 `scripts/court_scraper.py` (Datajud Metadata API Scraper)
*   **Key Logic to Reuse**:
    *   **Process Number Sanitization**: Extracting digits using `clean_number = re.sub(r'\D', '', process_number)` (Line 34).
    *   **CNJ Format Verification**: Checking length validation (Line 9).
    *   **Tribunal Endpoint Mapping**: The function `get_tribunal_endpoint` (Lines 8-31) parses the CNJ number to identify the correct tribunal. This can be adapted to raise an error or route requests if a process belongs to a non-TJRJ tribunal (as `scrape_process_documents` is specifically for TJRJ).
*   **Limitations**:
    *   It only retrieves general case metadata (classification, subject, and recent motions list) from the public Datajud API. It does **not** download actual document text or attachments.

### 2.2 `scripts/tjrj_extractor.py` (Playwright-based Extrator)
*   **Key Logic to Reuse**:
    *   **Playwright Session Setup**: launching browser context with specific window viewport sizes (Lines 82-85).
    *   **Iframe Target Navigation**: Accessing `https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica` and locating `iframe#mainframe` (Lines 87-98).
    *   **Text content extraction JS script**: Extracting motion date, motion type, and modal detail contents (Lines 140-155, 203-226) via `frame.evaluate`.
    *   **Modal control JS script**: Hiding and cleaning up the modal backdrop using jQuery and DOM manipulation to avoid state overlap (Lines 176-183, 255-276).
    *   **Filenaming & Sanitization**: Removing invalid characters from file names via `_sanitize` (Line 52).
*   **Issues / Changes Needed for Automation**:
    *   **Eliminate Blocking GUI**: Remove the Windows message box (`ctypes.windll.user32.MessageBoxW` in Line 72) which halts headless runtime.
    *   **Headless execution**: Launch chromium in headless mode (`headless=True`) by default to run invisibly.
    *   **Automate Search Input**: Currently, the script has a 30-minute loop (`for i in range(600): time.sleep(3)`) waiting for the user to manually enter the process number, solve the CAPTCHA, click "Pesquisar", and select pagination. In `tjrj_scraper_auto.py`, the typing of the process number and clicking search must be automated.
    *   **Add Fallback Handler**: No fallback mechanism exists in `tjrj_extractor.py` for offline testing or CAPTCHA/network blockades.

---

## 3. Mock Directory Structure (Lucas Freitas)
The mock folder `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo` exists and contains 27 items, including:
*   `.txt` files with exact dates (e.g., `03-04-2025_Audiência Instrução e Julgamento.txt`, `03-04-2025_Sentença em Audiência  - Proferida Sentença de Pronúncia.txt`).
*   `.pdf` files (e.g., `hrhe.pdf`, `motoboy.pdf`).
*   `.html` files (e.g., `rad5CCBF.html`).
Our demo fallback must copy all valid document files from this folder into the requested `save_dir` and return their new absolute paths.

---

## 4. Proposed Clean Architecture for `scripts/tjrj_scraper_auto.py`

We propose structuring `scripts/tjrj_scraper_auto.py` into five distinct layers to enforce separation of concerns, testability, and clean error handling:

```
┌─────────────────────────────────────────────────────────────┐
│                     Orchestration Layer                     │
│                 scrape_process_documents()                  │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
               ▼                               ▼
┌──────────────────────────────┐ ┌────────────────────────────┐
│      Scraper Engine          │ │      Fallback Provider     │
│  (Headless Playwright)       │ │  (Local Mock Copy/Link)    │
└──────────────────────────────┘ └────────────────────────────┘
               │                               │
               └───────────────┬───────────────┘
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Validation & Utilities                    │
│     (CNJ sanitizer, filename sanitization, file IO)        │
└─────────────────────────────────────────────────────────────┘
```

1.  **Orchestrator Layer**:
    *   Main entry point `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`.
    *   Inspects the environment variable `INTEGRITY_MODE` (which defaults to `"demo"`).
    *   Decides whether to trigger the Fallback Provider directly (e.g., if offline, if the process matches `0011857-95.2024.8.19.0002` in demo mode, or if the Playwright scraper fails).
2.  **Validation Layer**:
    *   Validates process number formatting.
    *   Sanitizes and prepares the `save_dir` directory.
3.  **Playwright Scraper Engine (Online)**:
    *   Operates in `headless=True` mode.
    *   Contains the DOM navigation selectors.
    *   Automates input entering, search submission, pagination configurations, and looping through document modals to save text files.
4.  **Fallback Provider (Offline/Demo)**:
    *   Resolves the project root path.
    *   Locates the target mock documents in `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo`.
    *   Copies files to the target `save_dir` and returns their absolute paths.
5.  **Utilities Layer**:
    *   Filename sanitization, clean directory checks, logging.

---

## 5. Draft Implementation Strategy (Pseudocode)

Below is the proposed implementation draft for `scripts/tjrj_scraper_auto.py`:

```python
import os
import re
import shutil
import logging
from typing import List

# Setup Logging
logger = logging.getLogger("tjrj_scraper_auto")

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sync_playwright = None

DEMO_PROCESS_NUMBER = "00118579520248190002"  # Sanitized 0011857-95.2024.8.19.0002

def sanitize_filename(name: str) -> str:
    """Sanitizes strings to be safe for filenames."""
    return re.sub(r'[<>:"/\\|?*\n\r]', '_', name).strip()[:120]

def get_project_root() -> str:
    """Resolves project root path dynamically."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)

def get_mock_documents_source(process_number_clean: str) -> str:
    """Returns the mock directory path for a given sanitized process number."""
    project_root = get_project_root()
    # Default is the Lucas Freitas case folder
    return os.path.join(
        project_root, "Clientes", "Lucas_Freitas", "Caso_Principal", "documentos_processo"
    )

def copy_mock_documents(process_number_clean: str, save_dir: str) -> List[str]:
    """Copies mock files from the client folder to save_dir and returns target paths."""
    src_dir = get_mock_documents_source(process_number_clean)
    if not os.path.exists(src_dir):
        raise FileNotFoundError(f"Mock source folder does not exist: {src_dir}")
    
    os.makedirs(save_dir, exist_ok=True)
    copied_files = []
    
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        if os.path.isfile(src_file) and not filename.startswith("~$"):
            dest_file = os.path.join(save_dir, filename)
            shutil.copy2(src_file, dest_file)
            copied_files.append(os.path.abspath(dest_file))
            
    return copied_files

def scrape_process_documents(process_number: str, save_dir: str) -> List[str]:
    """
    Main entry point. Scrapes or loads fallback process documents.
    """
    clean_number = re.sub(r"\D", "", process_number)
    if len(clean_number) != 20:
        raise ValueError(f"Invalid process number format (must be 20 digits): {process_number}")
        
    save_dir = os.path.abspath(save_dir)
    os.makedirs(save_dir, exist_ok=True)
    
    # Read Integrity mode setting (default to 'demo')
    integrity_mode = os.environ.get("INTEGRITY_MODE", "demo").lower()
    
    # Check if we should directly trigger the fallback
    # In Demo Mode, if process matches Lucas Freitas' demo process, use fallback directly.
    if integrity_mode == "demo" and clean_number == DEMO_PROCESS_NUMBER:
        logger.info("[*] Integrity mode: demo. Using mock documents for Lucas Freitas.")
        return copy_mock_documents(clean_number, save_dir)
        
    # Attempt online scraping using Playwright
    try:
        if sync_playwright is None:
            raise RuntimeError("Playwright library not installed in this environment.")
        return scrape_online_tjrj(clean_number, save_dir)
    except Exception as e:
        logger.warning(f"[-] Online scraping failed or was blocked: {e}")
        if integrity_mode == "demo":
            logger.info("[*] Falling back to mock documents (demo mode).")
            return copy_mock_documents(clean_number, save_dir)
        raise e

def scrape_online_tjrj(clean_number: str, save_dir: str) -> List[str]:
    """
    Performs fully automated headless scraping of TJRJ.
    """
    saved_files = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        
        # 1. Access the TJRJ search portal
        page.goto(
            "https://www3.tjrj.jus.br/consultaprocessual/#/consultapublica",
            timeout=30000,
            wait_until="networkidle"
        )
        
        # 2. Wait for mainframe iframe
        iframe_element = page.wait_for_selector("iframe#mainframe", timeout=10000)
        frame = iframe_element.content_frame()
        if not frame:
            raise RuntimeError("Could not load TJRJ mainframe iframe.")
            
        # 3. Enter process number and search
        # Automated input selection inside the iframe:
        # Note: selectors should search common input fields inside the TJRJ angular application
        input_selector = "input#numeroProcesso, input[placeholder*='processo'], input[type='text']"
        frame.wait_for_selector(input_selector, timeout=10000)
        frame.fill(input_selector, clean_number)
        
        search_btn_selector = "button#pesquisar, button[type='submit'], button:has-text('Pesquisar')"
        frame.click(search_btn_selector)
        
        # 4. Wait for results page
        # If a CAPTCHA appears, this wait will timeout, triggering the fallback.
        # Check for results list or motion list:
        motion_selector = "app-movimento, button:has-text('original')"
        frame.wait_for_selector(motion_selector, timeout=15000)
        
        # 5. Handle pagination and view adjustments (Todos os Movimentos & 500 per page)
        # Select pagination configuration programmatically if elements are present
        try:
            # Code to click "Todos os movimentos" link/button
            all_motions_btn = frame.query_selector("button:has-text('Todos os Movimentos'), a:has-text('Todos os Movimentos')")
            if all_motions_btn:
                all_motions_btn.click()
                time.sleep(2)
        except Exception:
            pass
            
        # 6. Extract documents
        # Reuses the exact modal extraction loop from tjrj_extractor.py:
        btns_all = frame.query_selector_all("button")
        originals = [
            b for b in btns_all 
            if "original" in (b.inner_text() or "").lower() and "ver" in (b.inner_text() or "").lower()
        ]
        
        # (Modal scraping and file writing details as in tjrj_extractor.py, without GUI prompts)
        # ... modal extraction logic ...
        
        browser.close()
        
    return saved_files
```

---

## 6. Implementation Timeline & Recommendation
We recommend that the **Implementer** proceeds with writing `scripts/tjrj_scraper_auto.py` based on this strategy. 

Verification can be executed via the E2E test suite (currently planned under `tests/test_e2e_scraping_analysis.py`), checking that:
1.  Running with environment variable `INTEGRITY_MODE="demo"` and process `0011857-95.2024.8.19.0002` correctly copies files from `Clientes/Lucas_Freitas/Caso_Principal/documentos_processo/`.
2.  File outputs match the input mock documents and returns the list of written absolute paths.
3.  No Windows Dialog boxes or GUI requirements block execution.
