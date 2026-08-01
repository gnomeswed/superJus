# -*- coding: utf-8 -*-
import os
import json
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

img_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\paginas_renderizadas"
out_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\_textos_extraidos"
os.makedirs(out_dir, exist_ok=True)

ocr_pages = []

for i in range(1, 6):
    img_path = os.path.join(img_dir, f"pagina_{i}.png")
    if os.path.exists(img_path):
        print(f"Executando RapidOCR na Página {i}...")
        result, _ = engine(img_path)
        page_text = ""
        if result:
            lines = [line[1] for line in result]
            page_text = "\n".join(lines)
        ocr_pages.append(f"--- PÁGINA {i} ---\n{page_text}")

full_text = "\n\n".join(ocr_pages)
txt_path = os.path.join(out_dir, "Documentos_Pessoais_e_Procedimento_Julio_OCR.txt")
with open(txt_path, "w", encoding="utf-8") as f:
    f.write(full_text)

print(f"OCR Concluído! Texto extraído salvo em {txt_path}. Tamanho: {len(full_text)} caracteres.")
