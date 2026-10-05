# -*- coding: utf-8 -*-
import os
import fitz

root_dir = r"C:\Projetos\superJus"

matches = []

for root, dirs, files in os.walk(root_dir):
    if ".venv" in root or ".git" in root:
        continue
    for f in files:
        fpath = os.path.join(root, f)
        ext = os.path.splitext(f)[1].lower()
        txt = ""
        if ext == ".pdf":
            try:
                doc = fitz.open(fpath)
                for p in doc:
                    txt += p.get_text() + "\n"
            except Exception:
                pass
        elif ext in [".txt", ".json", ".md", ".html"]:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                    txt = file.read()
            except Exception:
                pass

        if txt and ("alvará" in txt.lower() or "alvara" in txt.lower() or "soltura" in txt.lower()):
            for line in txt.split("\n"):
                if any(x in line.lower() for x in ["alvará", "alvara", "soltura"]) and len(line.strip()) > 10:
                    matches.append((fpath, line.strip()))

print(f"Total de ocorrências de Alvará/Soltura: {len(matches)}")
for path, line in matches[:25]:
    fname = os.path.basename(path)
    print(f"[{fname}] {line[:140]}")
