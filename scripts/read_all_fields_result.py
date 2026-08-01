# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\tjrj_lucas_2017_processos_final.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO TOTAL E DEFINITIVO! LISTA DE PROCESSOS DE LUCAS DE SOUZA FREITAS ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} ainda não foi gerado.")
