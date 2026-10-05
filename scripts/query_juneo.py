# -*- coding: utf-8 -*-
import urllib.request, json, ssl, sys

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {'Authorization': f"APIKey {API_KEY}", 'Content-Type': 'application/json'}
ctx = ssl._create_unverified_context()

procs = ["08106599520268190203", "0810659-95.2026.8.19.0203"]

for p in procs:
    url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"
    payload = json.dumps({"query": {"match": {"numeroProcesso": p}}, "size": 1}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            print(f"Busca '{p}': {len(hits)} hits")
            if hits:
                src = hits[0]["_source"]
                print("Órgão:", src.get("orgaoJulgador", {}).get("nome"))
                print("Classe:", src.get("classe", {}).get("nome"))
                print("Atualizado em:", src.get("dataHoraUltimaAtualizacao"))
                movs = sorted(src.get("movimentos", []), key=lambda m: m.get("dataHora", ""), reverse=True)
                print(f"Total de movimentos: {len(movs)}")
                for m in movs[:10]:
                    print(f"  • {m.get('dataHora')[:19]} — {m.get('nome')}")
    except Exception as e:
        print(f"Erro em {p}: {e}")
