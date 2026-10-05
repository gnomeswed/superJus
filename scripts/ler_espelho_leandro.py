# -*- coding: utf-8 -*-
import fitz # PyMuPDF
import sys

sys.stdout.reconfigure(encoding="utf-8")

pdf_path = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\03_Documentos_do_Processo\Espelho_Processual_Leandro_16_08_2026.pdf"
doc = fitz.open(pdf_path)

print("=" * 80)
print(f"ESPELHO PROCESSUAL LEANDRO MECÂNICO — {len(doc)} PÁGINAS")
print("=" * 80)

for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text()
    print(f"\n--- PÁGINA {page_num + 1} ---")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for l in lines[:40]:
        print(f"  {l}")
