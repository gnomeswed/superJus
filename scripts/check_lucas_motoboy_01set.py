# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
clean_num = "00118579520248190002"
nproc_fmt = "0011857-95.2024.8.19.0002"

print(f"=== VERIFICANDO ATUALIZAÇÕES DO PROCESSO DE LUCAS MOTOBOY: {nproc_fmt} (01/09/2026) ===")

url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q = {"query": {"match": {"numeroProcesso": clean_num}}, "size": 10}

req = urllib.request.Request(url_tjrj, data=json.dumps(q).encode("utf-8"), headers=headers)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    hits = data.get("hits", {}).get("hits", [])
    print(f"Hits encontrados: {len(hits)}")
    for h in hits:
        src = h["_source"]
        grau = src.get("grau")
        classe = src.get("classe", {}).get("nome")
        orgao = src.get("orgaoJulgador", {}).get("nome")
        dt_atualizacao = src.get("dataHoraUltimaAtualizacao")
        movs = src.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        
        print(f"\n==================================================")
        print(f"🏛️ Grau: {grau} | Órgão: {orgao}")
        print(f"Classe: {classe} | Total Movs: {len(movs)}")
        print(f"Última Atualização no Banco: {dt_atualizacao}")
        print("Últimos 10 movimentos:")
        for idx, m in enumerate(movs_sorted[:10], 1):
            dt = m.get("dataHora", "")[:19].replace("T", " ")
            comps = m.get("complementosTabelados", [])
            comp_str = " | ".join([f"{c.get('descricao')}: {c.get('nome')}" for c in comps])
            print(f"  {idx}. [{dt}] {m.get('nome')} (Cód {m.get('codigo')})" + (f" - {comp_str}" if comp_str else ""))
            
        out_dir = r"c:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_varredura_01_09_2026"
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, f"datajud_{grau}_{clean_num}.json"), "w", encoding="utf-8") as f:
            json.dump(src, f, ensure_ascii=False, indent=2)

print("\n=== VERIFICAÇÃO CONCLUÍDA ===")
