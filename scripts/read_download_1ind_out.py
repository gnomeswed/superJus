# -*- coding: utf-8 -*-
import os

pdf_p = r"C:\Users\Administrator\Desktop\202607291INDJETJRJ.pdf"
if os.path.exists(pdf_p):
    size = os.path.getsize(pdf_p)
    print(f"=== BINGO TOTAL! ARQUIVO DO CADERNO JUDICIAL DE 1ª INSTÂNCIA BAIXADO NO DESKTOP ({size} bytes) ===")
else:
    print("Arquivo 202607291INDJETJRJ.pdf ainda não foi criado no Desktop.")
