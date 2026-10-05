# -*- coding: utf-8 -*-
import os
import re
import fitz

search_dirs = [
    r"C:\Users\Administrator\Desktop",
    r"C:\Users\Administrator\Downloads",
    r"C:\Users\Administrator\Documents",
    r"C:\Projetos\superJus"
]

found = []

for d in search_dirs:
    if os.path.exists(d):
        for root, dirs, files in os.walk(d):
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

                if txt and ("lucas" in txt.lower() or "951-00552/2024" in txt.lower() or "0011857" in txt.lower()):
                    # Buscar CPF (11 dígitos) ou RG (7 a 9 dígitos) próximo de Lucas
                    for line in txt.split("\n"):
                        if any(k in line.lower() for k in ["cpf", "rg", "identidade", "ifp", "detran", "nascimento", "mãe", "marcia"]):
                            found.append((fpath, line.strip()))

print(f"Total de linhas suspeitas encontradas: {len(found)}")
for path, line in found[:20]:
    print(f"[{os.path.basename(path)}] {line[:150]}")
