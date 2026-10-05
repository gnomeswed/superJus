# -*- coding: utf-8 -*-
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

DATAJUD_KEY = "APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {"Authorization": DATAJUD_KEY, "Content-Type": "application/json"}
BASE_TJRJ = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

r = requests.post(BASE_TJRJ, headers=HEADERS, json={
    "query": {"match": {"numeroProcesso": "00043013320188190073"}},
    "size": 1
})

if r.status_code == 200:
    hits = r.json().get("hits", {}).get("hits", [])
    if hits:
        src = hits[0]["_source"]
        print("=== PROCESSO LOCALIZADO NO TJRJ ===")
        print("Numero:", src.get("numeroProcesso"))
        print("Classe:", src.get("classe", {}).get("nome"), f"(Cod: {src.get('classe', {}).get('codigo')})")
        print("Orgao:", src.get("orgaoJulgador", {}).get("nome"))
        print("Ajuizamento:", src.get("dataAjuizamento"))
        print("Ultima Atualizacao:", src.get("dataHoraUltimaAtualizacao"))
        print("Assuntos:", [f"{a.get('nome')} (Cod: {a.get('codigo')})" for a in src.get("assuntos", [])])
        
        movs = src.get("movimentos", [])
        print(f"\nTotal de Movimentos: {len(movs)}")
        
        # Ordenar decrescente por data
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        print("\n--- ULTIMOS 20 MOVIMENTOS ---")
        for m in movs_sorted[:20]:
            comp_str = ""
            comps = m.get("complementosTabelados", [])
            if comps:
                comp_str = " | Comps: " + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps])
            print(f"{m.get('dataHora')[:19]} | Cod {m.get('codigo')}: {m.get('nome')}{comp_str}")
            
        # Salvar json resumido
        with open("processo_daniel_guapimirim.json", "w", encoding="utf-8") as f:
            json.dump({
                "numero": src.get("numeroProcesso"),
                "classe": src.get("classe"),
                "orgao": src.get("orgaoJulgador"),
                "dataAjuizamento": src.get("dataAjuizamento"),
                "dataHoraUltimaAtualizacao": src.get("dataHoraUltimaAtualizacao"),
                "assuntos": src.get("assuntos"),
                "ultimos_movimentos": movs_sorted[:30]
            }, f, indent=2, ensure_ascii=False)
            print("\nArquivo salvo: processo_daniel_guapimirim.json")
