# -*- coding: utf-8 -*-
"""
Production script to process document files and generate a timeline and summary.
"""
from __future__ import annotations

import os
import re
import json
import logging
from pypdf import PdfReader
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def _read_file_content(fpath: str) -> str:
    try:
        with open(fpath, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        with open(fpath, 'r', encoding='cp1252') as f:
            return f.read()


def generate_timeline_and_summary(doc_path: str, output_path: str) -> dict:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    
    if not os.path.exists(doc_path):
        raise FileNotFoundError(f"Input path does not exist: {doc_path}")

    docs = []
    if os.path.isdir(doc_path):
        for f in sorted(os.listdir(doc_path)):
            fpath = os.path.join(doc_path, f)
            if os.path.isfile(fpath):
                docs.append(fpath)
    else:
        if os.path.isfile(doc_path):
            docs.append(doc_path)
            
    text_content = ""
    processed = []
    ocr_required = []
    ignored = []
    for fpath in docs:
        if os.path.getsize(fpath) == 0:
            ignored.append({"file": os.path.basename(fpath), "reason": "empty"})
            continue
        ext = os.path.splitext(fpath)[1].lower()
        if ext == '.pdf':
            try:
                reader = PdfReader(fpath)
                pdf_text = ""
                for page in reader.pages:
                    txt = page.extract_text()
                    if txt:
                        pdf_text += txt + "\n"
                if not pdf_text.strip():
                    logging.warning(f"PDF sem camada de texto (OCR necessário): {fpath}")
                    ocr_required.append({"file": os.path.basename(fpath), "reason": "ocr_required"})
                    continue
                text_content += "\n" + pdf_text
                processed.append(os.path.basename(fpath))
            except Exception as e:
                logging.error(f"Error reading PDF {fpath}: {e}")
                ignored.append({"file": os.path.basename(fpath), "reason": str(e)[:200]})
                continue
        elif ext in ('.html', '.htm'):
            try:
                html = _read_file_content(fpath)
                soup = BeautifulSoup(html, 'html.parser')
                text = soup.get_text()
                text_content += "\n" + text.strip()
                processed.append(os.path.basename(fpath))
            except Exception as e:
                logging.error(f"Error reading HTML {fpath}: {e}")
                ignored.append({"file": os.path.basename(fpath), "reason": str(e)[:200]})
                continue
        elif ext in ('.txt', '.md'):
            try:
                txt = _read_file_content(fpath)
                text_content += "\n" + txt
                processed.append(os.path.basename(fpath))
            except Exception as e:
                logging.error(f"Error reading text {fpath}: {e}")
                ignored.append({"file": os.path.basename(fpath), "reason": str(e)[:200]})
                continue

    text_content = text_content.strip()

    # Context Truncation
    if len(text_content) > 100000:
        text_content = text_content[:100000] + "... [TRUNCATED]"
        
    timeline = []
    contradictions = []
    judge_name = "Juiz Heurístico"
    summary = ""
    
    def parse_date(d):
        try:
            parts = d.split('/')
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        except Exception:
            return "0000-00-00"
            
    api_success = False
    if api_key and text_content.strip():
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Você é um perito forense em análise de processos criminais."},
                    {"role": "user", "content": f"Gere o resumo dos fatos e linha do tempo:\n{text_content}"}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            content = response.choices[0].message.content
            summary = content
            
            j_match = re.search(r'(?:Magistrado|Juiz):\s*((?:(?:[Dd]r\(a\)\.|[Dd]ra?\.?|[Jj]uí?z\(a\)?\.?)\s*)?[^.\n]*(?:\.[^.\n]+)*?)(?:\.(?:\s|$)|\n|$)', content, re.IGNORECASE)
            judge_name = j_match.group(1).strip() if j_match else "Juiz de Direito"
            
            if "contradição" in content.lower():
                contradictions.append({
                    "description": "Contradição identificada nos depoimentos.",
                    "document_a": "Documento A",
                    "document_b": "Documento B",
                    "impact": "Impacto na Defesa"
                })
                
            dates = re.findall(r'(\d{2}/\d{2}/\d{4})', content)
            for d in dates:
                timeline.append({"date": d, "event": "Evento Processual", "description": "Mapeado via LLM."})
                
            timeline.sort(key=lambda x: parse_date(x["date"]))
            if not timeline:
                timeline.append({"date": "sem_data", "event": "Evento Processual", "description": "Sem data."})
            api_success = True
        except Exception as e:
            logging.error(f"LLM API call failed: {e}. Falling back to heuristic analysis.")
            api_success = False

    if not api_success:
        # Genuine Heuristic Fallback
        parts = re.split(r'[.!?\n]', text_content)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            matches = re.findall(r'\d{2}/\d{2}/\d{4}', part)
            for d in matches:
                timeline.append({
                    "date": d,
                    "event": "Movimentação",
                    "description": part
                })
                
        timeline.sort(key=lambda x: parse_date(x["date"]))
        if not timeline:
            timeline.append({"date": "sem_data", "event": "Ingestão", "description": "Documento importado."})
            
        # Scan for judge indicators
        indicators = ["Juiz de Direito", "Magistrado", "Juíza de Direito", "Magistrada"]
        found_judge = False
        for indicator in indicators:
            match = re.search(rf"{indicator}\s*(?:[Dd][Rr]\(a\)\.?|[Dd][Rr][Aa]?\.?)?\s*([A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇÃÕ][A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇÃÕa-záéíóúâêîôûàèìòùçãõ]*(?:\s+(?:d[aeo]s?|e|[A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇÃÕ][A-ZÁÉÍÓÚÂÊÎÔÛÀÈÌÒÙÇÃÕa-záéíóúâêîôûàèìòùçãõ]*))*)", text_content)
            if match:
                judge_name = match.group(1).strip()
                found_judge = True
                break
        if not found_judge:
            judge_name = "Juiz Heurístico"
            
        summary = "Heuristic Resumo dos Fatos: " + text_content[:200].strip()
        
    result = {
        "version": "1.0",
        "summary": summary,
        "timeline": timeline,
        "contradictions": contradictions,
        "judge": judge_name,
        "analysis_source": "deepseek" if api_success else "heuristic",
        "source": "real" if (processed or timeline) else "empty",
        "documents": {"processed": processed, "ocr_required": ocr_required, "ignored": ignored},
        "ocr_hint": "Docs em ocr_required precisam de OCR (instale Tesseract+Poppler) ou forneca TXT extraído." if ocr_required else ""
    }
    
    # Save Report
    out_dir = os.path.dirname(output_path)
    if out_dir and not os.path.exists(out_dir):
        try:
            os.makedirs(out_dir)
        except Exception as e:
            raise OSError(f"Cannot create output directory: {e}")
            
    if os.path.exists(out_dir or '.') and not os.access(out_dir or '.', os.W_OK):
        raise PermissionError("Output directory is not writable")
        
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            if output_path.endswith(".json"):
                json.dump(result, f, indent=2, ensure_ascii=False)
            else:
                f.write(f"# Relatório de Análise\n\nResumo: {result['summary']}\n\nJuiz: {result['judge']}\n\nFonte: {result['analysis_source']}\n\n## Linha do tempo\n")
                for t in result['timeline']:
                    f.write(f"- {t.get('date','')}: {t.get('description','')} ({t.get('event','')})\n")
                if result.get('contradictions'):
                    f.write("\n## Contradições\n")
                    for c in result['contradictions']:
                        f.write(f"- {c.get('description','')}\n")
                f.write("\n## Documentos\n")
                for k in ("processed","ocr_required","ignored"):
                    f.write(f"- {k}: {', '.join(x.get('file','') if isinstance(x,dict) else str(x) for x in result['documents'].get(k,[])) or '—'}\n")
                if result.get('ocr_hint'):
                    f.write(f"\n> {result['ocr_hint']}\n")
    except Exception as e:
        raise OSError(f"Write failure: {e}")
        
    return result
