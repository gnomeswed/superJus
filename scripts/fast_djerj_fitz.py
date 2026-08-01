# -*- coding: utf-8 -*-
import fitz # PyMuPDF
import os

pdf_path = r"C:\Users\Administrator\Desktop\20260729ADMDJETJRJ.pdf"
doc = fitz.open(pdf_path)

print(f"=== ANÁLISE ULTRA-RÁPIDA DO DJERJ (29/07/2026) — TOTAL DE PÁGINAS: {len(doc)} ===")

terms = ["0023013-51", "0022975-39", "Júlio Pereira", "Julio Pereira", "Vitor Vale", "Gabriel Alves", "Búzios"]

found = False
for page_num in range(len(doc)):
    page = doc[page_num]
    text = page.get_text("text")
    for t in terms:
        if t.lower() in text.lower():
            found = True
            print(f"\n🎯 [BINGO!] PÁGINA {page_num + 1} — Termo: '{t}'")
            print("="*60)
            print(text)
            print("="*60)

if not found:
    print("Nenhum dos termos exatos foi encontrado no PDF. Exibindo cabeçalho das primeiras páginas:")
    for i in range(min(3, len(doc))):
        print(f"--- PÁGINA {i+1} ---")
        print(doc[i].get_text("text")[:800])
