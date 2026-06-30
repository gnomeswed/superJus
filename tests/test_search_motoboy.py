from scripts.search_docs import search_docs
import json, os

root = r'C:\Projetos\Super Analista Jurídico\Clientes\Lucas_Freitas\Caso_Principal\documentos_processo'
queries = ['processo', 'movimento', 'decisao', ' TJRJ', 'audiencia']

results = {}
for q in queries:
    r = search_docs(root, q, max_results=5)
    results[q] = r

print(json.dumps(results, ensure_ascii=False, indent=2))
