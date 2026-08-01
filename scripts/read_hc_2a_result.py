# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\hc_2017_lucas_2a_instancia.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO TOTAL DO HABEAS CORPUS DE 2ª INSTÂNCIA ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} não foi gerado.")
