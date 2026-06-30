from __future__ import annotations

import os
import re
from typing import Optional


DEFAULT_EXTS = {".txt", ".html", ".htm", ".csv", ".md", ".pdf"}


def search_docs(root: str, query: str, exts=None, max_results=50):
    """Busca textual simples nos arquivos da pasta documents_dir.
    Retorna lista de dicts: {name, path, snippet, relevance}.
    """
    if exts is None:
        exts = DEFAULT_EXTS
    exts = {e.lower() for e in exts}
    q = (query or "").strip()
    if not q:
        return []
    terms = [part for part in re.split(r"\s+", q) if part]
    results = []
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext not in exts:
                continue
            path = os.path.join(dirpath, filename)
            text = _read_text_file(path)
            if not text and ext in {".pdf"}:
                text = _try_extract_pdf_text(path)
            if not text:
                continue
            lowered = text.lower()
            matched_terms = [t for t in terms if t.lower() in lowered]
            if not matched_terms:
                continue
            score = (len(matched_terms) / max(1, len(terms))) * 100
            # snippet ao redor do primeiro termo
            first = next((t for t in terms if t.lower() in lowered), None)
            start = lowered.find((first or "").lower(), 0)
            if start < 0:
                start = 0
            start = max(0, start - 120)
            end = min(len(text), start + 300)
            snippet = _normalize(text[start:end])
            rel = round(score, 1)
            results.append(
                {
                    "name": filename,
                    "path": path,
                    "snippet": snippet,
                    "relevance": rel,
                }
            )
    results.sort(key=lambda item: (-item["relevance"], item["name"]))
    return results[: max_results]
