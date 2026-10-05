# -*- coding: utf-8 -*-
"""
Pesquisa Exaustiva no DataJud CNJ com a nova Chave de API
Cliente: Lucas de Souza Freitas
"""
import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')
os.environ["PYTHONIOENCODING"] = "utf-8"

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f"APIKey {API_KEY}",
    'Content-Type': 'application/json'
}

OUT_DIR = r"C:\Projetos\superJus\Clientes\Lucas_Freitas\03_Documentos_do_Processo\_datajud_completo_2026"
os.makedirs(OUT_DIR, exist_ok=True)

def query_endpoint(endpoint, payload):
    url = f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search"
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

print("==========================================================================")
print("=== CONSULTA DATAJUD CNJ — CHAVE DE API ATIVADA COM SUCESSO ===")
print("==========================================================================\n", flush=True)

# 1. TJRJ — Busca por Nome Completo "Lucas de Souza Freitas"
print("[1] Consultando TJRJ (api_publica_tjrj) por 'Lucas de Souza Freitas'...", flush=True)
p1 = {
    "query": {
        "bool": {
            "must": [
                {"match_phrase": {"partes.nome": "Lucas de Souza Freitas"}}
            ]
        }
    },
    "size": 50
}
res_tjrj = query_endpoint("api_publica_tjrj", p1)
hits_tjrj = res_tjrj.get('hits', {}).get('hits', [])
print(f"-> Total de processos encontrados no TJRJ para 'Lucas de Souza Freitas': {len(hits_tjrj)}\n", flush=True)

all_procs_summary = []

for idx, hit in enumerate(hits_tjrj, 1):
    src = hit['_source']
    num = src.get('numeroProcesso')
    classe = src.get('classe', {}).get('nome', 'N/I')
    orgao = src.get('orgaoJulgador', {}).get('nome', 'N/I')
    assuntos = [a.get('nome') for a in src.get('assuntos', [])]
    dt_atualizacao = src.get('dataHoraUltimaAtualizacao', 'N/I')
    movs = src.get('movimentos', [])
    movs_sorted = sorted(movs, key=lambda m: m.get('dataHora', ''), reverse=True)
    
    info = {
        "numero": num,
        "classe": classe,
        "orgao": orgao,
        "assuntos": assuntos,
        "ultima_atualizacao": dt_atualizacao,
        "total_movimentos": len(movs),
        "ultimas_3_movs": [f"{m.get('dataHora')[:19].replace('T', ' ')}: {m.get('nome')}" for m in movs_sorted[:3]]
    }
    all_procs_summary.append(info)
    
    print(f"--- PROCESSO #{idx} ---")
    print(f"  Número: {num}")
    print(f"  Órgão: {orgao}")
    print(f"  Classe: {classe}")
    print(f"  Assuntos: {assuntos}")
    print(f"  Última Atualização no CNJ: {dt_atualizacao}")
    print(f"  Total de Movimentos: {len(movs)}")
    print(f"  Últimos Movimentos:")
    for m in movs_sorted[:3]:
        print(f"    * {m.get('dataHora')[:19].replace('T', ' ')} — {m.get('nome')}")
    print()

with open(os.path.join(OUT_DIR, "datajud_tjrj_lucas_completo.json"), "w", encoding="utf-8") as f:
    json.dump(res_tjrj, f, indent=2, ensure_ascii=False)

# 2. STJ — Busca por Nome Completo "Lucas de Souza Freitas"
print("[2] Consultando STJ (api_publica_stj)...", flush=True)
res_stj = query_endpoint("api_publica_stj", p1)
hits_stj = res_stj.get('hits', {}).get('hits', [])
print(f"-> Total de processos no STJ: {len(hits_stj)}", flush=True)
for h in hits_stj:
    s = h['_source']
    print(f"  STJ: {s.get('numeroProcesso')} | {s.get('classe', {}).get('nome')} | {s.get('orgaoJulgador', {}).get('nome')}")

# 3. TRF2 (Federal) — Busca por Nome Completo
print("\n[3] Consultando TRF2 (api_publica_trf2)...", flush=True)
res_trf2 = query_endpoint("api_publica_trf2", p1)
hits_trf2 = res_trf2.get('hits', {}).get('hits', [])
print(f"-> Total de processos no TRF2: {len(hits_trf2)}", flush=True)
for h in hits_trf2:
    s = h['_source']
    print(f"  TRF2: {s.get('numeroProcesso')} | {s.get('classe', {}).get('nome')}")

# Salvar relatório consolidado
with open(os.path.join(OUT_DIR, "resumo_processos_datajud.json"), "w", encoding="utf-8") as f:
    json.dump({
        "tjrj_processos": all_procs_summary,
        "stj_total": len(hits_stj),
        "trf2_total": len(hits_trf2)
    }, f, indent=2, ensure_ascii=False)

print("\n==========================================================================")
print(f"=== CONSULTA CONCLUÍDA! Arquivos salvos em: {OUT_DIR} ===")
print("==========================================================================", flush=True)
