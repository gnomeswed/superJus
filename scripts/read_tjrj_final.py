# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_final_lucas.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== SUCESSO! RESULTADO FINAL DA CONSULTA TJRJ PARA LUCAS DE SOUZA FREITAS ({len(content)} bytes) ===")
    print(content[:3500])
else:
    print(f"Arquivo {fpath} não encontrado!")
