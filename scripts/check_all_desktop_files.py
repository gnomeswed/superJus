# -*- coding: utf-8 -*-
import os
import json
from pypdf import PdfReader

desktop_dir = r"C:\Users\Administrator\Desktop"

results = []

for fname in os.listdir(desktop_dir):
    fpath = os.path.join(desktop_dir, fname)
    if os.path.isfile(fpath):
        size = os.path.getsize(fpath)
        ext = os.path.splitext(fname)[1].lower()
        snippet = ""
        if ext == ".pdf":
            try:
                reader = PdfReader(fpath)
                num_p = len(reader.pages)
                for p in reader.pages[:3]:
                    t = p.extract_text()
                    if t:
                        snippet += t + "\n"
                results.append({
                    "name": fname,
                    "type": "pdf",
                    "pages": num_p,
                    "size": size,
                    "snippet": snippet[:400].replace('\n', ' ')
                })
            except Exception as e:
                results.append({"name": fname, "type": "pdf", "size": size, "error": str(e)})
        elif ext in [".txt", ".mhtml", ".html"]:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    snippet = f.read(500)
                results.append({
                    "name": fname,
                    "type": ext,
                    "size": size,
                    "snippet": snippet[:400].replace('\n', ' ')
                })
            except Exception as e:
                results.append({"name": fname, "type": ext, "size": size, "error": str(e)})

output_path = r"C:\Projetos\Super Analista Jurídico\scripts\all_desktop_files_check.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Relatório gerado em {output_path}")
