# -*- coding: utf-8 -*-
import os
import re

search_dirs = [
    r"C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas",
    r"C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002"
]

for sdir in search_dirs:
    if os.path.exists(sdir):
        for root, dirs, files in os.walk(sdir):
            for f in files:
                fpath = os.path.join(root, f)
                if f.endswith(".txt") or f.endswith(".json"):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as file:
                            content = file.read()
                            # Procurar mencao a Lucas de Souza Freitas seguida de números
                            for m in re.finditer(r'LUCAS DE SOUZA FREITAS[^\n]{0,200}', content, re.IGNORECASE):
                                print(f"[{f}] {m.group(0)}")
                    except Exception:
                        pass
