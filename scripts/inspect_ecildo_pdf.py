# -*- coding: utf-8 -*-
import fitz

fpath = r"C:\Users\Administrator\Desktop\relatório ecildo.pdf"

try:
    doc = fitz.open(fpath)
    print(f"=== {fpath} ({len(doc)} páginas) ===")
    full_txt = ""
    for i, page in enumerate(doc):
        t = page.get_text()
        print(f"Página {i+1} len: {len(t)}")
        full_txt += f"\n--- Página {i+1} ---\n" + t
        
    out_txt = r"C:\Projetos\Super Analista Jurídico\scripts\relatorio_ecildo_text.txt"
    with open(out_txt, "w", encoding="utf-8") as f:
        f.write(full_txt)
    print(f"Texto salvo em {out_txt}")
except Exception as e:
    print("Erro ao abrir ecildo.pdf:", e)
