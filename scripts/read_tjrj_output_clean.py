# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\resultado_lucas_tjrj.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== SUCESSO! RESULTADO DA BUSCA DE PROCESSOS DO LUCAS DE SOUZA FREITAS NO TJRJ ({len(content)} bytes) ===")
    print(content[:3500])
else:
    print(f"Arquivo {fpath} não encontrado. Checando arquivo em task log...")
