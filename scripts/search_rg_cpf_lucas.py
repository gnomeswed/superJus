# -*- coding: utf-8 -*-
import os
import re
import fitz
from bs4 import BeautifulSoup

search_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas"

for root, dirs, files in os.walk(search_dir):
    for f in files:
        fpath = os.path.join(root, f)
        ext = os.path.splitext(f)[1].lower()
        txt = ""
        if ext == ".pdf":
            try:
                doc = fitz.open(fpath)
                for p in doc:
                    txt += p.get_text() + "\n"
            except Exception:
                pass
        elif ext in [".html", ".htm"]:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                    soup = BeautifulSoup(file.read(), 'html.parser')
                    txt = soup.get_text()
            except Exception:
                pass
        elif ext in [".txt", ".json", ".md"]:
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                    txt = file.read()
            except Exception:
                pass

        if txt:
            # Buscar padrões de CPF (xxx.xxx.xxx-xx) ou RG (xx.xxx.xxx-x ou números de 7-11 digitos)
            rg_cpf_matches = re.findall(r'(\b\d{2,3}[\.\s]?\d{3}[\.\s]?\d{3}[-\s]?\d{1,2}\b|\b\d{7,11}\b)', txt)
            if any(k in txt.lower() for k in ["cpf", "rg", "identidade", "detran", "ifp", "ssp"]):
                print(f"=== {f} ===")
                lines = txt.split('\n')
                for l in lines:
                    if any(k in l.lower() for k in ["cpf", "rg", "identidade", "detran", "ifp", "ssp", "lucas"]):
                        print(f"  -> {l.strip()[:150]}")
