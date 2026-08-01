# -*- coding: utf-8 -*-
import json
import os

path = r"C:\Projetos\Super Analista Jurídico\Clientes\Processo_0011857-95.2024.8.19.0002\datajud_metadata.json"

if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    print("=== DADOS DO DATAJUD FOR NITERÓI JÚRI ===")
    
    # Navegar por polo / parte / pessoa
    polos = data.get('polo', [])
    if not polos and 'hits' in data:
        for hit in data['hits']['hits']:
            src = hit['_source']
            polos = src.get('polo', [])
            
    def search_dict(d, level=0):
        if isinstance(d, dict):
            for k, v in d.items():
                if any(x in k.lower() for x in ['pessoa', 'documento', 'numero', 'cpf', 'rg', 'nome', 'identificacao']):
                    print(f"{'  '*level}{k}: {str(v)[:200]}")
                search_dict(v, level+1)
        elif isinstance(d, list):
            for item in d:
                search_dict(item, level+1)

    search_dict(data)
