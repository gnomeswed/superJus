# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

procs = [
    ("0023013-51.2021.8.19.0078", "00230135120218190078", "Ação Penal Desmembrada (Júlio) - 2ª Vara Búzios"),
    ("0001140-87.2024.8.19.0078", "00011408720248190078", "Recurso em Sentido Estrito / Apenso Búzios"),
    ("0022975-39.2021.8.19.0078", "00229753920218190078", "Processo Originário (Corréus em Liberdade)"),
    ("0029845-67.2026.8.19.0000", "00298456720268190000", "Habeas Corpus - 7ª Câmara Criminal TJRJ")
]

print("=== CONSULTA DATAJUD OFICIAL TJRJ — TODOS OS PROCESSOS DE JÚLIO ===")

all_res = {}

for num_cnj, clean_num, desc in procs:
    print(f"\n--- Consultando {num_cnj} ({desc}) ---")
    q = {"query": {"match": {"numeroProcesso": clean_num}}}
    try:
        req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  -> Registros encontrados: {len(hits)}")
            if hits:
                src = hits[0]["_source"]
                movs = src.get("movimentos", [])
                movs_desc = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                orgao = src.get("orgaoJulgador", {}).get("nome")
                classe = src.get("classe", {}).get("nome")
                print(f"  📌 Órgão: {orgao} | Classe: {classe} | Total Movimentos: {len(movs)}")
                print(f"     Último movimento: {movs_desc[0].get('dataHora')} - {movs_desc[0].get('nome') if movs_desc else 'N/A'}")
                all_res[num_cnj] = {
                    "descricao": desc,
                    "orgao": orgao,
                    "classe": classe,
                    "total_movimentos": len(movs),
                    "ultimos_movimentos": movs_desc[:5]
                }
    except Exception as e:
        print(f"  ❌ Erro: {e}")

out_path = r"C:\Projetos\superJus\Clientes\Júlio_Pereira_Marcos\Caso_Principal\documentos_processo\tjrj_datajud_all_29ago.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_res, f, ensure_ascii=False, indent=2)

print(f"\n✅ Concluído! Salvo em {out_path}")
