# -*- coding: utf-8 -*-
import urllib.request, json, sys, os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.config import datajud_headers

sys.stdout.reconfigure(encoding="utf-8")

headers = datajud_headers()
url = "https://api-publica.datajud.cnj.jus.br/api_publica_tjrj/_search"

queries = [
    {"query": {"match": {"dadosBasicos.polo.parte.pessoa.nome": "Renan Rodrigues de Souza"}}, "size": 10},
    {"query": {"match": {"polo.parte.pessoa.nome": "Renan Rodrigues de Souza"}}, "size": 10},
    {"query": {"match_phrase": {"polo.parte.pessoa.nome": "Renan Rodrigues de Souza"}}, "size": 10},
    {"query": {"query_string": {"query": "Renan Rodrigues de Souza"}}, "size": 10},
    {"query": {"match": {"dadosBasicos.polo.parte.pessoa.nomeGenitora": "Lenir"}}, "size": 10}
]

for i, q in enumerate(queries):
    req = urllib.request.Request(url, data=json.dumps(q).encode("utf-8"), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", {}).get("hits", [])
            total = data.get("hits", {}).get("total", {})
            print(f"Query {i} total: {total} hits: {len(hits)}")
            for h in hits:
                src = h.get("_source", {})
                num = src.get("numeroProcesso")
                classe = src.get("classe", {}).get("nome")
                orgao = src.get("orgaoJulgador", {}).get("nome")
                print(f"  -> Proc: {num} | Classe: {classe} | Órgão: {orgao}")
    except Exception as e:
        print(f"Query {i} error: {e}")
