# -*- coding: utf-8 -*-
import json
import urllib.request
import urllib.parse
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"
os.makedirs(target_dir, exist_ok=True)

cpf_clean = "12498197761"
cpf_fmt = "124.981.977-61"
nome = "Renato Bastos Rocha"

print("================================================================================")
print(f"=== VARREDURA DE PROCESSO NOVO (2025/2026): {nome} (CPF: {cpf_fmt}) ===")
print("================================================================================")

url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}

# Queries variadas para capturar qualquer menção recente
queries = [
    # 1. Busca ampla por CPF em qualquer campo de documento
    {
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": cpf_clean}},
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.numeroDocumentoPrincipal": cpf_fmt}},
                    {"query_string": {"query": f'"{cpf_clean}" OR "{cpf_fmt}"'}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 50
    },
    # 2. Busca por nome completo "Renato Bastos Rocha"
    {
        "query": {
            "bool": {
                "should": [
                    {"match_phrase": {"dadosBasicos.polo.parte.pessoa.nome": nome}},
                    {"query_string": {"query": f'"{nome}"'}}
                ],
                "minimum_should_match": 1
            }
        },
        "size": 50
    },
    # 3. Wildcard por Renato Bastos
    {
        "query": {
            "bool": {
                "must": [
                    {"wildcard": {"dadosBasicos.polo.parte.pessoa.nome.keyword": {"value": "*Renato*Bastos*Rocha*", "case_insensitive": True}}}
                ]
            }
        },
        "size": 50
    }
]

encontrados = {}

for idx, q in enumerate(queries, 1):
    print(f"\n[Estratégia {idx}] Executando busca no DataJud TJRJ...")
    try:
        req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"  -> Hits: {len(hits)}")
            for h in hits:
                src = h["_source"]
                np = src.get("numeroProcesso")
                grau = src.get("grau")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                dt = src.get("dataAjuizamento")
                assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
                
                polos = src.get("dadosBasicos", {}).get("polo", [])
                partes_nomes = []
                for p in polos:
                    pol = p.get("polo", "")
                    for part in p.get("parte", []):
                        pess = part.get("pessoa", {})
                        n = pess.get("nome")
                        doc = pess.get("numeroDocumentoPrincipal")
                        if n:
                            partes_nomes.append(f"{pol}: {n} ({doc})")
                            
                movs = src.get("movimentos", [])
                movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
                last_mov = movs_sorted[0] if movs_sorted else {}
                
                key = f"{np}_{grau}"
                if key not in encontrados:
                    encontrados[key] = {
                        "numeroProcesso": np,
                        "grau": grau,
                        "orgao": orgao,
                        "classe": classe,
                        "assuntos": ", ".join(assuntos),
                        "dataAjuizamento": dt,
                        "total_movimentos": len(movs),
                        "partes": partes_nomes,
                        "ultimo_movimento": {
                            "data": last_mov.get("dataHora"),
                            "nome": last_mov.get("nome")
                        },
                        "raw_source": src
                    }
                    print(f"  📌 Processo: {np} ({grau}) | {classe}")
                    print(f"     Órgão: {orgao} | Data: {dt}")
                    print(f"     Assuntos: {', '.join(assuntos)}")
                    print(f"     Partes: {', '.join(partes_nomes)}")
                    print(f"     Último Mov: {last_mov.get('dataHora')} - {last_mov.get('nome')}\n")
    except Exception as e:
        print(f"  ❌ Erro na consulta {idx}: {e}")

out_json = os.path.join(target_dir, "todos_processos_renato_bastos_rocha.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(list(encontrados.values()), f, ensure_ascii=False, indent=2)

print(f"\n✅ Total de processos únicos mapeados: {len(encontrados)}")
print(f"Salvo em: {out_json}")
