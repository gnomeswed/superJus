# Analysis: TJRJ Integration and Timeline Generation

This report presents the analysis and verification of the integration of the TJRJ web scraper and the process report/timeline generator within the main `app.py` dashboard of **Super Analista Jurídico**.

---

## 1. Executive Summary
The target is to replace the old interactive/manual TJRJ extraction mechanism with a clean, fully automated background pipeline:
1. **Scraping**: Automated scraping of process documents from TJRJ using `scrape_process_documents` from `scripts/tjrj_scraper_auto.py`.
2. **Analysis & Summary**: Automatic processing of the downloaded files to extract the case summary, magistrate, list of events, and contradictions using `generate_timeline_and_summary` from `scripts/process_and_timeline.py`.
3. **Timeline Updating**: Standardizing the extracted timeline dates into the ISO-like format (`YYYY-MM-DD` / `YYYY-MM`) and saving them under `case_path/timeline.json` as a list of event dictionaries, so that the editable UI timeline loaded by `load_timeline` remains consistent and displays correctly.

---

## 2. Verification of app.py Code & Old State
### Old `extract_tjrj` Call (Before Integration)
Historically, `app.py` imported and called `extract_tjrj` under the "Atualização Eletrônica TJRJ" button:
- **Location**: Around line 768.
- **Old Import**: `from scripts.tjrj_extractor import extract_tjrj`
- **Old Execution**:
  ```python
  save_dir = os.path.join(case_path, "documentos_processo")
  with st.spinner("Abrindo extrator TJRJ..."):
      result = extract_tjrj(process_number_tjrj.strip(), save_dir)
  st.success("Extração finalizada.")
  st.text(result)
  ```
The old `extract_tjrj` relied on user interaction (via browser pops or message boxes) to manually navigate and click movements, which was not suitable for a headless production environment.

### Integrated State (Current Code in `app.py`)
In the current version of `app.py`, the old `extract_tjrj` import and execution block (lines 768–821) has been completely replaced with:
- **Scraper Import**: `from scripts.tjrj_scraper_auto import scrape_process_documents`
- **Timeline Generator Import**: `from scripts.process_and_timeline import generate_timeline_and_summary`

---

## 3. Analysis of the Integration Logic
The integration handles scraping, report generation, and timeline updating sequentially:

### Step A: Scraping (scrape_process_documents)
The process number inputted by the user is sanitized and passed to the automated scraper:
```python
save_dir = os.path.join(case_path, "documentos_processo")
with st.spinner("Buscando e baixando documentos do processo no TJRJ..."):
    scraped_files = scrape_process_documents(process_number_tjrj.strip(), save_dir)
```
- **Returns**: A list of absolute file paths to all successfully retrieved documents (e.g. metadata JSONs, text, PDF, HTML files).
- **Validation**: Strict CNJ format validation (20 digits or standard mask) is enforced inside `scrape_process_documents`.
- **Fallbacks**: If in demo mode and the target case is Lucas Freitas, it copies pre-existing mock files. If the TJRJ portal/Datajud queries fail, it safely returns an empty list `[]` instead of breaking.

### Step B: Report Generation (generate_timeline_and_summary)
If files were scraped, the timeline and summary engine is triggered:
```python
out_path = os.path.join(case_path, "analises", "Relatorio_Processo.json")
with st.spinner("Processando documentos e gerando linha do tempo/resumo..."):
    result = generate_timeline_and_summary(save_dir, out_path)
```
- **Inputs**: 
  - `doc_path`: `save_dir` (directory containing scraped files).
  - `output_path`: `out_path` (path to write the comprehensive JSON report).
- **Returns**: A dictionary containing:
  ```json
  {
    "summary": "Resumo dos fatos...",
    "timeline": [{"date": "DD/MM/YYYY", "event": "...", "description": "..."}],
    "contradictions": [...],
    "judge": "Nome do Juiz"
  }
  ```
- **Storage**: The complete result dictionary is written to `case_path/analises/Relatorio_Processo.json`.

### Step C: Standardizing and Saving to `timeline.json`
To prevent `load_timeline(case_path)` from breaking, the dictionary structure returned by `generate_timeline_and_summary` cannot be written directly to `timeline.json`. The UI expects `timeline.json` to be a flat list of event dicts with `date` and `event` keys.

