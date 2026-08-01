# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_perfect_lucas.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO ABSOLUTO! RESULTADO DOS PROCESSOS DO LUCAS NO TJRJ ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} ainda não foi gerado.")
