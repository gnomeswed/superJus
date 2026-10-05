# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="

cpf_clean = "12498197761"
cpf_fmt = "124.981.977-61"
nome = "Renato Bastos Rocha"

target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"
os.makedirs(target_dir, exist_ok=True)

print(f"=== PESQUISANDO PROCESSOS: {nome} (CPF: {cpf_fmt}) ===")

# Lista de tribunais para consulta DataJud
tribunais = [
    ("TJRJ", "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"),
    ("TRF2", "https://api-publica.datajud.cnj.jus.br/api_publica_trf2/_search"),
    ("TJSP", "https://api-publica.datajud.cnj.jus.br/api_publica_tjsp/_search"),
    ("TJMG", "https://api-publica.datajud.cnj.jus.br/api_publica_tjmg/_search")
]

headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

all_results = {}

for sigla, url in tribunais:
    print(f"\n--- Consultando DataJud: {sigla} ---")
    query = {
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": cpf_clean}},
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": cpf_fmt}},
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": nome}},
                    {"query_string": {"query": f'"{cpf_clean}" OR "{cpf_fmt}" OR "{nome}"'}}
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
            print(f"[{sigla}] Processos encontrados: {len(hits)}")
            all_results[sigla] = []
            
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                dt = src.get("dataAjuizamento")
                grau = src.get("grau")
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
                            
                item = {
                    "numeroProcesso": np,
                    "grau": grau,
                    "classe": classe,
                    "orgaoJulgador": orgao,
                    "assuntos": assunto_str,
                    "dataAjuizamento": dt,
                    "total_movimentos": len(movs),
                    "partes": partes_nomes,
                    "ultima_movimentacao": {
                        "data": last_mov.get("dataHora"),
                        "nome": last_mov.get("nome")
                    },
                    "raw_source": src
                }
                all_results[sigla].append(item)
                print(f"  📌 Processo: {np} ({grau}) | Órgão: {orgao}")
                print(f"     Classe: {classe} | Assunto: {assunto_str}")
                print(f"     Partes: {', '.join(partes_nomes)}")
                print(f"     Última Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}\n")
                
    except Exception as e:
        print(f"[{sigla}] Erro: {e}")

out_path = os.path.join(target_dir, "datajud_pesquisa_renato_bastos_rocha.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f"\nResultados gravados em: {out_path}")
