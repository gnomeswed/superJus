# -*- coding: utf-8 -*-
import os
import re

dir_path = r"C:\Projetos\superJus\Clientes\Lucas_Freitas"

rg_patterns = [
    r'\b\d{2}\.\d{3}\.\d{3}-\d{1,2}\b', # RG RJ 00.000.000-0
    r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b',    # CPF 000.000.000-00
    r'\b\d{9,11}\b',                    # Numeros puros de 9 a 11 digitos
    r'RG[^\n]*',
    r'CPF[^\n]*',
    r'IFP[^\n]*',
    r'identidade[^\n]*'
]

print("=== BUSCA POR PADRÕES DE RG / CPF / IFP / IDENTIDADE NOS ARQUIVOS DO LUCAS ===")

for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith(('.txt', '.json', '.md')):
            fp = os.path.join(root, f)
            with open(fp, "r", encoding="utf-8", errors="ignore") as file_obj:
                content = file_obj.read()
                for p in rg_patterns:
                    matches = re.findall(p, content, re.IGNORECASE)
                    if matches:
                        print(f"[{f}] Encontrado padrão ({p}): {matches[:5]}")
