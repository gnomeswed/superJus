# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

print("=== PARSING DA RESPOSTA DA CONSULTA PÚBLICA PJe ===")

fp = r"c:\Projetos\superJus\Clientes\Leandro_Mecanico\scraping_2026-08-16\pje_consulta_resultado.html"

with open(fp, "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

# Find any tables or process cards
tables = re.findall(r'<table.*?>.*?</table>', html, re.DOTALL)
print(f"Total de tabelas na resposta: {len(tables)}")

for idx, t in enumerate(tables, start=1):
    clean = re.sub(r'<.*?>', ' ', t)
    lines = [l.strip() for l in clean.split('\n') if l.strip()]
    print(f"\n--- TABELA {idx} ({len(lines)} linhas) ---")
    for l in lines[:25]:
        print(f"  • {l}")

# Check for error or notice messages
notices = re.findall(r'class=".*?message.*?"|id=".*?message.*?"', html)
print(f"\nTotal de mensagens/notificações: {len(notices)}")

print("\n=== FIM DO PARSING ===")
