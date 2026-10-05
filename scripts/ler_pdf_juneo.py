# -*- coding: utf-8 -*-
import fitz, sys
sys.stdout.reconfigure(encoding="utf-8")

pdf_path = r"c:\Projetos\superJus\Clientes\Pastor_Juneo\reportPDF.pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")
for i in range(len(doc)):
    print(f"\n--- PAGE {i+1} ---")
    print(doc[i].get_text())
