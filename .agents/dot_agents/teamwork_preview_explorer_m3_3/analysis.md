# Integration Analysis: Automated TJRJ Scraper and Process Timeline

This document analyzes how to integrate the automated scraping and timeline generation tools into `app.py` for Milestone 3.

---

## 1. Current State Observation

In `app.py`, the old `extract_tjrj` tool is imported and called inside the update button logic for **Atualização Eletrônica TJRJ** within the "Documentos" tab:

- **Location**: `app.py` (around lines 763–779)
- **Verbatim Code**:
```python
    process_number_tjrj = st.text_input("Número do Processo TJRJ", value=default_process_number, placeholder="Ex: 0011857-95.2021.8.19.0002", key="tjrj_process_number")
    if st.button("Abrir Extrator TJRJ", key="btn_open_tjrj"):
        if not process_number_tjrj.strip():
            st.warning("Informe o número do processo para abrir o extrator.")
        else:
            from scripts.tjrj_extractor import extract_tjrj
            try:
                save_dir = os.path.join(case_path, "documentos_processo")
                with st.spinner("Abrindo extrator TJRJ..."):
                    result = extract_tjrj(process_number_tjrj.strip(), save_dir)
                st.success("Extração finalizada.")
                st.text(result)
            except RuntimeError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Erro ao abrir extrator: {e}")
```

---

## 2. Integration Strategy

The new workflow requires a seamless, automated process without GUI blockers:
1. **Scrape**: Call `scrape_process_documents(process_number, save_dir)` which returns a list of paths to the saved documents.
2. **Process**: If documents were successfully obtained, run `generate_timeline_and_summary(doc_path=save_dir, output_path=out_path)` where:
   - `doc_path` is the `save_dir` directory.
   - `output_path` is `os.path.join(case_path, "analises", "Relatorio_Processo.json")`.
3. **Timeline Ingestion**: Extract the timeline list from the result (`result["timeline"]`), transform the dates from `"DD/MM/YYYY"` to a Plotly-compatible format (such as `"YYYY-MM-DD"` or `"YYYY-MM"`), clean or assign event names, and save it using `save_timeline(case_path, transformed_timeline)`.
4. **Error Handling**: Use Streamlit spinners (`st.spinner`), success logs (`st.success`), warning logs (`st.warning`), and error blocks (`st.error`).

---

## 3. Timeline Structure and Date Transformation

### Date Format Mapping
- `generate_timeline_and_summary` parses dates from the text and outputs `"DD/MM/YYYY"` (e.g., `"10/05/2026"`).
- `app.py`'s default timeline events use `"YYYY-MM"` format (e.g., `"2026-05"`).
- We can convert the date format:
  - Option A: `"YYYY-MM"` (`f"{parts[2]}-{parts[1]}"`) - Matches the app's default format.
  - Option B: `"YYYY-MM-DD"` (`f"{parts[2]}-{parts[1]}-{parts[0]}"`) - Provides finer resolution on the timeline without clustering multiple daily events on a single month node.
  - Option C: Fall back to the original string if the format is not matched or equals `"sem_data"`.

### Event Text Optimization
- `generate_timeline_and_summary` uses generic event names like `"Movimentação"` or `"Evento Processual"`, but places detailed context in the `"description"` key.
- To display useful information on the Plotly chart (which renders `event` as the marker text label), we can transform it:
  - If the event is generic (e.g., `"Movimentação"`, `"Evento Processual"`, `"Ingestão"`) and a non-empty `description` exists, we extract the first sentence (or truncate to the first 50 characters) and use it as the `event` label.

---

## 4. Proposed Code Replacement

Replace lines 768–778 in `app.py` with:

```python
            from scripts.tjrj_scraper_auto import scrape_process_documents
            from scripts.process_and_timeline import generate_timeline_and_summary
            try:
                save_dir = os.path.join(case_path, "documentos_processo")
                
                # Step 1: Headless extraction
                with st.spinner("Buscando documentos no TJRJ (execução automatizada)..."):
                    scraped_files = scrape_process_documents(process_number_tjrj.strip(), save_dir)
                
                if not scraped_files:
                    st.warning("Nenhum documento novo foi encontrado ou extraído do TJRJ.")
                else:
                    st.success(f"Extração finalizada com sucesso. {len(scraped_files)} documento(s) obtido(s).")
                    
                    # Step 2: Line timeline & summary generation
                    out_path = os.path.join(case_path, "analises", "Relatorio_Processo.json")
                    with st.spinner("Gerando linha do tempo e relatório consolidado..."):
                        result = generate_timeline_and_summary(save_dir, out_path)
                    
                    st.success("Relatório processual salvo com sucesso em analises/Relatorio_Processo.json.")
                    
                    # Step 3: Update and save editable timeline (timeline.json)
                    if "timeline" in result and result["timeline"]:
                        transformed_timeline = []
                        for item in result["timeline"]:
                            # Date Conversion (DD/MM/YYYY -> YYYY-MM-DD / YYYY-MM)
                            raw_date = item.get("date", "")
                            date_str = raw_date
                            if "/" in raw_date:
                                parts = raw_date.split("/")
                                if len(parts) == 3:
                                    date_str = f"{parts[2]}-{parts[1]}-{parts[0]}"  # Option B: YYYY-MM-DD
                            
                            # Event Description refinement for visualization
                            desc = item.get("description", "")
                            event_text = item.get("event", "Movimentação")
                            if event_text in ("Movimentação", "Evento Processual", "Ingestão") and desc:
                                # Extract first sentence/line, capped at 50 chars
                                clean_desc = desc.split("\n")[0].split(".")[0].strip()
                                if len(clean_desc) > 50:
                                    clean_desc = clean_desc[:50] + "..."
                                event_text = clean_desc
                                
                            transformed_timeline.append({
                                "date": date_str,
                                "event": event_text
                            })
                        
                        save_timeline(case_path, transformed_timeline)
                        st.success("Linha do tempo atualizada com os novos eventos!")
                        st.rerun()
            except ValueError as e:
                st.error(f"Erro de Validação: {e}")
            except PermissionError as e:
                st.error(f"Erro de Acesso: {e}")
            except Exception as e:
                st.error(f"Erro inesperado durante a atualização: {e}")
```

Additionally, it is recommended to update the button label on line 764:
- **Before**: `st.button("Abrir Extrator TJRJ", key="btn_open_tjrj")`
- **After**: `st.button("Executar Atualização TJRJ", key="btn_open_tjrj")`
*(Key is kept as `btn_open_tjrj` to maintain UI state reference integrity).*
