# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"
os.makedirs(target_dir, exist_ok=True)

print("=== BUSCANDO NO STJ: RENATO BASTOS ROCHA ===")

url_stj = "https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

queries = [
    {"query": {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": "Renato Bastos Rocha"}}},
    {"query": {"query_string": {"query": '"0023757-47.2025.8.19.0000" OR "00237574720258190000"'}}},
    {"query": {"query_string": {"query": '"Renato Bastos Rocha"'}}}
]

for idx, q in enumerate(queries, 1):
    print(f"\n[Consulta {idx}]...")
    try:
        req = urllib.request.Request(url_stj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"Hits no STJ: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                dt = src.get("dataAjuizamento")
                movs = src.get("movimentos", [])
                movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                
                print(f"  📌 Processo STJ: {np} | Classe: {classe} | Órgão: {orgao}")
                print(f"     Data: {dt} | Total Movs: {len(movs)}")
                print(f"     Último Mov: {movs_sorted[0].get('dataHora') if movs_sorted else ''} - {movs_sorted[0].get('nome') if movs_sorted else ''}\n")
                
                with open(os.path.join(target_dir, f"stj_{np}_raw.json"), "w", encoding="utf-8") as f:
                    json.dump(src, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro: {e}")

print("=== FIM DA CONSULTA STJ ===")
