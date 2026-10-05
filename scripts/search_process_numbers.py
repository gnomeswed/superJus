# -*- coding: utf-8 -*-
import os
import re

root_dir = r"C:\Projetos\superJus\Clientes"

found = set()

for root, dirs, files in os.walk(root_dir):
    for f in files:
        fpath = os.path.join(root, f)
        ext = os.path.splitext(f)[1].lower()
        if ext in [".txt", ".json", ".md", ".html"]:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                    txt = file.read()
                    matches = re.findall(r'\b\d{7}-\d{2}\.\d{4}\.8\.19\.\d{4}\b', txt)
                    for m in matches:
                        found.add((m, f))
            except Exception:
                pass

print("Todos os números de processo encontrados em Clientes:")
for num, fname in sorted(found):
    print(f" - {num} (no arquivo {fname})")
