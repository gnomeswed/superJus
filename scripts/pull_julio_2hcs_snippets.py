# -*- coding: utf-8 -*-
import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

print("=== EXTRAINDO ANDAMENTOS EXATOS DOS 2 HABEAS CORPUS DE JÚLIO PEREIRA MARCOS ===")

# 1. HC TJRJ (0029845-67.2026.8.19.0000)
hc_tjrj_file = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\_textos_extraidos\Andamento_Processo_0029845-67.2026.txt"

print("\n" + "="*70)
print("1. HABEAS CORPUS NO TJRJ — Nº 0029845-67.2026.8.19.0000 (7ª CÂMARA CRIMINAL)")
print("="*70)

if os.path.exists(hc_tjrj_file):
    content = open(hc_tjrj_file, "r", encoding="utf-8", errors="ignore").read()
    print(content[:2500])

# 2. HC / RHC NO STJ (HC 1.116.750 / RJ)
compilado_file = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\Diarios_Oficiais\Compilado_Diarios_Oficiais_Julio_Pereira_Marcos.md"

print("\n" + "="*70)
print("2. RECURSO ORDINÁRIO EM HC NO STJ — HC nº 1.116.750 / RJ (2026/0311210-7)")
print("="*70)

if os.path.exists(compilado_file):
    content_stj = open(compilado_file, "r", encoding="utf-8", errors="ignore").read()
    print(content_stj[:2500])
