# -*- coding: utf-8 -*-
import os

fpath = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\tjrj_live_29_07_2026_13h.txt"

if os.path.exists(fpath):
    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    print(f"=== RESULTADO DA VERIFICAÇÃO AUTOMÁTICA DAS 14H00 ({len(content)} bytes) ===")
    print(content)
else:
    print(f"Arquivo {fpath} ainda não foi gerado.")
