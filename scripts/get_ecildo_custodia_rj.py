# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
num_proc = "0122675-83.2025.8.19.0001"
clean_num = "01226758320258190001"

print(f"=== CONSULTANDO AUTOS DA CUSTÓDIA RJ: {num_proc} ===")

url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q = {"query": {"match": {"numeroProcesso": clean_num}}}

req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    hits = data.get("hits", {}).get("hits", [])
    print(f"Hits: {len(hits)}")
    if hits:
        src = hits[0]["_source"]
        dt_aj = src.get("dataAjuizamento")
        classe = src.get("classe", {}).get("nome")
        orgao = src.get("orgaoJulgador", {}).get("nome")
        assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
        movs = src.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""))
        
        print(f"Data Ajuizamento: {dt_aj}")
        print(f"Órgão: {orgao} | Classe: {classe}")
        print(f"Assuntos: {', '.join(assuntos)}")
        print(f"Total Movimentos: {len(movs)}")
        print("\n--- Linha do Tempo da Prisão / Custódia no RJ ---")
        for m in movs_sorted:
            dt = m.get("dataHora", "")[:19].replace("T", " ")
            comps = m.get("complementosTabelados", [])
            comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
            print(f"[{dt}] {m.get('nome')} (Cód {m.get('codigo')})" + (f" - {comp_str}" if comp_str else ""))
            
        out_file = r"c:\Projetos\superJus\Clientes\Ecildo_Victor\processos\custodia_rj_0122675-83.2025.8.19.0001.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(src, f, ensure_ascii=False, indent=2)
        print(f"\nSalvo em {out_file}")
