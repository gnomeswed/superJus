# -*- coding: utf-8 -*-
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

dir_path = r"c:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal"

terms = ["ligaç", "escuta", "intercepta", "whatsapp", "áudio", "voz", "vocálic", "operadora", "telefôn"]

print("=== BUSCANDO DETALHES DAS PROVAS TELEFÔNICAS vs WHATSAPP NO CASO JÚLIO ===")

found = []
for root, dirs, files in os.walk(dir_path):
    for f in files:
        if f.endswith(('.txt', '.md', '.json', '.html')):
            fp = os.path.join(root, f)
            try:
                content = open(fp, "r", encoding="utf-8", errors="ignore").read()
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    for t in terms:
                        if t in line.lower():
                            context = lines[max(0, i-1):min(len(lines), i+2)]
                            found.append((f, i+1, t, " ".join([c.strip() for c in context])))
                            break
            except Exception:
                pass

for f, line_no, term, ctx in found[:25]:
    print(f"\n📄 {f} (Linha {line_no} - '{term}'):")
    print(f"   {ctx[:300]}")
