# -*- coding: utf-8 -*-
import re
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\Administrator\.gemini\antigravity\brain\2187cd0c-a701-4a55-bea5-ce9e775530e8\.system_generated\steps\2096\content.md"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

m = re.search(r'id=["\']__VIEWSTATE["\'] value=["\']([^"\']+)["\']', text)
if m:
    raw = base64.b64decode(m.group(1)).decode('latin1', errors='ignore')
    idx = raw.find("0004301-33")
    print(f"Encontrado na posicao: {idx}")
    if idx != -1:
        snippet = raw[max(0, idx-300):idx+2500]
        # Limpar tags html para ler melhor
        clean = re.sub(r'<[^>]+>', ' ', snippet)
        clean = re.sub(r'\s+', ' ', clean)
        print("=== TRECHO DA PAUTA DE JULGAMENTO ===")
        print(clean)
else:
    print("VIEWSTATE nao encontrado")
