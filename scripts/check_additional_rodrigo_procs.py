# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"

procs_to_check = [
    ("0800060-52.2023.8.19.0058", "08000605220238190058", "Ação Penal 1 (Saquarema)"),
    ("0800262-29.2023.8.19.0058", "08002622920238190058", "Ação Penal 2 (Saquarema)"),
    ("0801082-93.2023.8.19.0043", "08010829320238190043", "Agravo de Execução Penal / VEP"),
    ("0809172-80.2023.8.19.0014", "08091728020238190014", "Apelação Criminal")
]

print("=== VERIFICANDO TODOS OS PROCESSOS CONEXOS E EXECUÇÃO PENAL ===")

results = {}

for num_cnj, clean_num, desc in procs_to_check:
    print(f"\n--- Consultando {num_cnj} ({desc}) ---")
    q = {"query": {"match": {"numeroProcesso": clean_num}}, "size": 10}
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  -> Hits: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                classe = src.get("classe", {}).get("nome")
                grau = src.get("grau")
                dt = src.get("dataAjuizamento")
                assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
                
                polos = src.get("dadosBasicos", {}).get("polo", [])
                partes = []
                for p in polos:
                    pol = p.get("polo", "")
                    for part in p.get("parte", []):
                        pess = part.get("pessoa", {})
                        n = pess.get("nome")
                        if n:
                            partes.append(f"{pol}: {n}")
                            
                movs = src.get("movimentos", [])
                movs_desc = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                
                print(f"  📌 Processo: {np} | Grau: {grau} | Órgão: {orgao} | Classe: {classe}")
                print(f"     Assuntos: {', '.join(assuntos)}")
                print(f"     Partes: {', '.join(partes)}")
                print(f"     Último Mov: {movs_desc[0].get('dataHora') if movs_desc else ''} - {movs_desc[0].get('nome') if movs_desc else ''}")
                
                # Salvar em pasta própria
                p_dir = os.path.join(target_dir, "processos", num_cnj)
                os.makedirs(p_dir, exist_ok=True)
                with open(os.path.join(p_dir, f"raw_{grau}.json"), "w", encoding="utf-8") as f:
                    json.dump(src, f, ensure_ascii=False, indent=2)
                    
    except Exception as e:
        print(f"  Erro: {e}")

print("\n=== CONCLUÍDO ===")
