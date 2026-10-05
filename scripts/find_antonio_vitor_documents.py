# -*- coding: utf-8 -*-
import json
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

print("=== BUSCANDO CPF / RG DO ANTÔNIO VITOR NOS DADOS DO PROCESSO ===")

base_dir = r"c:\Projetos\superJus"
json_path = r"c:\Projetos\superJus\Clientes\Antonio_Vitor\02_Movimentacoes\datajud_movimentacoes_completas.json"

if os.path.exists(json_path):
    with open(json_path, "r", encoding="utf-8", errors="ignore") as f:
        data = json.load(f)
    
    hits = data.get('hits', {}).get('hits', [])
    print(f"Instâncias encontradas no Datajud: {len(hits)}")
    
    for h in hits:
        src = h.get('_source', {})
        pessoas = src.get('pessoas', [])
        print(f"\nÓrgão: {src.get('orgaoJulgador', {}).get('nome')}")
        print(f"Pessoas cadastradas ({len(pessoas)}):")
        for p in pessoas:
            nome = p.get('nome', '')
            cpf = p.get('cpf', p.get('numeroDocumentoPrincipal', p.get('cnpj', 'N/I')))
            tipo_doc = p.get('tipoDocumentoPrincipal', 'N/I')
            polo = p.get('polo', 'N/I')
            print(f"  • Polo: {polo} | Nome: {nome} | Doc: {cpf} ({tipo_doc})")
            
            # Print full dict of person to find any hidden fields
            print(f"    Dict completo: {json.dumps(p, ensure_ascii=False)}")

# Buscar em outros arquivos de texto no projeto por "Antonio Vitor" ou "Antônio Vitor"
print("\nBusca textual por CPF/RG nas pastas do projeto:")
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(('.txt', '.json', '.md')):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if ("0175803" in content or "ANTONIO VITOR" in content.upper()) and ("CPF" in content.upper() or "RG" in content.upper() or "DOCUMENTO" in content.upper()):
                        lines = content.split('\n')
                        for l in lines:
                            if any(w in l.upper() for w in ["CPF", "RG", "DOCUMENTO", "0175803", "ANTONIO"]):
                                print(f"  [{os.path.basename(fp)}]: {l.strip()[:140]}")
            except Exception:
                pass

print("\n=== BUSCA FINALIZADA ===")
