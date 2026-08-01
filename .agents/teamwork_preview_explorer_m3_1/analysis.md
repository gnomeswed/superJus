# M3 Integration Analysis Report

## Executive Summary
This report analyzes the integration of the new automated TJRJ scraper (`scripts/tjrj_scraper_auto.py`) and the timeline generator (`scripts/process_and_timeline.py`) into the main Streamlit application (`app.py`). It highlights the differences between the old semi-manual extractor and the new automated service, outlines two implementation pathways for saving and loading timeline data, and details the logic behind date sorting and JSON structure compatibility.

---

## 1. Relocation of the Old Extractor (`extract_tjrj`)
In the original/previous state of `app.py` (around line 768), the old `extract_tjrj` function from `scripts.tjrj_extractor` was imported and executed inside a Streamlit button click event:

### Code Snippet (Old Implementation)
```python
768:             from scripts.tjrj_extractor import extract_tjrj
769:             try:
770:                 save_dir = os.path.join(case_path, "documentos_processo")
771:                 with st.spinner("Abrindo extrator TJRJ..."):
772:                     result = extract_tjrj(process_number_tjrj.strip(), save_dir)
773:                 st.success("Extração finalizada.")
774:                 st.text(result)
```

### Characteristics of the Old Extractor:
- Interactively popped up a Chromium GUI using Windows API `ctypes.windll.user32.MessageBoxW`.
- Required manual intervention from the user to navigate the portal, select pagination, and click buttons.
- Returned a plain text success/failure log message.

---

## 2. Transition to the Automated Scraper and Timeline Generation
The new service, `scrape_process_documents`, operates in a fully automated, headless fashion. Once the documents are downloaded to the target directory, `generate_timeline_and_summary` parses them using pyPDF, BeautifulSoup, and DeepSeek (or a regex fallback) to extract the judge, summary, and process timeline.

### Integration Steps:
1. **Import the New Modules:**
   ```python
   from scripts.tjrj_scraper_auto import scrape_process_documents
   from scripts.process_and_timeline import generate_timeline_and_summary
   ```
2. **Execute Headless Scraping:**
   Call `scrape_process_documents(process_number, save_dir)` which returns a list of paths of all successfully written documents.
3. **Execute Document Parsing & Timeline Generation:**
   Call `generate_timeline_and_summary(save_dir, output_path)` to ingest all documents in `save_dir` and write a structured dictionary output containing:
   - `summary`: text summary of facts.
   - `timeline`: list of events, e.g., `[{"date": "10/05/2026", "event": "...", "description": "..."}]`.
   - `contradictions`: list of detected conflicts.
   - `judge`: identified judge or magistrate.

---

## 3. Storage and UI Compatibility Tradeoffs for `timeline.json`

When saving the results of `generate_timeline_and_summary` to update the client's timeline, there are two primary approaches.

### Approach A: Programmatic Parsing & Flat List Storage (Currently Selected)
In this approach, the timeline is processed programmatically in `app.py` before saving to `timeline.json`. The output of `generate_timeline_and_summary` is saved to a report file (e.g., `analises/Relatorio_Processo.json`), and the timeline events are extracted, date-converted, and sorted:

#### Implementation Logic:
```python
# 1. Generate full analysis
result = generate_timeline_and_summary(save_dir, out_path)

# 2. Extract and format raw timeline events
raw_timeline = result.get("timeline", [])
transformed_timeline = []
for entry in raw_timeline:
    raw_date = entry.get("date", "")
    # Convert DD/MM/YYYY (from scraper) to YYYY-MM-DD (for Plotly/sorting)
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

# 3. Sort chronologically
transformed_timeline.sort(key=lambda x: x["date"])

# 4. Save to timeline.json
save_timeline(case_path, transformed_timeline)
```

#### Tradeoff Analysis:
- **Pros:**
  - Maintains `timeline.json` as a simple, flat JSON array of dicts (fully compatible with `load_timeline()` and the Plotly rendering loop).
  - Converts dates from `DD/MM/YYYY` to `YYYY-MM-DD`. This is crucial because standard string sorting of `DD/MM/YYYY` is alphabetically incorrect (sorting by day first). `YYYY-MM-DD` guarantees correct chronological sorting in Python and Plotly.
  - Minimizes changes to the rest of `app.py`'s timeline editing functionality.
