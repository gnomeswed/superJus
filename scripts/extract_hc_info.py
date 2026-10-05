# -*- coding: utf-8 -*-
import re
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = r"C:\Users\Administrator\.gemini\antigravity\brain\2187cd0c-a701-4a55-bea5-ce9e775530e8\.system_generated\steps\2110\content.md"
with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Buscar direto na string de base64 dentro do value
m = re.search(r'value="([A-Za-z0-9+/=]{100,})"', text)
if m:
    raw = base64.b64decode(m.group(1)).decode('latin1', errors='ignore')
    idx = raw.find("0105796-38")
    print(f"Encontrado na posicao: {idx}")
    if idx != -1:
        snippet = raw[max(0, idx-300):idx+3500]
        clean = re.sub(r'<[^>]+>', ' ', snippet)
        clean = re.sub(r'\s+', ' ', clean)
        print("=== TRECHO DO HABEAS CORPUS NA PAUTA ===")
        print(clean)
    else:
        # Procurar Daniel
        idx_d = raw.find("DANIEL FERREIRA")
        print("Busca por DANIEL FERREIRA:", idx_d)
        if idx_d != -1:
            snippet = raw[max(0, idx_d-300):idx_d+3500]
            clean = re.sub(r'<[^>]+>', ' ', snippet)
            clean = re.sub(r'\s+', ' ', clean)
            print("=== TRECHO DANIEL ===")
            print(clean)
else:
    print("Nao achou base64")
