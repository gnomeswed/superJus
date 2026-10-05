# -*- coding: utf-8 -*-
import os
import re

root_dir = r"C:\Projetos\superJus\Clientes\Lucas_Freitas"
matches = []

for dirpath, _, filenames in os.walk(root_dir):
    for f in filenames:
        if f.endswith(('.txt', '.md', '.json')):
            p = os.path.join(dirpath, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    if re.search(r'tr[aá]fico', content, re.I) and ('2019' in content or '11.343' in content or 'FAC' in content):
                        # Find matching lines
                        for line_num, l in enumerate(content.split('\n'), 1):
                            if re.search(r'tr[aá]fico|2019|11\.343|entorpecente', l, re.I):
                                matches.append(f"[{f}:{line_num}] {l.strip()[:160]}")
            except Exception:
                pass

print(f"Total matches found: {len(matches)}")
for m in matches[:40]:
    print(m)
