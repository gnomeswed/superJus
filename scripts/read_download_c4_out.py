# -*- coding: utf-8 -*-
import os

print("=== VERIFICANDO RESULTADO DO DOWNLOAD DO CADERNO IV DO DJERJ ===")
target_dir = r"C:\Projetos\Super Analista Jurídico\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"
files = os.listdir(target_dir)
djerj_files = [f for f in files if "DJERJ" in f]
print(f"Arquivos DJERJ presentes na pasta do cliente ({len(djerj_files)}):")
for df in djerj_files:
    fp = os.path.join(target_dir, df)
    print(f" - {df} ({os.path.getsize(fp)} bytes)")
