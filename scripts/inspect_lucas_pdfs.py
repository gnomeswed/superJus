# -*- coding: utf-8 -*-
import os
import fitz

pdf_files = [
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\motoboy.pdf",
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\hrhe.pdf",
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\jdsjs.pdf"
]

for pfile in pdf_files:
    if os.path.exists(pfile):
        doc = fitz.open(pfile)
        print(f"=== PDF: {os.path.basename(pfile)} ({len(doc)} páginas) ===")
        for i, page in enumerate(doc):
            t = page.get_text()
            print(f"--- Página {i+1} ---")
            print(t[:500])
