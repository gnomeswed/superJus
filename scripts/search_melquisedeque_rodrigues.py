# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

nome = "Melquisedeque Rodrigues dos Santos"
cpf = "06429650723"
cpf_formatted = "064.296.507-23"

tribunais = ["tjrj", "trf2", "stj", "tjsp", "tjmg"]

print(f"=== PESQUISANDO: {nome} (CPF: {cpf_formatted}) ===")

all_results = {}

for tb in tribunais:
    url = f"https://api-publica.datajud.cnj.jus.br/api_publica_{tb}/_search"
    headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
    
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": nome}},
                    {"query_string": {"query": f'"{nome}"'}},
                    {"query_string": {"query": f'"Melquisedeque Rodrigues"'}},
                    {"query_string": {"query": f'"{cpf}"'}},
                    {"query_string": {"query": f'"{cpf_formatted}"'}},
                    {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": {"value": "*Melquisedeque*Rodrigues*", "case_insensitive": True}}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 50
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(query).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"[{tb.upper()}] Encontrados: {len(hits)} processo(s)")
            if hits:
                all_results[tb] = []
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
                            n = pess.get("nome")
                            doc = pess.get("numeroDocumentoPrincipal")
                            pol = p.get("polo", "")
                            if n:
                                partes_nomes.append(f"{pol}: {n} ({doc if doc else 'sem doc'})")
                                
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
                    all_results[tb].append(entry_info)
                    print(f"   -> [{tb.upper()}] Proc: {np} | Classe: {classe} | Assunto: {assunto_str}")
                    print(f"      Órgão: {orgao}")
                    print(f"      Partes: {', '.join(partes_nomes)}")
                    print(f"      Última Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}\n")
    except Exception as e:
        print(f"[{tb.upper()}] Erro: {e}")

out_file = "scripts/melquisedeque_rodrigues_results.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f"\nBusca finalizada! Salvo em {out_file}")
