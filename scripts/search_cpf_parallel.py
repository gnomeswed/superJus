# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

cpf = "06429650723"
cpf_formatted = "064.296.507-23"

# Principais tribunais
tribunais = [
    "tjrj", "tjsp", "tjmg", "tjes", "tjmt", "tjba", "trf2", "trf1", "stj"
]

print(f"=== INICIANDO PESQUISA POR CPF: {cpf_formatted} ({cpf}) ===", flush=True)

def query_tribunal(tb):
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
    
    try:
        req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            return tb, hits, None
    except Exception as e:
        return tb, [], str(e)

results_by_tribunal = {}

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = {executor.submit(query_tribunal, tb): tb for tb in tribunais}
    for future in as_completed(futures):
        tb, hits, err = future.result()
        if err:
            print(f"[{tb.upper()}] Erro: {err}", flush=True)
        else:
            print(f"[{tb.upper()}] Encontrados: {len(hits)} processo(s)", flush=True)
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
                    print(f"   -> [{tb.upper()}] Proc: {np} | Classe: {classe} | Assunto: {assunto_str}", flush=True)
                    print(f"      Órgão: {orgao}", flush=True)
                    print(f"      Partes: {', '.join(partes_nomes)}", flush=True)
                    print(f"      Última Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}\n", flush=True)

out_file = "scripts/cpf_06429650723_parallel_results.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results_by_tribunal, f, ensure_ascii=False, indent=2)

print(f"\n==================================================", flush=True)
print(f"Varredura concluída! Tribunais com processos: {list(results_by_tribunal.keys())}", flush=True)
