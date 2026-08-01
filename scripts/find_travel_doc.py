# -*- coding: utf-8 -*-
import os
import fitz

search_dirs = [
    r"C:\Users\Administrator\Desktop",
    r"C:\Users\Administrator\Downloads"
]

results = []

for d in search_dirs:
    if os.path.exists(d):
        for fname in os.listdir(d):
            fpath = os.path.join(d, fname)
            if os.path.isfile(fpath) and fname.lower().endswith(".pdf"):
                try:
                    doc = fitz.open(fpath)
                    text = ""
                    for p in doc:
                        text += p.get_text()
                    results.append({
                        "name": fname,
                        "path": fpath,
                        "size": os.path.getsize(fpath),
                        "pages": len(doc),
                        "text_snippet": text[:500].replace('\n', ' ')
                    })
                except Exception as e:
                    results.append({"name": fname, "error": str(e)})

for r in results:
    print(f"=== {r['name']} ({r.get('pages', 0)} pags, {r.get('size', 0)} bytes) ===")
    print(r.get('text_snippet', r.get('error', '')))
    print("-" * 50)
