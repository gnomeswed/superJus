# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\resultado_lucas_tjrj_completo.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== CONTEÚDO DE {fpath} (tamanho {len(content)}) ===")
    print(content[:2500])
else:
    print(f"Arquivo {fpath} não encontrado!")
