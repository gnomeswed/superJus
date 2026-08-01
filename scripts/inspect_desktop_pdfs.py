# -*- coding: utf-8 -*-
import os
import json
from pypdf import PdfReader

desktop_files = [
    r"C:\Users\Administrator\Desktop\DENUNCIA.pdf",
    r"C:\Users\Administrator\Desktop\Julio Pereira Marcos.pdf",
    r"C:\Users\Administrator\Desktop\MP pelo indef.pdf",
    r"C:\Users\Administrator\Desktop\processo Júlio .pdf"
]

results = {}

for fpath in desktop_files:
    fname = os.path.basename(fpath)
    if os.path.exists(fpath):
        try:
            reader = PdfReader(fpath)
            num_pages = len(reader.pages)
            text_snippet = ""
            for p in reader.pages[:5]:  # Primeiras 5 paginas
                t = p.extract_text()
                if t:
                    text_snippet += t + "\n"
            results[fname] = {
                "pages": num_pages,
                "size_bytes": os.path.getsize(fpath),
                "text_snippet": text_snippet[:1500]
            }
        except Exception as e:
            results[fname] = {"error": str(e)}

output_path = r"C:\Projetos\Super Analista Jurídico\scripts\desktop_pdfs_inspection.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"Inspeção concluída! Resultados salvos em {output_path}")
