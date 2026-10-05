# -*- coding: utf-8 -*-
"""Extrai modelos do provider commandcode do bundle do 9router."""
import re, sys
sys.stdout.reconfigure(encoding="utf-8")

path = r"C:\Users\Administrator\AppData\Local\hermes\node\node_modules\9router\app\.next-cli-build\server\chunks\4963.js"
with open(path, encoding="utf-8", errors="ignore") as f:
    content = f.read()

# Achar o bloco do provider commandcode
idx = content.find('id:"commandcode"')
if idx < 0:
    print("commandcode não encontrado")
    sys.exit(0)

bloco = content[idx:idx+30000]
# Extrair modelos: id:"xxx",name:"yyy"
modelos = re.findall(r'id:"([^"]+)",name:"([^"]+)"', bloco)
print(f"=== Modelos do provider commandcode ({len(modelos)}) ===")
for mid, name in modelos:
    print(f" - {mid} | {name}")

# Ver se menciona muse ou mimo
print("\n=== Menções a muse/mimo ===")
for m in re.finditer(r'(muse|mimo)[^",}]{0,60}', bloco, re.IGNORECASE):
    print(" ", m.group(0)[:80])
