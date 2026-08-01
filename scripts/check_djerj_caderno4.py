# -*- coding: utf-8 -*-
import fitz # PyMuPDF
import os

pdf_path = r"C:\Users\Administrator\Desktop\20260729ADMDJETJRJ.pdf"
doc = fitz.open(pdf_path)

print(f"=== CABEÇALHO DO DJERJ (29/07/2026) ENCONTRADO NO DESKTOP ===")
print(f"Nome do arquivo: 20260729ADMDJETJRJ.pdf")
print(f"Total de Páginas: {len(doc)}")

first_page_text = doc[0].get_text("text")
print("\nTexto da 1ª Página:")
print(first_page_text[:1200])
