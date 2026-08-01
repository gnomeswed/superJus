# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\todos_movimentos_julio_28_07_2026.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== BINGO TOTAL! TODOS OS MOVIMENTOS DO JÚLIO PEREIRA MARCOS (28/07/2026) ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} ainda não foi gerado.")
