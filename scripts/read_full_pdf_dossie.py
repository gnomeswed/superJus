# -*- coding: utf-8 -*-
with open(r"c:\Projetos\Super Analista Jurídico\scripts\pdf_dossie_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Split by process block or print all lines with process numbers and titles
blocks = text.split("--- PAGE ---")
print(f"Total pages in dossier PDF: {len(blocks)}")

for i, page in enumerate(blocks):
    print(f"\n=================== PAGE {i+1} ===================")
    print(page)
