# -*- coding: utf-8 -*-
import os, sys, json, urllib.request
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw=="
HEADERS = {
    'Authorization': f"APIKey {API_KEY}",
    'Content-Type': 'application/json'
}

proc_clean = "00118579520248190002"
proc_fmt = "0011857-95.2024.8.19.0002"

def query_endpoint(endpoint, payload):
    url = f"https://api-publica.datajud.cnj.jus.br/{endpoint}/_search"
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=req_data, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

print("=" * 80)
print(f"🔍 VARREDURA AO VIVO DATAJUD CNJ — PROCESSO DE LUCAS DE SOUZA FREITAS")
print(f"⏰ Consulta em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
print(f"⚖️ Número do Processo: {proc_fmt}")
print("=" * 80)

# 1. Consulta TJRJ
res_tjrj = query_endpoint("api_publica_tjrj", {
    "query": {"match": {"numeroProcesso": proc_clean}},
    "size": 10
})

hits = res_tjrj.get("hits", {}).get("hits", [])
print(f"\n📊 Total de Registros Encontrados no TJRJ: {len(hits)}")

for idx, hit in enumerate(hits, 1):
    src = hit["_source"]
    grau = src.get("grau", "N/I")
    classe = src.get("classe", {}).get("nome", "N/I")
    orgao = src.get("orgaoJulgador", {}).get("nome", "N/I")
    dt_at = src.get("dataHoraUltimaAtualizacao", "N/I")
    movs = src.get("movimentos", [])
    movs_sorted = sorted(movs, key=lambda m: m.get("dataHora", ""), reverse=True)

    print(f"\n[{idx}] 🏛️ Órgão: {orgao} | Classe: {classe} | Grau: {grau}")
    print(f"    📅 Última Atualização no Banco CNJ: {dt_at}")
    print(f"    📑 Total de Movimentos: {len(movs)}")
    print("    📌 Últimos 10 Atos Registrados:")
    for m in movs_sorted[:10]:
        dt = m.get("dataHora", "")
        nome = m.get("nome", "")
        code = m.get("codigo", "")
        comps = m.get("complementosTabelados", [])
        comp_str = ""
        if comps:
            comp_str = " (" + ", ".join([f"{c.get('nome')}: {c.get('descricao')}" for c in comps]) + ")"
        print(f"       • {dt[:19].replace('T', ' ')} — {nome}{comp_str} [Cód. {code}]")

# 2. Consulta STJ
res_stj = query_endpoint("api_publica_stj", {
    "query": {"match": {"numeroProcesso": proc_clean}},
    "size": 5
})
hits_stj = res_stj.get("hits", {}).get("hits", [])
print(f"\n🏛️ Consulta STJ (api_publica_stj): {len(hits_stj)} registros encontrados.")

print("\n" + "=" * 80)
print("✅ Varredura ao vivo concluída com sucesso.")
print("=" * 80)
