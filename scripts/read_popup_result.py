# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\decisao_monocratica_hc_lucas_2017.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO TOTAL DA DECISÃO MONOCRÁTICA DO HABEAS CORPUS DE 2017 ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} não foi gerado.")
