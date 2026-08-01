# -*- coding: utf-8 -*-
import fitz # PyMuPDF
import os
import shutil

desktop_pdf = r"C:\Users\Administrator\Desktop\20260729EDIDJETJRJ_1.pdf"
target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
target_pdf = os.path.join(target_dir, "DJERJ_29_07_2026_Caderno5_Editais.pdf")

shutil.copy2(desktop_pdf, target_pdf)
print(f"Copiado {desktop_pdf} -> {target_pdf}")

doc = fitz.open(target_pdf)
print(f"=== ANÁLISE DO CADERNO V (EDITAIS E AVISOS - 29/07/2026) — TOTAL PÁGINAS: {len(doc)} ===")

terms = [
    "0023013-51.2021.8.19.0078",
    "0022975-39.2021.8.19.0078",
    "00230135120218190078",
    "Júlio Pereira Marcos",
    "Julio Pereira Marcos",
    "Vitor Vale",
    "Gabriel Alves",
    "Búzios",
    "Armação dos Búzios"
]

found = False
for p in range(len(doc)):
    page_txt = doc[p].get_text("text")
    for t in terms:
        if t.lower() in page_txt.lower():
            found = True
            print(f"\n🎯 [BINGO!] PÁGINA {p+1} — Termo: '{t}'")
            print("="*60)
            print(page_txt)
            print("="*60)

if not found:
    print("\nNenhum dos termos exatos do Júlio foi encontrado no Caderno V. Exibindo o texto integral do Caderno V:")
    for i in range(len(doc)):
        print(f"\n--- PÁGINA {i+1} ---")
        print(doc[i].get_text("text"))
