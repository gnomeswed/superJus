# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

cpf = "06429650723"
cpf_formatted = "064.296.507-23"

tribunais = [
    "tjrj", "tjsp", "tjmg", "tjes", "tjmt", "tjba", "tjpr", "tjrs", "tjsc", "tjgo",
    "trf2", "trf1", "trf3", "trf4", "trf5", "stj"
]

print(f"=== INICIANDO PESQUISA POR CPF: {cpf_formatted} ({cpf}) ===")

results_by_tribunal = {}

for tb in tribunais:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
    
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": cpf}},
                    {"match": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": cpf_formatted}},
                    {"query_string": {"query": f'"{cpf}"'}},
                    {"query_string": {"query": f'"{cpf_formatted}"'}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 30
    }
    
    req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"[{tb.upper()}] Encontrados: {len(hits)} processo(s)")
            if hits:
                results_by_tribunal[tb] = []
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
                    
                    # Extract parties
                    polos = src.get("dadosBasicos", {}).get("polo", [])
                    partes_nomes = []
                    for p in polos:
                        for part in p.get("parte", []):
                            pess = part.get("pessoa", {})
                            nome = pess.get("nome")
                            doc = pess.get("numeroDocumentoPrincipal")
                            if nome:
                                partes_nomes.append(f"{nome} ({doc if doc else 'sem doc'})")
                                
                    entry_info = {
                        "tribunal": tb.upper(),
                        "numeroProcesso": np,
                        "classe": classe,
                        "orgaoJulgador": orgao,
                        "assunto": assunto_str,
                        "dataAjuizamento": dt,
                        "total_movimentos": len(movs),
                        "partes": partes_nomes,
                        "ultima_movimentacao": {
                            "data": last_mov.get("dataHora"),
                            "nome": last_mov.get("nome"),
                            "comps": last_mov.get("complementosTabelados", [])
                        },
                        "movimentos": movs_sorted
                    }
                    results_by_tribunal[tb].append(entry_info)
                    print(f"   -> Proc: {np} | Classe: {classe} | Assunto: {assunto_str}")
                    print(f"      Órgão: {orgao}")
                    print(f"      Partes: {', '.join(partes_nomes)}")
                    print(f"      Última Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}\n")
    except Exception as e:
        print(f"[{tb.upper()}] Erro: {e}")

out_file = "scripts/cpf_06429650723_results.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results_by_tribunal, f, ensure_ascii=False, indent=2)

print(f"\nPesquisa finalizada! Resultados salvos em {out_file}")
