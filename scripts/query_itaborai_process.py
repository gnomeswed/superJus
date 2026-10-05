# -*- coding: utf-8 -*-
import json
import urllib.request
import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

api_key = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
target_dir = r"c:\Projetos\superJus\Clientes\Renato_Bastos_Rocha"
num_proc = "0802759-53.2025.8.19.0023"
clean_num = "08027595320258190023"

print(f"=== CONSULTANDO AÇÃO PENAL DE ORIGEM: {num_proc} (1ª Vara Criminal de Itaboraí) ===")

url_tjrj = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
headers = {"Authorization": f"APIKey {api_key}", "Content-Type": "application/json"}
q = {"query": {"match": {"numeroProcesso": clean_num}}}

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
        dt = src.get("dataAjuizamento")
        assuntos = [a.get("nome", "") for a in src.get("assuntos", [])]
        movs = src.get("movimentos", [])
        movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)
        
        polos = src.get("dadosBasicos", {}).get("polo", [])
        partes = []
        for p in polos:
            pol = p.get("polo", "")
            for part in p.get("parte", []):
                pess = part.get("pessoa", {})
                n = pess.get("nome")
                doc = pess.get("numeroDocumentoPrincipal")
                partes.append(f"{pol}: {n} ({doc})")
                
        print(f"\n📌 Processo: {clean_num} ({grau}) | Órgão: {orgao}")
        print(f"   Classe: {classe} | Assuntos: {', '.join(assuntos)}")
        print(f"   Data Ajuizamento: {dt}")
        print(f"   Partes: {', '.join(partes)}")
        print(f"   Total Movimentações: {len(movs)}")
        print("   Últimos 5 movimentos:")
        for m in movs_sorted[:5]:
            print(f"     [{m.get('dataHora')}] {m.get('nome')} ({m.get('codigo')})")
            
        with open(os.path.join(target_dir, f"acao_penal_{clean_num}_{grau}.json"), "w", encoding="utf-8") as f:
            json.dump(src, f, ensure_ascii=False, indent=2)

print("\n=== CONCLUÍDO ===")
