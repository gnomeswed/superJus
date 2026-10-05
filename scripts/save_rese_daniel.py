# -*- coding: utf-8 -*-
import json
import requests
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

CLIENT_DIR = r"c:\Projetos\superJus\Clientes\Daniel_Ferreira_Lima"
MOVS_DIR = os.path.join(CLIENT_DIR, "02_Movimentacoes")

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

r = requests.post(BASE_TJRJ, headers=HEADERS, json={
    "query": {"match": {"numeroProcesso": "00043013320188190073"}},
    "size": 5
}, timeout=30)

if r.status_code == 200:
    hits = r.json().get("hits", {}).get("hits", [])
    print(f"Total de registros obtidos: {len(hits)}")
    for i, h in enumerate(hits):
        src = h["_source"]
        orgao = src.get("orgaoJulgador", {}).get("nome", "")
        classe = src.get("classe", {}).get("nome", "")
        print(f"[{i}] {orgao} | {classe}")
        
        if "RECURSO" in classe.upper() or "DESA" in orgao.upper():
            json_file = os.path.join(MOVS_DIR, "datajud_raw_2a_instancia_rese.json")
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(src, f, indent=2, ensure_ascii=False)
            
            md_file = os.path.join(MOVS_DIR, "movimentacoes_2a_instancia_rese.md")
            movs = sorted(src.get("movimentos", []), key=lambda m: m.get("dataHora", ""), reverse=True)
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(f"# TJRJ 2ª Instância — Recurso em Sentido Estrito nº 0004301-33.2018.8.19.0073\n\n")
                f.write(f"- **Órgão Julgador:** {orgao}\n")
                f.write(f"- **Classe:** {classe}\n")
                f.write(f"- **Assuntos:** {', '.join([a.get('nome','') for a in src.get('assuntos',[])])}\n")
                f.write(f"- **Julgamento:** Acórdão de Não-Provimento em 22/05/2025\n")
                f.write(f"- **Baixa Definitiva:** 03/07/2025 (autos devolvidos a Guapimirim para o Júri)\n\n")
                f.write("| Data | Código | Movimento | Detalhes |\n| :--- | :--- | :--- | :--- |\n")
                for m in movs:
                    comps = [f"{c.get('nome')}: {c.get('descricao')}" for c in m.get("complementosTabelados", [])]
                    comp_str = "; ".join(comps) if comps else "-"
                    f.write(f"| {m.get('dataHora','')[:19].replace('T', ' ')} | {m.get('codigo','')} | {m.get('nome','')} | {comp_str} |\n")
            print(f"Salvo RESE em: {md_file}")

print("Concluído!")
