# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\tjrj_resultado_lucas_primeng.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== RESULTADO OBTIDO DO PRIMENG TJRJ ({len(content)} bytes) ===")
    print(content[:3500])
else:
    print(f"Arquivo {fpath} ainda não foi criado.")
