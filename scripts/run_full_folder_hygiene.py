# -*- coding: utf-8 -*-
import os
import sys
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

base_dir = r"c:\Projetos\superJus\Clientes"
script_path = r"c:\Projetos\superJus\.agents\skills\organizar_pastas_clientes\scripts\organizer_engine.py"
python_exe = r"C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe"

print("=== INICIANDO EXECUÇÃO COMPLETA DE HIGIENIZAÇÃO E DESDUPLICAÇÃO EM TODAS AS PASTAS ===")

for item in sorted(os.listdir(base_dir)):
    p = os.path.join(base_dir, item)
    if os.path.isdir(p):
        print(f"\n==================================================")
        print(f"📂 PROCESSANDO PASTA DE CLIENTE: {item}")
        print(f"==================================================")
        res = subprocess.run([python_exe, script_path, p, "--execute"], capture_output=True, text=True, encoding='utf-8')
        print(res.stdout)
        if res.stderr:
            print("Avisos/Erros:", res.stderr)

print("\n=== HIGIENIZAÇÃO COMPLETA DE TODAS AS PASTAS CONCLUÍDA COM SUCESSO! ===")
