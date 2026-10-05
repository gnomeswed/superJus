# -*- coding: utf-8 -*-
import os
import re

dir_path = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo"

keywords = [
    "júlio", "julio", "0023013", "0029845", "0022975", "0001140",
    "búzios", "buzios", "sidney rosa", "og fernandes", "1.116.750"
]

results = []
results.append("=== EXTRAMENTO EXATO DE TRECHOS NOS DOCUMENTOS E DIÁRIOS DE JÚLIO PEREIRA MARCOS ===")

for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith(('.txt', '.md', '.json', '.html')):
            fp = os.path.join(root, f)
            try:
                content = open(fp, "r", encoding="utf-8", errors="ignore").read()
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    for kw in keywords:
                        if kw in line.lower():
                            context = lines[max(0, i-2):min(len(lines), i+3)]
                            results.append(f"\n📄 ARQUIVO: {f} (Linha {i+1} - Ocorrência '{kw}'):")
                            results.append("-" * 60)
                            for c in context:
                                results.append(f"  {c.strip()}")
                            results.append("-" * 60)
            except Exception as e:
                pass

res_txt = "\n".join(results)
target_path = r"c:\Projetos\superJus\julio_snippets_result.txt"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(res_txt)

print("SUCESSO: Trechos salvos em " + target_path)
