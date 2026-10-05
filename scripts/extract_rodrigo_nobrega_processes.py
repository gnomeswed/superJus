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
os.makedirs(target_dir, exist_ok=True)

processos = [
    ("0800060-52.2023.8.19.0058", "08000605220238190058", "Roubo Majorado - 2ª Vara Saquarema"),
    ("0800262-29.2023.8.19.0058", "08002622920238190058", "Ação Penal / Apelação - 2ª Vara Saquarema")
]

print("=== EXTRAINDO AUTOS E MOVIMENTAÇÕES DE RODRIGO DOS REIS NÓBREGA ===")

results = {}

for num_cnj, clean_num, desc in processos:
    print(f"\n--- Consultando {num_cnj} ({desc}) no DataJud TJRJ ---")
    proc_dir = os.path.join(target_dir, "processos", num_cnj)
    os.makedirs(proc_dir, exist_ok=True)
    
    q = {"query": {"match": {"numeroProcesso": clean_num}}}
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  -> Hits encontrados: {len(hits)}")
            if hits:
                src = hits[0]["_source"]
                with open(os.path.join(proc_dir, "datajud_raw.json"), "w", encoding="utf-8") as f:
                    json.dump(src, f, ensure_ascii=False, indent=2)
                    
                movs = src.get("movimentos", [])
                movs_desc = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                orgao = src.get("orgaoJulgador", {}).get("nome")
                classe = src.get("classe", {}).get("nome")
                assuntos = src.get("assuntos", [])
                assunto_str = ", ".join([a.get("nome", "") for a in assuntos])
                
                print(f"  📌 Órgão: {orgao}")
                print(f"     Classe: {classe} | Assunto: {assunto_str}")
                print(f"     Total Movimentos: {len(movs)}")
                print(f"     Último Movimento: {movs_desc[0].get('dataHora')} - {movs_desc[0].get('nome') if movs_desc else 'N/A'}")
                
                results[num_cnj] = {
                    "descricao": desc,
                    "orgao": orgao,
                    "classe": classe,
                    "assunto": assunto_str,
                    "total_movimentos": len(movs),
                    "ultimos_movimentos": movs_desc[:5]
                }
    except Exception as e:
        print(f"  ❌ Erro ao consultar {num_cnj}: {e}")

out_res = os.path.join(target_dir, "resumo_processos_rodrigo.json")
with open(out_res, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n✅ Concluído! Resumo salvo em {out_res}")
