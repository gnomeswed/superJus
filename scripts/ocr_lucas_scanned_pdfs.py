# -*- coding: utf-8 -*-
import os
import fitz

pdf_files = [
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\motoboy.pdf",
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\hrhe.pdf",
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\jdsjs.pdf"
]

out_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\imagens_digitalizadas"
os.makedirs(out_dir, exist_ok=True)

for pfile in pdf_files:
    if os.path.exists(pfile):
        fname = os.path.splitext(os.path.basename(pfile))[0]
        doc = fitz.open(pfile)
        for i, page in enumerate(doc):
            pix = page.get_pixmap(dpi=150)
            png_path = os.path.join(out_dir, f"{fname}_page_{i+1}.png")
            pix.save(png_path)
            print(f"Salvo {png_path}")
