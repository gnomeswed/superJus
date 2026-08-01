# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo\processo_antigo_0000253_2017_lucas.md"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO TOTAL DO PROCESSO 0000253-78.2017.8.19.0004 ({len(content)} bytes) ===")
    print(content[:4000])
else:
    print(f"Arquivo {fpath} ainda não foi gerado.")
