# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
nome1 = "Rodrigo dos Reis Nobrega"
nome2 = "Rodrigo dos Reis Nóbrega"

target_dir = r"c:\Projetos\superJus\Clientes\Rodrigo_Nobrega"
os.makedirs(target_dir, exist_ok=True)

print(f"=== PESQUISANDO PROCESSOS: {nome2} (Saquarema/RJ) ===")

url_datajud = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

query = {
    "query": {
        "bool": {
            "should": [
                {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": nome1}},
                {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": nome2}},
                {"query_string": {"query": f'"{nome1}"'}},
                {"query_string": {"query": f'"{nome2}"'}},
                {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": {"value": "*Rodrigo*Reis*Nobrega*", "case_insensitive": True}}},
                {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": {"value": "*Rodrigo*Reis*Nóbrega*", "case_insensitive": True}}}
            ],
            "minimum_should_match": 1
        }
    },
    "size": 50
}

all_found = []

try:
    req = urllib.request.Request(url_datajud, data=json.dumps(query).encode("utf-8"), headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        hits = data.get("hits", {}).get("hits", [])
        print(f"[DATAJUD TJRJ] Encontrados: {len(hits)} processo(s)")
        
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
                pol = p.get("polo", "")
                for part in p.get("parte", []):
                    pess = part.get("pessoa", {})
                    n = pess.get("nome")
                    doc = pess.get("numeroDocumentoPrincipal")
                    if n:
                        partes_nomes.append(f"{pol}: {n} ({doc if doc else 'sem doc'})")
                        
            proc_entry = {
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
                "raw_source": src
            }
            all_found.append(proc_entry)
            print(f"  📌 Processo: {np} | Classe: {classe} | Assunto: {assunto_str}")
            print(f"     Órgão Julgador: {orgao}")
            print(f"     Partes: {', '.join(partes_nomes)}")
            print(f"     Última Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}\n")

except Exception as e:
    print(f"Erro DataJud: {e}")

out_json = os.path.join(target_dir, "datajud_results_rodrigo_nobrega.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(all_found, f, ensure_ascii=False, indent=2)

print(f"Salvo em: {out_json}")
