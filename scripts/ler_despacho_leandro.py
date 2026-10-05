# -*- coding: utf-8 -*-
import fitz
import sys

sys.stdout.reconfigure(encoding="utf-8")

pdf_path = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\03_Documentos_do_Processo\Despacho_11_06_2026_Vista_MP.pdf"
doc = fitz.open(pdf_path)

print("=" * 80)
print(f"DESPACHO 11/06/2026 — JUIZA REGINA CÉLIA")
print("=" * 80)

for page_num in range(len(doc)):
    page = doc[page_num]
    print(page.get_text())