To achieve this:
1. **Extract and Convert**: Loop over `result["timeline"]`, extracting each event.
2. **Date Format Standardization**: Convert dates from Brazilian format (`DD/MM/YYYY`) to ISO format (`YYYY-MM-DD`) using a regex pattern. This ensures chronological sorting works correctly in both Python and Plotly.
3. **Event Description Normalization**: Clean spacing and assign descriptions or event names.
4. **Sort and Save**: Sort the list of events chronologically and save it via the helper function `save_timeline`.

Here is the exact transformation logic implemented in `app.py`:
```python
raw_timeline = result.get("timeline", [])
transformed_timeline = []
for entry in raw_timeline:
    raw_date = entry.get("date", "")
    # Convert DD/MM/YYYY to YYYY-MM-DD
    if re.match(r'^\d{2}/\d{2}/\d{4}$', raw_date):
        parts = raw_date.split('/')
        formatted_date = f"{parts[2]}-{parts[1]}-{parts[0]}"
    else:
        formatted_date = raw_date
    
    event_text = entry.get("description", "") or entry.get("event", "")
    event_text = " ".join(event_text.split())
    transformed_timeline.append({
        "date": formatted_date,
        "event": event_text
    })

# Sort the timeline by date
transformed_timeline.sort(key=lambda x: x["date"])

# Save using the helper
save_timeline(case_path, transformed_timeline)
```

---

## 4. How the UI Displays the Updated Timeline
Once `save_timeline(case_path, transformed_timeline)` is called, the file `timeline.json` contains a flat list of events:
```json
[
  {
    "date": "2026-05-02",
    "event": "Decisão que indeferiu a liberdade provisória."
  },
  {
    "date": "2026-05-10",
    "event": "Oferecimento da denúncia pelo MP em face de Lucas Freitas."
  }
]
```
When the user goes to the Strategic View tab or does a page refresh, Streamlit calls `load_timeline(case_path)`:
```python
def load_timeline(case_path):
    """FEATURE 4: Carrega timeline editável."""
    tl_path = os.path.join(case_path, "timeline.json")
    if os.path.exists(tl_path):
        with open(tl_path, "r", encoding="utf-8") as f:
            return json.load(f)
```
Since the file format is a list, `json.load(f)` returns the list directly. The Plotly timeline and the manual event editor display and update this timeline seamlessly without format conflicts.

---

## 5. Potential Enhancements / Edge Case Mitigations
While the current integration is functional, the following improvements are recommended to increase robustness:

1. **Load Timeline Resiliency**:
   If an external script accidentally writes the entire dict structure to `timeline.json`, `load_timeline` should detect this and extract the `"timeline"` key to avoid crashing the Plotly render:
   ```python
   def load_timeline(case_path):
       tl_path = os.path.join(case_path, "timeline.json")
       if os.path.exists(tl_path):
           try:
               with open(tl_path, "r", encoding="utf-8") as f:
                   data = json.load(f)
                   if isinstance(data, dict):
                       return data.get("timeline", [])
                   return data
           except Exception:
               pass
       # fallback list...
   ```

2. **Save Timeline Dict Preservation**:
   If `timeline.json` is stored as a dictionary containing additional properties (`summary`, `judge`, etc.), `save_timeline` should update only the `"timeline"` sub-key instead of replacing the entire file with a list:
   ```python
   def save_timeline(case_path, timeline):
       tl_path = os.path.join(case_path, "timeline.json")
       existing_data = {}
       if os.path.exists(tl_path):
           try:
               with open(tl_path, "r", encoding="utf-8") as f:
                   existing_data = json.load(f)
           except Exception:
               pass
       if isinstance(existing_data, dict) and "timeline" in existing_data:
           existing_data["timeline"] = timeline
           with open(tl_path, "w", encoding="utf-8") as f:
               json.dump(existing_data, f, ensure_ascii=False, indent=2)
       else:
           with open(tl_path, "w", encoding="utf-8") as f:
               json.dump(timeline, f, ensure_ascii=False, indent=2)
   ```
