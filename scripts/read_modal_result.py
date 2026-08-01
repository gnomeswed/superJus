# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\movimentos_e_personagens_2017.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO TOTAL DO MODAL E MOVIMENTO DE SOLTURA DE 2017 ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} ainda não foi gerado.")
