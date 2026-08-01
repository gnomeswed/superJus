# -*- coding: utf-8 -*-
import os
import re

search_dirs = [
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas",
    r"C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002"
]

matches = []

for sdir in search_dirs:
    if os.path.exists(sdir):
        for root, dirs, files in os.walk(sdir):
            for f in files:
                if f.endswith((".txt", ".json", ".html", ".md")):
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                            lines = file.readlines()
                            for i, line in enumerate(lines, start=1):
                                if any(k in line.lower() for k in ["cpf", "rg", "identidade", "lucas de souza", "nascimento", "filiação", "mãe"]):
                                    matches.append((fpath, i, line.strip()))
                    except Exception:
                        pass

print(f"Total de ocorrências encontradas: {len(matches)}")
for path, line_no, content in matches[:30]:
    fname = os.path.basename(path)
    print(f"[{fname}:{line_no}] {content}")
