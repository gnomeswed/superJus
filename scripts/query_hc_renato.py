# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"
os.makedirs(target_dir, exist_ok=True)

print("=== CONSULTANDO HABEAS CORPUS: 0023757-47.2025.8.19.0000 ===")

url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q = {"query": {"match": {"numeroProcesso": "00237574720258190000"}}}

req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    hits = data.get("hits", {}).get("hits", [])
    print(f"Hits encontrados: {len(hits)}")
    if hits:
        src = hits[0]["_source"]
        classe = src.get("classe", {}).get("nome")
        orgao = src.get("orgaoJulgador", {}).get("nome")
        dt = src.get("dataAjuizamento")
        assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
        movs = src.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        
        print(f"Classe: {classe}")
        print(f"Órgão Julgador: {orgao}")
        print(f"Data Ajuizamento: {dt}")
        print(f"Assuntos: {', '.join(assuntos)}")
        print(f"Total Movimentações: {len(movs)}")
        print("\nÚltimos 10 movimentos:")
        for m in movs_sorted[:10]:
            comps = m.get("complementosTabelados", [])
            comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
            print(f"  [{m.get('dataHora')}] {m.get('nome')} ({m.get('codigo')})" + (f" - {comp_str}" if comp_str else ""))
            
        with open(os.path.join(target_dir, "hc_0023757-47.2025.8.19.0000_raw.json"), "w", encoding="utf-8") as f:
            json.dump(src, f, ensure_ascii=False, indent=2)

print("\n=== CONCLUÍDO ===")
