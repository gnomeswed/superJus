# -*- coding: utf-8 -*-
import os

dir_path = r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo"
f_movs = os.path.join(dir_path, "todos_movimentos_processo_2017_lucas.txt")
f_hc = os.path.join(dir_path, "hc_2017_lucas_tjrj.txt")

print("=== 1. MOVIMENTAÇÕES COMPLETAS DO PROCESSO DE 2017 (2ª VARA CRIMINAL DE NITERÓI) ===")
if os.path.exists(f_movs):
    with open(f_movs, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())
else:
    print(f"Arquivo {f_movs} não encontrado.")

print("\n=== 2. DECISÃO / INTEGRAL DO HABEAS CORPUS 0046418-98.2017.8.19.0000 ===")
if os.path.exists(f_hc):
    with open(f_hc, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())
else:
    print(f"Arquivo {f_hc} não encontrado.")
