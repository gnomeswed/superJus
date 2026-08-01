# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\tjrj_lucas_2017_sucesso.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO! PROCESSO(S) ENCONTRADO(S) NO TJRJ PARA LUCAS DE SOUZA FREITAS ({len(content)} bytes) ===")
    print(content[:4000])
else:
    print(f"Arquivo {fpath} não foi gerado.")
