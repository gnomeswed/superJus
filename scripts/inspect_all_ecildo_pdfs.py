# -*- coding: utf-8 -*-
import fitz
import os

folder = r"c:\Projetos\Super Analista Jurídico\Clientes\ecildo"
pdf_files = [f for f in os.listdir(folder) if f.endswith('.pdf')]

print(f"Found {len(pdf_files)} PDF files in {folder}:")

for pdf in pdf_files:
    pdf_path = os.path.join(folder, pdf)
    print(f"\n=================== {pdf} ===================")
    try:
        doc = fitz.open(pdf_path)
        print(f"Pages: {len(doc)}")
        for i, page in enumerate(doc):
            txt = page.get_text()
            print(f"--- Page {i+1} ---")
            print(txt.strip()[:1000])
    except Exception as e:
        print(f"Error reading {pdf}: {e}")
