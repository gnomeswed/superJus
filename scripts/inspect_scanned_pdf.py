# -*- coding: utf-8 -*-
import os
from pypdf import PdfReader

fpath = r"C:\Users\Administrator\Desktop\Julio Pereira Marcos.pdf"
reader = PdfReader(fpath)

print(f"Arquivo: {fpath}")
print(f"Páginas: {len(reader.pages)}")

for idx, page in enumerate(reader.pages, start=1):
    print(f"--- Página {idx} ---")
    print("Texto extraído direto:", repr(page.extract_text()[:200]))
    print("Imagens na página:", len(page.images))
    for img_idx, img in enumerate(page.images, start=1):
        print(f"  Imagem {img_idx}: {img.name} ({len(img.data)} bytes)")
