# -*- coding: utf-8 -*-
import os

dir_path = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"

for fn in os.listdir(dir_path):
    if fn.startswith("integra_aba_"):
        fpath = os.path.join(dir_path, fn)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            txt = f.read()
        print(f"=== BINGO SUPREMO! ABA {fn} ({len(txt)} bytes) ===")
        print(txt)
