# -*- coding: utf-8 -*-
import os
import sys

try:
    from pypdf import PdfReader
    from PIL import Image
    import io
except ImportError:
    pass

fpath = r"C:\Users\Administrator\Desktop\Julio Pereira Marcos.pdf"
target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
img_out_dir = os.path.join(target_dir, "paginas_digitalizadas_julio")
os.makedirs(img_out_dir, exist_ok=True)

reader = PdfReader(fpath)
print(f"Extraindo {len(reader.pages)} páginas do PDF {fpath}...")

saved_imgs = []
for idx, page in enumerate(reader.pages, start=1):
    for img_idx, img in enumerate(page.images, start=1):
        img_name = f"pagina_{idx}_img_{img_idx}.png"
        img_path = os.path.join(img_out_dir, img_name)
        with open(img_path, "wb") as f:
            f.write(img.data)
        saved_imgs.append(img_path)

print(f"Salvas {len(saved_imgs)} imagens das páginas digitalizadas em {img_out_dir}")

# Tentar OCR via pytesseract se disponível
try:
    import pytesseract
    ocr_texts = []
    for ipath in saved_imgs:
        txt = pytesseract.image_to_string(Image.open(ipath), lang='por')
        ocr_texts.append(f"=== {os.path.basename(ipath)} ===\n{txt}")
    
    ocr_file = os.path.join(target_dir, "_textos_extraidos", "Documentos_Pessoais_Julio_OCR.txt")
    with open(ocr_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(ocr_texts))
    print(f"OCR realizado com sucesso! Salvo em {ocr_file}")
except Exception as e:
    print(f"Tesseract/pytesseract não executado: {e}")
