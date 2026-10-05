# -*- coding: utf-8 -*-
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== BUSCANDO CITAÇÕES DE DIÁRIO OFICIAL (DJERJ/DJEN) NOS DOCUMENTOS ===")

base_dir = r"c:\Projetos\superJus"

terms = ["DJEN", "DJERJ", "Publicação", "Publicacao", "602775138", "602661584", "DECI/2026"]

results = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(('.txt', '.md', '.json')):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if ("0023013" in content or "0029845" in content or "JULIO" in content.upper()) and ("DJERJ" in content.upper() or "DJEN" in content.upper() or "PUBLICA" in content.upper()):
                        results.append((fp, f, content))
            except Exception:
                pass

print(f"Arquivos com menção a Diário Oficial e ao Júlio: {len(results)}\n")

for fp, f, content in results[:10]:
    print(f"📄 Arquivo: {os.path.relpath(fp, base_dir)}")
    lines = content.split('\n')
    for line in lines:
        if any(term.upper() in line.upper() for term in ["DJERJ", "DJEN", "PUBLICAÇÃO", "PUBLICACAO", "602775138", "602661584"]):
            print(f"   • {line.strip()[:150]}")
    print("-" * 60)
