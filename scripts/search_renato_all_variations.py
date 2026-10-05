# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"

url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

print("=== VARREDURA DE PROCESSOS CONEXOS, VEP E NOVAS AÇÕES ===")

# Consultas específicas
queries = [
    # 1. Execuções penais ou processos com "Renato Bastos"
    {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": '"Renato Bastos"'}}
                ]
            }
        },
        "size": 50
    },
    # 2. Processos em Itaperuna com "Bastos Rocha"
    {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": '"Bastos Rocha"'}}
                ]
            }
        },
        "size": 50
    },
    # 3. Processos com o número da ação originária referenciada em outros feitos
    {
        "query": {
            "bool": {
                "must": [
                    {"query_string": {"query": '"0801630-04.2025.8.19.0026" OR "08016300420258190026"'}}
                ]
            }
        },
        "size": 50
    }
]

for idx, q in enumerate(queries, 1):
    print(f"\n[Busca {idx}] Executando...")
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  -> Hits: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                grau = src.get("grau")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                dt = src.get("dataAjuizamento")
                assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
                
                polos = src.get("dadosBasicos", {}).get("polo", [])
                partes = []
                for p in polos:
                    pol = p.get("polo", "")
                    for part in p.get("parte", []):
                        pess = part.get("pessoa", {})
                        n = pess.get("nome")
                        doc = pess.get("numeroDocumentoPrincipal")
                        partes.append(f"{pol}: {n} ({doc})")
                        
                print(f"  📌 Processo: {np} ({grau}) | {classe}")
                print(f"     Órgão: {orgao} | Data: {dt}")
                print(f"     Assuntos: {', '.join(assuntos)}")
                print(f"     Partes: {', '.join(partes)}\n")
    except Exception as e:
        print(f"  Erro: {e}")
