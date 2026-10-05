# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

print("=== VERIFICANDO PUBLICAÇÕES NO DJERJ — LEANDRO DA SILVA ===")

# Vamos consultar o serviço de busca de publicações no DJERJ
url_djerj = "https://www3.tjrj.jus.br/consultadjerj/consulta.aspx"

print("1. Verificando repositórios salvos no projeto...")
base_dir = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico"

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(('.txt', '.json', '.md')):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if "0827233" in content or "LEANDRO DA SILVA" in content.upper():
                        print(f"  • Encontrado registro em: {os.path.relpath(fp, base_dir)}")
            except Exception:
                pass

print("\n=== CONSULTA CONCLUÍDA ===")
