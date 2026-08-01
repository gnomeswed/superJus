# Scope: Implementation Track

## Architecture
- `scripts/tjrj_scraper_auto.py`: Scrapes process documents from TJRJ. Under demo mode, fallback to mock documents when needed.
- `scripts/process_and_timeline.py`: Processes the downloaded documents to extract a summary and construct a timeline.
- `app.py`: Streamlit application integrating the scraping and processing functions.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | M1: Scraping Automatizado (R1) | Implement `scripts/tjrj_scraper_auto.py` to download process documents without GUI prompts. Fallback to mock document in demo mode. | None | DONE |
| 2 | M2: Processamento e Linha do Tempo (R2) | Implement `scripts/process_and_timeline.py` to analyze the document and output facts summary and timeline. | M1 | DONE |
| 3 | M3: Integração Streamlit | Integrate M1 and M2 into `app.py`. | M2 | DONE |

## Interface Contracts
### Scraping Service (`scripts/tjrj_scraper_auto.py`)
- Function: `scrape_process_documents(process_number: str, save_dir: str) -> list[str]`
- Behavior: Downloads documents for process_number, saves them to save_dir, and returns list of local file paths. If blocked/offline, returns local mock document paths (demo mode).

### Analysis Service (`scripts/process_and_timeline.py`)
- Function: `generate_timeline_and_summary(doc_path: str, output_path: str) -> dict`
- Behavior: Processes doc_path, saves timeline/summary as markdown/json to output_path, and returns data dict containing timeline and summary.
