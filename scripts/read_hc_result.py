# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\habeas_corpus_2017_lucas_completo.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO TOTAL DO HABEAS CORPUS DO LUCAS ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} não foi gerado.")
