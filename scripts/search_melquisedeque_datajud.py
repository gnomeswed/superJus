# -*- coding: utf-8 -*-
import json
import urllib.request
import sys

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

tribunais = [
    "tjrj", "tjsp", "tjmg", "tjes", "tjmt", "tjba", "tjpr", "tjrs", "tjsc", "tjgo", "tjdf",
    "trf2", "trf1", "trf3", "trf4", "trf5", "stj"
]

search_terms = [
    "Melquisedeque",
    "Melquisedec",
    "Melquisedeq"
]

all_hits = {}

print("=== INICIANDO VARREDURA NACIONAL NO DATAJUD PARA: MELQUISEDEQUE ===")

for tb in tribunais:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
    
    query = {
        "query": {
            "bool": {
                "should": [
                    {"query_string": {"query": f'"{st}"'}} for st in search_terms
                ],
                "minimum_should_match": 1
            }
        },
        "size": 30
    }
    
    req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"[{tb.upper()}] Encontrados: {len(hits)} processo(s)")
            if hits:
                all_hits[tb] = []
                for h in hits:
                    src = h["_source"]
                    np = src.get("numeroProcesso")
                    classe = src.get("classe", {}).get("nome")
                    orgao = src.get("orgaoJulgador", {}).get("nome")
                    dt = src.get("dataAjuizamento")
                    movs = src.get("movimentos", [])
                    movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""))
                    last_mov = movs_sorted[-1] if movs_sorted else {}
                    assuntos = src.get("assuntos", [])
                    assunto_str = ", ".join([a.get("nome", "") for a in assuntos])
                    
                    # Check parties / characters if available
                    partes = src.get("dadosBasicos", {}).get("polo", [])
                    
                    entry_info = {
                        "tribunal": tb.upper(),
                        "numeroProcesso": np,
                        "classe": classe,
                        "orgaoJulgador": orgao,
                        "assuntos": assunto_str,
                        "dataAjuizamento": dt,
                        "total_movimentos": len(movs),
                        "ultima_movimentacao": {
                            "data": last_mov.get("dataHora"),
                            "nome": last_mov.get("nome")
                        }
                    }
                    all_hits[tb].append(entry_info)
                    print(f"   -> Proc: {np} | Classe: {classe} | Assunto: {assunto_str} | Órgão: {orgao}")
                    print(f"      Última Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}")
    except Exception as e:
        print(f"[{tb.upper()}] Erro na consulta: {e}")

with open("scripts/melquisedeque_datajud_results.json", "w", encoding="utf-8") as f:
    json.dump(all_hits, f, ensure_ascii=False, indent=2)

print(f"\nVarredura concluída! Total de tribunais com resultados: {len(all_hits)}")