- **Cons:**
  - Moves formatting and cleaning logic into `app.py` rather than keeping it inside the service script.

---

### Approach B: Direct Dict Storage with UI Load/Save Upgrades
In this approach, `generate_timeline_and_summary` writes its dictionary result directly to `timeline.json` under `case_path`.

#### Required Code Modifications:
1. **Update `load_timeline` in `app.py`** to extract the list of events from the dictionary if a dict is loaded:
   ```python
   def load_timeline(case_path):
       tl_path = os.path.join(case_path, "timeline.json")
       if os.path.exists(tl_path):
           with open(tl_path, "r", encoding="utf-8") as f:
               data = json.load(f)
               if isinstance(data, dict) and "timeline" in data:
                   return data["timeline"]
               return data
       return [...]
   ```
2. **Update `save_timeline` in `app.py`** to prevent overwriting/destroying other keys (like `summary` and `judge`) when the user edits a timeline event:
   ```python
   def save_timeline(case_path, timeline):
       tl_path = os.path.join(case_path, "timeline.json")
       data = {}
       if os.path.exists(tl_path):
           try:
               with open(tl_path, "r", encoding="utf-8") as f:
                   data = json.load(f)
           except Exception:
               pass
       
       if isinstance(data, dict):
           data["timeline"] = timeline
       else:
           data = timeline
           
       with open(tl_path, "w", encoding="utf-8") as f:
           json.dump(data, f, ensure_ascii=False, indent=2)
   ```

#### Tradeoff Analysis:
- **Pros:**
  - `timeline.json` acts as a single source of truth containing the summary, timeline list, contradictions, and judge name.
- **Cons:**
  - Date sorting issue: the raw `timeline` output of `generate_timeline_and_summary` uses `DD/MM/YYYY` formatting. Under this approach, the timeline would fail to sort chronologically unless additional date conversion is introduced inside the load/render cycle.

---

## 4. Proposed/Current Code Integration in `app.py`
The current codebase in `app.py` implements **Approach A** elegantly between lines 764 and 821, validating and executing the scraping, generating the process report, sanitizing/sorting the timeline dates to `YYYY-MM-DD`, and displaying the extracted magistrate and summary in the UI.

### Integrated Code Block:
```python
    if st.button("Executar Atualização TJRJ", key="btn_open_tjrj"):
        if not process_number_tjrj.strip():
            st.warning("Informe o número do processo para executar a atualização.")
        else:
            from scripts.tjrj_scraper_auto import scrape_process_documents
            from scripts.process_and_timeline import generate_timeline_and_summary
            try:
                save_dir = os.path.join(case_path, "documentos_processo")
                out_path = os.path.join(case_path, "analises", "Relatorio_Processo.json")
                
                with st.spinner("Buscando e baixando documentos do processo no TJRJ..."):
                    scraped_files = scrape_process_documents(process_number_tjrj.strip(), save_dir)
                
                if not scraped_files:
                    st.warning("Nenhum documento novo foi encontrado ou extraído.")
                else:
                    st.info(f"Sucesso: {len(scraped_files)} documentos obtidos.")
                    
                with st.spinner("Processando documentos e gerando linha do tempo/resumo..."):
                    result = generate_timeline_and_summary(save_dir, out_path)
                
                # Transform and save timeline
                raw_timeline = result.get("timeline", [])
                transformed_timeline = []
                for entry in raw_timeline:
                    raw_date = entry.get("date", "")
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
                
                transformed_timeline.sort(key=lambda x: x["date"])
                save_timeline(case_path, transformed_timeline)
                
                st.success("Atualização TJRJ e processamento concluídos com sucesso! A linha do tempo foi atualizada.")
                st.markdown(f"**Juiz do caso:** {result.get('judge', 'Não identificado')}")
                st.markdown(f"**Resumo do processo:** {result.get('summary', 'Não disponível')}")
                
            except ValueError as e:
                st.error(f"Erro de formato: {e}")
            except PermissionError as e:
                st.error(f"Erro de permissão no diretório: {e}")
            except Exception as e:
                st.error(f"Erro durante a atualização: {e}")
```
