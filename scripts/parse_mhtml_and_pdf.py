# -*- coding: utf-8 -*-
import fitz
import re
from bs4 import BeautifulSoup

pdf_path = r"c:\Projetos\Super Analista Jurídico\Clientes\ecildo\dossie_processos_08073097290_2026-06-11_18-43.pdf"
mhtml_path1 = r"c:\Projetos\Super Analista Jurídico\Clientes\ecildo\Consulta Processual - TJMT.mhtml"
mhtml_path2 = r"c:\Projetos\Super Analista Jurídico\Clientes\ecildo\Consulta Processual - TJMT 2.mhtml"

print("=== INSPECTING PDF DOSSIE ===")
try:
    doc = fitz.open(pdf_path)
    pdf_text = ""
    for page in doc:
        pdf_text += page.get_text() + "\n--- PAGE ---\n"
    with open(r"c:\Projetos\Super Analista Jurídico\scripts\pdf_dossie_text.txt", "w", encoding="utf-8") as f:
        f.write(pdf_text)
    print(f"PDF text saved, length: {len(pdf_text)}")
except Exception as e:
    print(f"Error reading PDF: {e}")

print("\n=== INSPECTING MHTML 1 ===")
try:
    with open(mhtml_path1, "r", encoding="utf-8", errors="ignore") as f:
        html1 = f.read()
    soup1 = BeautifulSoup(html1, 'html.parser')
    text1 = soup1.get_text()
    with open(r"c:\Projetos\Super Analista Jurídico\scripts\mhtml1_text.txt", "w", encoding="utf-8") as f:
        f.write(text1)
    print(f"MHTML 1 text saved, length: {len(text1)}")
except Exception as e:
    print(f"Error reading MHTML 1: {e}")

print("\n=== INSPECTING MHTML 2 ===")
try:
    with open(mhtml_path2, "r", encoding="utf-8", errors="ignore") as f:
        html2 = f.read()
    soup2 = BeautifulSoup(html2, 'html.parser')
    text2 = soup2.get_text()
    with open(r"c:\Projetos\Super Analista Jurídico\scripts\mhtml2_text.txt", "w", encoding="utf-8") as f:
        f.write(text2)
    print(f"MHTML 2 text saved, length: {len(text2)}")
except Exception as e:
    print(f"Error reading MHTML 2: {e}")
